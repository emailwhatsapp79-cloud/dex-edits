"""Edit J - F1. Direction: "20 years old. One race from history." Kimi Antonelli's 2026: the wins (intro),
Monza from P19 to P1 (the drop), the celebrations, then Austin - where he can clinch the title.
Song: v22 F1 sound (130 BPM, drop 7.514 s). Official F1 footage is 720p, so every shot sits in a 4:5 card
(1080x1350, ~1.9x upscale + sharpening) over a blurred fill; the card swings in in 3D on each section start."""
import os, sys, math, json, subprocess
from concurrent.futures import ThreadPoolExecutor
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
sys.path.insert(0, os.path.dirname(__file__))
import velocity
from velocity import frame_for, cut_frames, src_needed, clean_span, W, H, FPS, IFPS
_a = sys.argv; sys.argv = [sys.argv[0]]
from edit_c_justdance import flash, chroma, zoom, gblur, dec, ease, VIG, GRAIN, ROOT
sys.argv = _a

SRC = os.path.join(ROOT, 'src_f1')
SONG = os.path.join(ROOT, 'songs', 'named', '22_just_keep_watching_f1.mp3')
OUT = os.path.join(ROOT, 'out', 'edit_J_antonelli.mp4')
TMP = os.path.join(ROOT, 'tmp_j')
CW, CH, CY = 1080, 1350, 300                      # card size and top y
SW, SH = 1280, 720                                # source size
END = 22.9

# source takes: union of both detectors (race footage has soft cuts the scene detector misses, and vice versa)
_det = {}
def union_cuts(path):
    if path not in _det:
        cs = []
        for d in ('hist', 'scene'):
            velocity.DETECTOR = d; cs += velocity._source_cuts_orig(path)
        cs = sorted(cs); _det[path] = [c for i, c in enumerate(cs) if i == 0 or c - cs[i - 1] > 0.06]
    return _det[path]
velocity._source_cuts_orig = velocity.source_cuts
velocity.source_cuts = union_cuts

# (cut time = exact drum hit, file, src, cx, mode, race label)
PLAN = [
    (0.000, 'monza', 0.80, 0.50, 'real', 'MONZA'),       # hook: home win, chequered flag
    (0.838, 'china', 5.40, 0.52, 'real', 'CHINA'),
    (1.759, 'japan', 5.20, 0.55, 'real', 'JAPAN'),
    (2.665, 'miami', 2.20, 0.50, 'real', 'MIAMI'),
    (3.612, 'canada', 3.80, 0.50, 'real', 'CANADA'),
    (4.529, 'monaco', 1.40, 0.55, 'real', 'MONACO'),
    (5.100, 'spain', 0.30, 0.40, 'real', 'SPAIN'),
    (6.127, 'spain', 4.60, 0.50, 'real', 'SPAIN'),
    (7.084, None, 0, 0, 'black', ''),                    # the gap before the drop: "8 WINS."
    (7.514, 'monza_hl', 216.2, 0.50, 'real', ''),        # DROP - onboard, Monza
    (8.440, 'monza_hl', 7.0, 0.50, 'real', ''),          # the start
    (9.360, 'monza_hl', 146.2, 0.40, 'real', ''),
    (10.286, 'monza_hl', 229.0, 0.50, 'real', ''),
    (10.748, 'monza_hl', 237.0, 0.55, 'real', ''),
    (11.207, 'monza_hl', 280.2, 0.55, 'real', ''),
    (11.664, 'monza_hl', 312.0, 0.50, 'real', ''),
    (12.125, 'monza_hl', 400.5, 0.50, 'real', ''),
    (12.594, 'monza_hl', 415.5, 0.55, 'real', ''),       # the move on Russell
    (13.053, 'monza_hl', 437.3, 0.40, 'real', ''),
    (13.517, 'monza_hl', 430.0, 0.60, 'real', ''),
    (13.952, 'monza_hl', 452.0, 0.50, 'slow', ''),       # leading to the flag
    (14.902, 'monza_hl', 468.5, 0.50, 'real', ''),       # the tifosi
    (15.817, 'monza', 3.00, 0.55, 'real', ''),
    (16.745, 'china', 9.00, 0.50, 'real', ''),
    (17.663, 'japan', 11.60, 0.50, 'real', ''),
    (18.591, 'miami', 4.30, 0.50, 'real', ''),
    (19.512, 'spain', 6.20, 0.45, 'real', ''),
    (20.453, 'monaco', 3.00, 0.50, 'hero', ''),          # breath: onboard, slow
    (21.363, 'canada', 6.30, 0.50, 'real', ''),
    (21.825, 'china', 15.30, 0.50, 'real', ''),
    (22.285, 'monza', 8.15, 0.50, 'slow', ''),      # onboard: the Italian helmet
]
T0 = [p[0] for p in PLAN]
CF = cut_frames(T0[1:])
SHOTS = [dict(file=p[1], src=p[2], cx=p[3], mode=p[4], label=p[5], t0=T0[i],
              t1=(T0[i + 1] if i + 1 < len(T0) else END)) for i, p in enumerate(PLAN)]
