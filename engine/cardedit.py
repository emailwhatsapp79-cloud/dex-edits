"""Shared engine for beat-cut edits (grown out of edit J).

An edit script builds a config dict and calls run(cfg). Layouts:
  'card' - landscape source (trailer / press film) cropped to a 4:5 card (1080x1350) over a blurred fill; the
           card swings in in 3D on section starts. Best for 720p/1080p letterboxed footage.
  'full' - vertical source (TikTok 9:16 or 4:5) scaled to fill the whole 1080x1920 frame.
Shot modes: 'real' 1x, 'slow' 0.4x, 'hero' 0.28x, 'black' (empty frame for text), 'split' (two landscape
sources stacked, for an A-vs-B ending).
Every shot sits inside one take of its source (clean_span), no take is used twice (checked before rendering),
and every cut lands on the frame of its drum hit (measured after rendering)."""
import os, sys, math, subprocess
from concurrent.futures import ThreadPoolExecutor
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
sys.path.insert(0, os.path.dirname(__file__))
import velocity
from velocity import frame_for, cut_frames, src_needed, clean_span, W, H, FPS, IFPS
_a = sys.argv; sys.argv = [sys.argv[0]]
from edit_c_justdance import flash, chroma, zoom, gblur, dec, ease, VIG, GRAIN, ROOT
sys.argv = _a

CW, CH, CY = 1080, 1350, 300                     # card size and top y
ANTON = os.path.join(ROOT, 'fonts', 'Anton.ttf'); ORB = os.path.join(ROOT, 'fonts', 'Orbitron.ttf')

# ---------------------------------------------------------------- source takes
_det = {}
def union_cuts(path):
    """Hard cuts in a source: union of both detectors (race/film footage fools each one differently)."""
    if path not in _det:
        cs = []
        for d in ('hist', 'scene'):
            velocity.DETECTOR = d; cs += velocity._source_cuts_orig(path)
        cs = sorted(cs); _det[path] = [c for i, c in enumerate(cs) if i == 0 or c - cs[i - 1] > 0.06]
    return _det[path]
if not hasattr(velocity, '_source_cuts_orig'):
    velocity._source_cuts_orig = velocity.source_cuts
velocity.source_cuts = union_cuts


def probe(path):
    out = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v', '-show_entries', 'stream=width,height',
                          '-of', 'csv=p=0', path], capture_output=True, text=True).stdout.strip().split(',')
    return int(out[0]), int(out[1])


# ---------------------------------------------------------------- footage prep
def _vf(cfg, path, cx, out_w, out_h, interp=True):
    """Crop the source's active picture (letterbox removed) to out_w:out_h aspect around cx, scale, sharpen."""
    sw, sh = probe(path)
    ay0, ah = cfg.get('active', {}).get(os.path.basename(path), (0, sh))
    cw = int(min(sw, ah * out_w / out_h)) // 2 * 2; chh = int(min(ah, cw * out_h / out_w)) // 2 * 2
    x = int((sw - cw) * cx); y = ay0 + (ah - chh) // 2
    # real-speed shots keep their own frames (frame repeat, no motion interpolation = no smear); only slow-mo
    # shots are interpolated
    tail = (f"minterpolate=fps={IFPS}:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1" if interp else f"fps={IFPS}")
    return f"crop={cw}:{chh}:{x}:{y},scale={out_w}:{out_h}:flags=lanczos,unsharp=5:5:0.8:3:3:0.4,{tail}"


def _cut(cfg, path, src, need, cx, out_w, out_h, tag, interp=True):
    out = os.path.join(cfg['tmp'], f"{tag}_{os.path.basename(path)[:-4]}_{src:.2f}_{need:.2f}_{cx:.2f}_{out_w}{'' if interp else '_r'}.mp4")
    if not os.path.exists(out):
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{src:.3f}', '-t', f'{need:.3f}', '-i', path,
                        '-vf', _vf(cfg, path, cx, out_w, out_h, interp), '-an', '-c:v', 'libx264', '-crf', '13',
                        '-preset', 'veryfast', out], check=True)
    return out


SQ_Y = 300                                       # top of the 1080x1080 'showroom' square


def size_for(cfg):
    return {'card': (CW, CH), 'square': (W, W), 'broadcast': (W, 608), 'window': (W, 608), 'tall': (W, cfg.get('pic_h', 1440))}.get(cfg['layout'], (W, H))