SWING = {9, 21, 28}                                  # 3D card entrance on section starts
PUNCH = set(range(10, 20))                           # drop section: punch + shake on every cut

TEXT = [(0.0, 1.759, '20 YEARS OLD.'), (7.084, 7.514, '8 WINS.'), (7.514, 8.44, 'MONZA.'),
        (9.36, 11.207, 'STARTED P19.'), (13.952, 14.902, 'P19 → P1'), (14.902, 15.817, 'AT HOME.'),
        (17.663, 20.453, '102 POINTS|CLEAR.'), (20.453, 21.363, 'NEXT:|AUSTIN.'),
        (21.363, END, 'ONE RACE|FROM HISTORY.')]


# --------------------------------------------------------------- footage
def prep_one(i):
    sh = SHOTS[i]
    if sh['mode'] == 'black': return None
    path = os.path.join(SRC, sh['file'] + '.mp4')
    need = src_needed(sh['mode'], sh['t1'] - sh['t0']) + 0.15
    new = clean_span(path, sh['src'], need)
    if abs(new - sh['src']) > 1e-3: print(f"shot {i}: src {sh['src']:.2f} -> {new:.2f}", flush=True); sh['src'] = new
    out = os.path.join(TMP, f"j{i:02d}_{sh['file']}_{sh['src']:.2f}_{sh['mode']}.mp4")
    if os.path.exists(out): return out
    cw = int(SH * CW / CH) // 2 * 2; x = int((SW - cw) * sh['cx'])
    vf = (f"crop={cw}:{SH}:{x}:0,scale={CW}:{CH}:flags=lanczos,unsharp=5:5:0.9:3:3:0.4,"
          f"minterpolate=fps={IFPS}:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1")
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(sh['src']), '-t', f'{need:.3f}', '-i', path, '-vf', vf,
                    '-an', '-c:v', 'libx264', '-crf', '13', '-preset', 'veryfast', out], check=True)
    return out


class CSeq:
    def __init__(self, path):
        self.p = subprocess.Popen(['ffmpeg', '-v', 'error', '-i', path, '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'],
                                  stdout=subprocess.PIPE)
        self.buf = []; self.idx = -1

    def get(self, i):
        while self.idx < i:
            b = self.p.stdout.read(CW * CH * 3)
            if len(b) < CW * CH * 3: break
            self.idx += 1; self.buf.append(np.frombuffer(b, np.uint8).reshape(CH, CW, 3))
            if len(self.buf) > 4: self.buf.pop(0)
        k = max(0, len(self.buf) - 1 - max(0, self.idx - i))
        return self.buf[k] if self.buf else np.zeros((CH, CW, 3), np.uint8)

    def close(self): self.p.kill()


# --------------------------------------------------------------- look
def look(a):
    lum = a @ np.array([0.299, 0.587, 0.114], np.float32)
    a = lum[..., None] + (a - lum[..., None]) * 1.12
    a = np.clip((a - 0.025) * 1.07, 0, 1); s = a * a * (3 - 2 * a); a = s * 0.4 + a * 0.6
    l = lum[..., None]
    return np.clip(a + (1 - l) * np.array([-0.015, 0.0, 0.025]) + l * np.array([0.015, 0.005, -0.01]), 0, 1)


_yy, _xx = np.mgrid[0:CH, 0:CW].astype(np.float32)
CARD_VIG = (1 - 0.35 * np.clip(np.sqrt(((_xx - CW / 2) / (CW / 2)) ** 2 + ((_yy - CH / 2) / (CH / 2)) ** 2) - 0.6, 0, 1))[..., None]