def prep(cfg):
    os.makedirs(cfg['tmp'], exist_ok=True)
    shots = cfg['shots']; ow, oh = size_for(cfg)
    def job(i):
        s = shots[i]
        if s['mode'] == 'black': return None
        dur = s['t1'] - s['t0']
        if s['mode'] == 'split':
            m = s.get('sub_mode', 'slow'); need = src_needed(m, dur) + cfg.get('pad', 0.15)
            return [_cut(cfg, os.path.join(cfg['srcdir'], f), src, need, cx, W, 860, f's{i:02d}{k}')
                    for k, (f, src, cx) in enumerate(s['parts'])]
        need = src_needed(s['mode'], dur) + cfg.get('pad', 0.15)
        return _cut(cfg, os.path.join(cfg['srcdir'], s['file']), s['src'], need, s['cx'], ow, oh, f'{i:02d}',
                    interp=s['mode'] != 'real')
    with ThreadPoolExecutor(4) as ex:
        return list(ex.map(job, range(len(shots))))


class Reader:
    def __init__(self, path, w, h):
        self.w, self.h = w, h
        self.p = subprocess.Popen(['ffmpeg', '-v', 'error', '-i', path, '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'],
                                  stdout=subprocess.PIPE)
        self.buf = []; self.idx = -1

    def get(self, i):
        n = self.w * self.h * 3
        while self.idx < i:
            b = self.p.stdout.read(n)
            if len(b) < n: break
            self.idx += 1; self.buf.append(np.frombuffer(b, np.uint8).reshape(self.h, self.w, 3))
            if len(self.buf) > 4: self.buf.pop(0)
        k = max(0, len(self.buf) - 1 - max(0, self.idx - i))
        return self.buf[k] if self.buf else np.zeros((self.h, self.w, 3), np.uint8)

    def close(self): self.p.kill()


# ---------------------------------------------------------------- look
def look(a, warm=0.0, sat=1.12):
    lum = a @ np.array([0.299, 0.587, 0.114], np.float32)
    a = lum[..., None] + (a - lum[..., None]) * sat
    a = np.clip((a - 0.025) * 1.07, 0, 1); s = a * a * (3 - 2 * a); a = s * 0.4 + a * 0.6
    l = lum[..., None]
    return np.clip(a + (1 - l) * np.array([-0.015, 0.0, 0.025]) + l * np.array([0.015 + warm, 0.005, -0.01 - warm]), 0, 1)


_yy, _xx = np.mgrid[0:CH, 0:CW].astype(np.float32)
CARD_VIG = (1 - 0.35 * np.clip(np.sqrt(((_xx - CW / 2) / (CW / 2)) ** 2 + ((_yy - CH / 2) / (CH / 2)) ** 2) - 0.6, 0, 1))[..., None]