def background(card):
    im = Image.fromarray((card * 255).astype(np.uint8)).resize((96, 120), Image.BILINEAR).filter(ImageFilter.GaussianBlur(5))
    bw = int(H * CW / CH)
    im = im.resize((bw, H), Image.BILINEAR).crop(((bw - W) // 2, 0, (bw - W) // 2 + W, H))
    return np.asarray(im).astype(np.float32) / 255 * 0.42


def _persp_coeffs(src, dst):
    """PIL PERSPECTIVE coefficients mapping output (dst) points back to input (src) points."""
    A, b = [], []
    for (x, y), (u, v) in zip(dst, src):
        A += [[x, y, 1, 0, 0, 0, -u * x, -u * y], [0, 0, 0, x, y, 1, -v * x, -v * y]]; b += [u, v]
    return np.linalg.solve(np.array(A, np.float64), np.array(b, np.float64)).tolist()


def place(bg, card, ang=0.0, scale=1.0):
    """Composite the card onto the background, rotated `ang` degrees about its vertical axis (3D swing)."""
    out = bg.copy()
    cx, cy = W / 2, CY + CH / 2
    hw, hh = CW / 2 * scale, CH / 2 * scale
    if abs(ang) < 0.3 and abs(scale - 1) < 1e-3:
        sh = np.zeros((H, W), np.float32); sh[CY + 18:CY + CH + 18, 12:W - 12] = 1
        sh = np.asarray(Image.fromarray((sh * 255).astype(np.uint8)).resize((W // 8, H // 8)).filter(ImageFilter.GaussianBlur(4))
                        .resize((W, H), Image.BILINEAR)).astype(np.float32)[..., None] / 255
        out = out * (1 - 0.6 * sh)
        out[CY:CY + CH] = card; return out
    r = math.radians(ang); d = 1800.0                                   # camera distance
    pts = []
    for sx, sy in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
        x3, z3 = sx * hw * math.cos(r), sx * hw * math.sin(r)
        k = d / (d + z3); pts.append((cx + x3 * k, cy + sy * hh * k))
    co = _persp_coeffs([(0, 0), (CW, 0), (CW, CH), (0, CH)], pts)
    im = Image.fromarray((card * 255).astype(np.uint8)).convert('RGBA')
    warped = im.transform((W, H), Image.PERSPECTIVE, co, Image.BILINEAR)
    wa = np.asarray(warped).astype(np.float32) / 255
    m = wa[..., 3:4]
    return out * (1 - m) + wa[..., :3] * m


# --------------------------------------------------------------- text
ANTON = os.path.join(ROOT, 'fonts', 'Anton.ttf'); ORB = os.path.join(ROOT, 'fonts', 'Orbitron.ttf')
_tc = {}
def text_layer(text, font, size, cy, maxw=960, track=0):
    key = (text, font, size, cy)
    if key in _tc: return _tc[key]
    lines = text.split('|')
    f = ImageFont.truetype(font, size)
    if font == ORB:
        try: f.set_variation_by_axes([800])
        except Exception: pass
    while max(f.getbbox(l)[2] for l in lines) > maxw:
        size -= 6; f = ImageFont.truetype(font, size)
    m = Image.new('L', (W, H), 0); d = ImageDraw.Draw(m); lh = int(size * 1.08); y0 = cy - lh * len(lines) // 2
    for i, l in enumerate(lines):
        bb = f.getbbox(l); d.text(((W - bb[2]) / 2, y0 + i * lh - bb[1] // 2), l, font=f, fill=255)
    a = np.asarray(m).astype(np.float32) / 255
    sh = np.asarray(m.filter(ImageFilter.GaussianBlur(16))).astype(np.float32) / 255
    _tc[key] = (a[..., None], np.clip(sh * 1.4, 0, 1)[..., None])
    return _tc[key]


def put(a, text, k, font=ANTON, size=150, cy=CY + CH // 2, dy=0):
    if k <= 0.01: return a
    al, sh = text_layer(text, font, size, cy)
    if dy: al = np.roll(al, int(dy), 0); sh = np.roll(sh, int(dy), 0)
    a = a * (1 - sh * 0.55 * k)
    return a * (1 - al * k) + al * k


# --------------------------------------------------------------- render
def render(f, seqs, paths):
    t = f / FPS
    i = sum(1 for c in CF if c <= f)
    s = SHOTS[i]; start_f = CF[i - 1] if i else 0; end_f = CF[i] if i < len(CF) else int(END * FPS)
    lf = f - start_f; lt = lf / FPS
    if s['mode'] == 'black':
        a = np.zeros((H, W, 3), np.float32)
    else:
        if i not in seqs:
            for q in seqs.values(): q.close()
            seqs.clear(); seqs[i] = CSeq(paths[i])
        card = look(frame_for(seqs[i], s['mode'], lt, (end_f - start_f) / FPS))
        z = 1.0 + 0.035 * lf / max(1, end_f - start_f)                          # slow push inside every shot
        if i in PUNCH or i in SWING: z += 0.08 * dec(lt, 0.09)                  # punch on the hit
        card = zoom(card, z)
        if i in PUNCH and lf < 6:
            card = np.roll(card, int(14 * dec(lt, 0.04) * (1 if f % 2 else -1)), 1)
            card = chroma(card, 8 * dec(lt, 0.06))
        card = card * CARD_VIG
        bg = background(card)
        if i in SWING and lt < 0.3:
            k = 1 - ease(lt / 0.3)
            a = place(bg, card, ang=-38 * k, scale=1 - 0.12 * k)
        else:
            a = place(bg, card)
        if i == 9: a = flash(a, 1.0 * dec(lt, 0.07))                          # the drop
        elif lf == 0 and i: a = flash(a, 0.22)                                   # every cut flashes on the hit frame
        elif lf == 1 and i: a = flash(a, 0.08)
    for s0, s1, txt in TEXT:
        if s0 <= t < s1:
            k = ease((t - s0) / 0.07) * (1 - ease((t - (s1 - 0.06)) / 0.06))
            dy = 40 * (1 - ease((t - s0) / 0.12))
            a = put(a, txt, k, size=170 if '|' not in txt else 150, dy=dy)
    if s['label'] and s['mode'] != 'black':                                     # race name above the card
        a = put(a, s['label'], ease(lt / 0.06), font=ORB, size=64, cy=CY - 70)
    if t > END - 0.5: a = a * (1 - ease((t - (END - 0.5)) / 0.5))
    a = a * VIG + GRAIN[f % 4] * 0.3
    return np.clip(a, 0, 1)


if __name__ == '__main__':
    os.makedirs(TMP, exist_ok=True)
    for sh in SHOTS:                                                             # one source take per shot
        if sh['mode'] == 'black': continue
        p = os.path.join(SRC, sh['file'] + '.mp4')
        sh['src'] = clean_span(p, sh['src'], src_needed(sh['mode'], sh['t1'] - sh['t0']) + 0.15)
    takes = [(sh['file'], sum(1 for x in union_cuts(os.path.join(SRC, sh['file'] + '.mp4')) if x <= sh['src'] + 0.02))
             for sh in SHOTS if sh['mode'] != 'black']
    assert len(set(takes)) == len(takes), f'repeated take: {takes}'
    with ThreadPoolExecutor(4) as ex: paths = list(ex.map(prep_one, range(len(SHOTS))))
    seqs = {}
    if len(sys.argv) > 1:
        for ts in sys.argv[1:]:
            f0 = int(round(float(ts) * FPS)); seqs = {}; i = sum(1 for c in CF if c <= f0)
            for f in range(CF[i - 1] if i else 0, f0 + 1): a = render(f, seqs, paths)
            Image.fromarray((a * 255).astype(np.uint8)).save(os.path.join(ROOT, 'out', f'J_{float(ts):.3f}.jpg'))
        sys.exit()
    tmp = OUT + '.v.mp4'
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS),
                          '-i', '-', '-c:v', 'libx264', '-preset', 'medium', '-crf', '17', '-pix_fmt', 'yuv420p', tmp], stdin=subprocess.PIPE)
    for f in range(int(END * FPS)):
        p.stdin.write((render(f, seqs, paths) * 255).astype(np.uint8).tobytes())
        if f % 240 == 0: print(f, flush=True)
    p.stdin.close(); p.wait()
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', tmp, '-i', SONG, '-map', '0:v', '-map', '1:a', '-c:v', 'copy',
                    '-af', f'apad,afade=t=out:st={END - 0.5}:d=0.5', '-c:a', 'aac', '-b:a', '256k', '-t', str(END),
                    '-movflags', '+faststart', OUT], check=True)
    os.remove(tmp); print('done', OUT)