def background(card):
    im = Image.fromarray((card * 255).astype(np.uint8)).resize((96, 120), Image.BILINEAR).filter(ImageFilter.GaussianBlur(5))
    bw = int(H * CW / CH)
    im = im.resize((bw, H), Image.BILINEAR).crop(((bw - W) // 2, 0, (bw - W) // 2 + W, H))
    return np.asarray(im).astype(np.float32) / 255 * 0.42


def _persp_coeffs(src, dst):
    A, b = [], []
    for (x, y), (u, v) in zip(dst, src):
        A += [[x, y, 1, 0, 0, 0, -u * x, -u * y], [0, 0, 0, x, y, 1, -v * x, -v * y]]; b += [u, v]
    return np.linalg.solve(np.array(A, np.float64), np.array(b, np.float64)).tolist()


_SHADOW = None
def place(bg, card, ang=0.0, scale=1.0):
    """Card onto background; ang = rotation about the vertical axis in degrees (3D swing)."""
    global _SHADOW
    out = bg.copy(); cx, cy = W / 2, CY + CH / 2; hw, hh = CW / 2 * scale, CH / 2 * scale
    if abs(ang) < 0.3 and abs(scale - 1) < 1e-3:
        if _SHADOW is None:
            sh = np.zeros((H, W), np.float32); sh[CY + 18:CY + CH + 18, 12:W - 12] = 1
            _SHADOW = np.asarray(Image.fromarray((sh * 255).astype(np.uint8)).resize((W // 8, H // 8))
                                 .filter(ImageFilter.GaussianBlur(4)).resize((W, H), Image.BILINEAR)).astype(np.float32)[..., None] / 255
        out = out * (1 - 0.6 * _SHADOW); out[CY:CY + CH] = card; return out
    r = math.radians(ang); d = 1800.0; pts = []
    for sx, sy in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
        x3, z3 = sx * hw * math.cos(r), sx * hw * math.sin(r); k = d / (d + z3)
        pts.append((cx + x3 * k, cy + sy * hh * k))
    co = _persp_coeffs([(0, 0), (CW, 0), (CW, CH), (0, CH)], pts)
    im = Image.fromarray((card * 255).astype(np.uint8)).convert('RGBA')
    wa = np.asarray(im.transform((W, H), Image.PERSPECTIVE, co, Image.BILINEAR)).astype(np.float32) / 255
    m = wa[..., 3:4]; return out * (1 - m) + wa[..., :3] * m


# ---------------------------------------------------------------- text
_tc = {}
def text_layer(text, font, size, cy, maxw=960):
    key = (text, font, size, cy)
    if key in _tc: return _tc[key]
    lines = text.split('|'); f = ImageFont.truetype(font, size)
    while max(f.getbbox(l)[2] for l in lines) > maxw:
        size -= 6; f = ImageFont.truetype(font, size)
    m = Image.new('L', (W, H), 0); d = ImageDraw.Draw(m); lh = int(size * 1.08); y0 = cy - lh * len(lines) // 2
    for i, l in enumerate(lines):
        bb = f.getbbox(l); d.text(((W - bb[2]) / 2, y0 + i * lh - bb[1] // 2), l, font=f, fill=255)
    a = np.asarray(m).astype(np.float32) / 255
    sh = np.asarray(m.filter(ImageFilter.GaussianBlur(16))).astype(np.float32) / 255
    _tc[key] = (a[..., None], np.clip(sh * 1.4, 0, 1)[..., None]); return _tc[key]


def put(a, text, k, font=ANTON, size=150, cy=CY + CH // 2, dy=0):
    if k <= 0.01: return a
    al, sh = text_layer(text, font, size, cy)
    if dy: al = np.roll(al, int(dy), 0); sh = np.roll(sh, int(dy), 0)
    a = a * (1 - sh * 0.55 * k)
    return a * (1 - al * k) + al * k


# ---------------------------------------------------------------- render
def _gray(a):
    return np.repeat((a @ np.array([0.299, 0.587, 0.114], np.float32))[..., None], 3, 2)


def radial(a, k):
    """Radial zoom blur (k 0..1): average of progressively zoomed copies."""
    if k < 0.03: return a
    acc = a.copy(); n = 6
    for j in range(1, n): acc += zoom(a, 1 + 0.12 * k * j / n)
    return acc / n


def shot_fx(a, fx, lf):
    """Per-shot effects from the F1-edit style: 'bw' black & white, 'strobe' colour/B&W every 4 frames,
    'xerox' 3 photocopy (threshold) frames on the hit, 'radial' zoom blur decaying from the hit."""
    if 'bw' in fx: a = np.clip((_gray(a) - 0.05) * 1.15, 0, 1)
    if 'strobe' in fx and (lf // 4) % 2 == 1: a = np.clip((_gray(a) - 0.05) * 1.2, 0, 1)
    if 'xerox' in fx and lf < 3:
        g = _gray(a); a = np.where(g > 0.42, 1.0, 0.0).astype(np.float32) * 0.92 + g * 0.08
    if 'radial' in fx: a = radial(a, math.exp(-lf / 6))
    return a


def make_shots(cfg):
    P = cfg['plan']; END = cfg['end']; shots = []
    for i, p in enumerate(P):
        s = dict(p); s['t0'] = p['t']; s['t1'] = P[i + 1]['t'] if i + 1 < len(P) else END; shots.append(s)
    return shots


def render_frame(cfg, f, seqs, paths):
    shots, CF, END = cfg['shots'], cfg['cf'], cfg['end']
    t = f / FPS; i = sum(1 for c in CF if c <= f); s = shots[i]
    start_f = CF[i - 1] if i else 0; end_f = CF[i] if i < len(CF) else int(END * FPS)
    lf = f - start_f; lt = lf / FPS; dur = (end_f - start_f) / FPS
    if i not in seqs:
        for q in seqs.values():
            for r in (q if isinstance(q, list) else [q]): r.close()
        seqs.clear()
        if s['mode'] == 'split': seqs[i] = [Reader(p, W, 860) for p in paths[i]]
        elif s['mode'] != 'black': seqs[i] = Reader(paths[i], *size_for(cfg))
    grade = lambda x: look(x, cfg.get('warm', 0.0), cfg.get('sat', 1.12))
    if s['mode'] == 'black':
        a = np.zeros((H, W, 3), np.float32)
    elif s['mode'] == 'split':
        a = np.zeros((H, W, 3), np.float32); m = s.get('sub_mode', 'slow')
        for k, r in enumerate(seqs[i]):
            fr = grade(frame_for(r, m, lt, dur))
            fr = zoom(fr, 1.0 + 0.04 * lf / max(1, end_f - start_f))
            y0 = 40 + k * 1020; a[y0:y0 + 860] = fr
            off = int(W * (1 - ease(lt / 0.35)) * (1 if k == 0 else -1))         # halves slide in from both sides
            if off: a[y0:y0 + 860] = np.roll(a[y0:y0 + 860], off, 1)
        if lf == 0: a = flash(a, 0.5)
    else:
        fr = grade(frame_for(seqs[i], s['mode'], lt, dur))
        z = 1.0 + 0.035 * lf / max(1, end_f - start_f)
        if i in cfg.get('punch', ()) or i in cfg.get('swing', ()): z += 0.08 * dec(lt, 0.09)
        fr = zoom(fr, z)
        fr = shot_fx(fr, cfg.get('fx', {}).get(i, ()), lf)
        if i in cfg.get('punch', ()) and lf < 6:
            fr = np.roll(fr, int(14 * dec(lt, 0.04) * (1 if f % 2 else -1)), 1); fr = chroma(fr, 8 * dec(lt, 0.06))
        if cfg.get('pre_fx'): fr = cfg['pre_fx'](fr, i, t, lt)
        if cfg['layout'] == 'square':
            a = np.zeros((H, W, 3), np.float32); a[SQ_Y:SQ_Y + W] = fr
        elif cfg['layout'] == 'broadcast':                      # 16:9 'TV window' on a designed background
            a = cfg['bg'].copy(); y = cfg.get('win_y', 560); a[y:y + 608] = fr
        elif cfg['layout'] == 'tall':                           # 3:4 picture (much less crop than 9:16) over its own blur
            ph = cfg.get('pic_h', 1440); y = (H - ph) // 2     # pic_h=810: 4:3 = 1:1 from a 2.39:1 1080p film
            sm = Image.fromarray((np.clip(fr, 0, 1) * 255).astype(np.uint8)).resize((45, max(20, 80 * ph // 1440)), Image.BILINEAR)
            sm = sm.filter(ImageFilter.GaussianBlur(3)).resize((W, H), Image.BILINEAR)
            a = np.asarray(sm).astype(np.float32) / 255 * cfg.get('bg_dim', 0.5); a[y:y + ph] = fr
        elif cfg['layout'] == 'window':                         # sharp 16:9 window (no upscale) over its own blur
            y = cfg.get('win_y', (H - 608) // 2)
            sm = Image.fromarray((np.clip(fr[:, 351:729], 0, 1) * 255).astype(np.uint8)).resize((54, 96), Image.BILINEAR)
            sm = sm.filter(ImageFilter.GaussianBlur(3)).resize((W, H), Image.BILINEAR)
            a = np.asarray(sm).astype(np.float32) / 255 * 0.42 if cfg.get('win_blur', True) else np.zeros((H, W, 3), np.float32)
            a[y:y + 608] = fr
            if cfg.get('win_rule', True): a[y - 3:y] = 1.0; a[y + 608:y + 611] = 1.0
        elif cfg['layout'] == 'card':
            fr = fr * CARD_VIG; bg = background(fr)
            if i in cfg.get('swing', ()) and lt < 0.3:
                k = 1 - ease(lt / 0.3); a = place(bg, fr, ang=-38 * k, scale=1 - 0.12 * k)
            else:
                a = place(bg, fr)
        else:
            a = fr
        if i in cfg.get('drop', ()): a = flash(a, 1.0 * dec(lt, 0.07))
        elif lf == 0 and i and cfg.get('cut_flash', True): a = flash(a, 0.22)
        elif lf == 1 and i and cfg.get('cut_flash', True): a = flash(a, 0.08)
    tcy = cfg.get('text_cy', CY + CH // 2)
    for s0, s1, txt in cfg['text']:
        if s0 <= t < s1:
            k = ease((t - s0) / 0.07) * (1 - ease((t - (s1 - 0.06)) / 0.06)); dy = 40 * (1 - ease((t - s0) / 0.12))
            a = put(a, txt, k, size=170 if '|' not in txt else 150, cy=tcy, dy=dy)
    if cfg.get('overlay'): a = cfg['overlay'](a, f, t, i, lt)
    if s.get('label'):
        a = put(a, s['label'], ease(lt / 0.06), font=ORB, size=cfg.get('label_size', 60), cy=cfg.get('label_cy', CY - 70))
    if t > END - 0.5: a = a * (1 - ease((t - (END - 0.5)) / 0.5))
    v = cfg.get('vig', 1.0); a = a * (1 - (1 - VIG) * v) + GRAIN[f % 4] * cfg.get('grain', 0.3) * 0.25
    return np.clip(a, 0, 1)


def check(cfg):
    """One take per shot (moves src to a clean span) and no take used twice."""
    takes = []; bad = []
    for s in cfg['shots']:
        dur = s['t1'] - s['t0']
        if s['mode'] == 'black': continue
        parts = s['parts'] if s['mode'] == 'split' else [(s['file'], s['src'], s['cx'])]
        m = s.get('sub_mode', 'slow') if s['mode'] == 'split' else s['mode']
        newparts = []
        for f, src, cx in parts:
            p = os.path.join(cfg['srcdir'], f)
            try:
                src0 = src; src = clean_span(p, src, src_needed(m, dur) + cfg.get('pad', 0.15))
                if abs(src - src0) > 0.01:      # the action timing was planned on src0 - say so
                    print(f"WARNING shot {cfg['shots'].index(s)} (t={s['t0']:.3f}): src moved {src0:.2f} -> {src:.2f}")
            except ValueError as e:
                bad.append(f"shot {cfg['shots'].index(s)} (t={s['t0']:.3f}, {m}, {dur:.2f}s): {e}"); continue
            if not s.get('jump'):               # jump=True: a deliberate jump cut later in the same take
                takes.append((f, sum(1 for x in union_cuts(p) if x <= src + 0.02)))
            newparts.append((f, src, cx))
        if not newparts: continue
        if s['mode'] == 'split': s['parts'] = newparts
        else: s['src'] = newparts[0][1]
    assert not bad, 'unclean shots:\n' + '\n'.join(bad)
    dup = [t for t in set(takes) if takes.count(t) > 1]
    assert not dup, f'repeated take(s): {dup}'


def measure(cfg):
    from beatsync import video_cuts
    vc = video_cuts(cfg['out'], FPS); plan = [c / FPS for c in cfg['cf']]
    errs = [(min(vc, key=lambda c: abs(c - p)) - t) * 1000 for p, t in zip(plan, [s['t'] for s in cfg['plan'][1:]])]
    stray = [round(c, 3) for c in vc if min(abs(c - p) for p in plan) > 0.04]
    print(f"cuts {len(plan)} | err ms min {min(errs):.0f} max {max(errs):.0f} | stray {stray}")
    return errs, stray


def run(cfg, argv):
    cfg['shots'] = make_shots(cfg); cfg['cf'] = cut_frames([p['t'] for p in cfg['plan'][1:]])
    check(cfg)
    if len(argv) > 1 and argv[1] == 'check':
        print('check ok:', len(cfg['shots']), 'shots'); return
    paths = prep(cfg); seqs = {}
    if len(argv) > 1 and argv[1] == 'measure':
        measure(cfg); return
    if len(argv) > 1:
        for ts in argv[1:]:
            f0 = int(round(float(ts) * FPS)); seqs = {}; i = sum(1 for c in cfg['cf'] if c <= f0)
            for f in range(cfg['cf'][i - 1] if i else 0, f0 + 1): a = render_frame(cfg, f, seqs, paths)
            Image.fromarray((a * 255).astype(np.uint8)).save(os.path.join(ROOT, 'out', f"{cfg['name']}_{float(ts):.3f}.jpg"))
        return
    tmp = cfg['out'] + '.v.mp4'
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS),
                          '-i', '-', '-c:v', 'libx264', '-preset', 'medium', '-crf', str(cfg.get('crf', 17)), '-pix_fmt', 'yuv420p', tmp], stdin=subprocess.PIPE)
    for f in range(int(cfg['end'] * FPS)):
        p.stdin.write((render_frame(cfg, f, seqs, paths) * 255).astype(np.uint8).tobytes())
        if f % 240 == 0: print(f, flush=True)
    p.stdin.close(); p.wait()
    off = cfg.get('song_offset', 0.0); END = cfg['end']
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', tmp, '-ss', f'{off:.3f}', '-i', cfg['song'], '-map', '0:v', '-map', '1:a',
                    '-c:v', 'copy', '-af', f'apad,afade=t=out:st={END - 0.6}:d=0.6', '-c:a', 'aac', '-b:a', '256k',
                    '-t', str(END), '-movflags', '+faststart', cfg['out']], check=True)
    os.remove(tmp); print('done', cfg['out']); measure(cfg)
