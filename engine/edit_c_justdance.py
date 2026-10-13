"""Edit C - 'Just Dance' lyric edit with real car footage.
Structure learned from the reference: calm intro where each sung word appears on its own (text behind
the car), beat comes in at 4.88s -> cuts on words, white word cards, picture-in-picture, split screens,
'can't see straight' gets the heavy treatment, calm 'keep it cool', end on 'just' so it loops."""
import os, subprocess, sys, math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CL = os.path.join(ROOT, 'clips', 'hd')
SONG = os.path.join(ROOT, 'songs', '56214fa7-ssstik.io_1791867553638.mp3')
OUT = os.path.join(ROOT, 'out', 'edit_C_just_dance.mp4')
W, H, FPS = 1080, 1920, 30
END = 23.9

# --------------------------------------------------------------- footage reader
class Clip:
    """Streams frames of a clip segment at FPS, cover-cropped to (w,h) around horizontal centre cx."""
    def __init__(self, name, src_in, w=W, h=H, cx=0.5, speed=1.0, cy=0.5):
        self.args = (name, src_in, w, h, cx, speed, cy)
        self.p = None

    def frame(self):
        name, src_in, w, h, cx, speed, cy = self.args
        if self.p is None:
            path = os.path.join(CL, name + '.mp4')
            sw, sh = map(int, subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v', '-show_entries',
                       'stream=width,height', '-of', 'csv=p=0', path], capture_output=True, text=True).stdout.split(','))
            s = max(w / sw, h / sh)
            cw, ch = int(round(w / s)), int(round(h / s))
            x0 = int((sw - cw) * cx); y0 = int((sh - ch) * cy)
            vf = (f'setpts=PTS/{speed},fps={FPS},crop={cw}:{ch}:{x0}:{y0},scale={w}:{h}:flags=lanczos,'
                  f'unsharp=5:5:0.6')
            self.p = subprocess.Popen(['ffmpeg', '-v', 'error', '-ss', str(src_in), '-i', path, '-vf', vf,
                                       '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
            self.last = None
        b = self.p.stdout.read(w * h * 3)
        if len(b) == w * h * 3:
            self.last = np.frombuffer(b, np.uint8).reshape(h, w, 3).astype(np.float32) / 255
        return self.last


# --------------------------------------------------------------- look
def grade(a, warm=0.0):
    """Moody teal look of the reference: crushed blacks, slightly desaturated, teal shadows."""
    lum = a @ np.array([0.299, 0.587, 0.114], np.float32)
    a = lum[..., None] + (a - lum[..., None]) * 0.9
    a = np.clip((a - 0.03) * 1.08, 0, 1)
    s = a * a * (3 - 2 * a)
    a = s * 0.5 + a * 0.5
    l = lum[..., None]
    a = a + (1 - l) * np.array([-0.03, 0.012, 0.035]) + l * np.array([0.02 + warm, 0.006, -0.02])
    return np.clip(a, 0, 1)

_y, _x = np.mgrid[0:H, 0:W].astype(np.float32)
VIG = (1 - 0.5 * np.clip(np.sqrt(((_x - W / 2) / (W / 2)) ** 2 + ((_y - H / 2) / (H / 2)) ** 2) - 0.45, 0, 1) ** 1.5)[..., None]
GRAIN = [np.random.default_rng(i).normal(0, 0.022, (H, W, 1)).astype(np.float32) for i in range(4)]


def flash(a, k, c=1.0):
    return a + (c - a) * min(max(k, 0), 1) if k > 0.003 else a


def chroma(a, px):
    px = int(px)
    if px < 1: return a
    o = a.copy(); o[..., 0] = np.roll(a[..., 0], px, 1); o[..., 2] = np.roll(a[..., 2], -px, 1); return o


def zoom(a, z, cx=0.5, cy=0.5):
    z = max(z, 1.0)
    if z - 1 < 0.002: return a
    h, w = a.shape[:2]; im = Image.fromarray((a * 255).astype(np.uint8))
    vw, vh = w / z, h / z; x0, y0 = (w - vw) * cx, (h - vh) * cy
    return np.asarray(im.resize((w, h), Image.BILINEAR, box=(x0, y0, x0 + vw, y0 + vh))).astype(np.float32) / 255


def gblur(a, r):
    if r < 0.5: return a
    h, w = a.shape[:2]; im = Image.fromarray((a * 255).astype(np.uint8))
    im = im.resize((w // 4, h // 4)).filter(ImageFilter.GaussianBlur(r / 4)).resize((w, h), Image.BILINEAR)
    return np.asarray(im).astype(np.float32) / 255


def dec(t, tau):
    return math.exp(-t / tau) if t >= 0 else 0.0


def ease(x):
    x = min(max(x, 0), 1); return 1 - (1 - x) ** 3


# --------------------------------------------------------------- text
FONT_PATH = os.path.join(ROOT, 'fonts', 'Archivo.ttf')
_fc = {}
def fnt(size):
    if size not in _fc:
        f = ImageFont.truetype(FONT_PATH, size); f.set_variation_by_axes([900, 125]); _fc[size] = f
    return _fc[size]

_tc = {}
def word_layer(text, card=False, maxw=900):
    """RGBA full-frame layer with the word centred (soft shadow, slight vertical gradient)."""
    key = (text, card)
    if key in _tc: return _tc[key]
    size = 170
    while fnt(size).getbbox(text)[2] > maxw and size > 60: size -= 6
    f = fnt(size); bb = f.getbbox(text); tw, th = bb[2] - bb[0], bb[3] - bb[1]
    x, y = (W - tw) / 2 - bb[0], (H - th) / 2 - bb[1]
    m = Image.new('L', (W, H), 0); ImageDraw.Draw(m).text((x, y), text, font=f, fill=255)
    m = np.asarray(m).astype(np.float32) / 255
    if card:
        bx0, by0, bx1, by1 = (W - tw) / 2 - 60, (H - th) / 2 - 55, (W + tw) / 2 + 60, (H + th) / 2 + 55
        box = np.zeros((H, W), np.float32); box[int(by0):int(by1), int(bx0):int(bx1)] = 1
        rgb = np.ones((H, W, 3), np.float32) * (1 - m[..., None])          # white card, black letters
        alpha = np.clip(box * 0.95, 0, 1)
    else:
        sh = np.asarray(Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(14))).astype(np.float32) / 255
        g = np.linspace(1.0, 0.82, H)[:, None]
        rgb = np.ones((H, W, 3), np.float32) * g[..., None]
        alpha_t = m
        alpha = np.clip(m + sh * 0.55, 0, 1)
        rgb = np.where(alpha_t[..., None] > 0.01, rgb, 0)                  # shadow is black
    _tc[key] = (rgb, alpha[..., None])
    return _tc[key]


def put_text(a, text, lt, card=False, behind_mask=None, ty=0.0):
    rgb, al = word_layer(text, card)
    if ty:
        rgb, al = np.roll(rgb, int(ty * H), 0), np.roll(al, int(ty * H), 0)
    pop = 1 + 0.12 * (1 - ease(lt / 0.12))
    if pop > 1.003:
        im = Image.fromarray(np.dstack([rgb, al]).__mul__(255).astype(np.uint8), 'RGBA')
        nw, nh = int(W * pop), int(H * pop)
        im = im.resize((nw, nh), Image.BILINEAR).crop(((nw - W) // 2, (nh - H) // 2, (nw - W) // 2 + W, (nh - H) // 2 + H))
        arr = np.asarray(im).astype(np.float32) / 255; rgb, al = arr[..., :3], arr[..., 3:]
    out = a * (1 - al) + rgb * al
    if behind_mask is not None:
        out = out * (1 - behind_mask) + a * behind_mask
    return out


# --------------------------------------------------------------- car masks (text behind the car)
_seg = None
def car_mask(a):
    global _seg
    from rembg import new_session, remove
    if _seg is None: _seg = new_session('isnet-general-use')
    small = Image.fromarray((a * 255).astype(np.uint8)).resize((540, 960))
    m = remove(small, session=_seg, only_mask=True).resize((W, H), Image.BILINEAR)
    m = np.asarray(m).astype(np.float32) / 255
    return np.clip((m - 0.25) / 0.5, 0, 1)[..., None]


# --------------------------------------------------------------- lyrics (start, text, card?) - from word timestamps
WORDS = [(0.0, 'WHERE'), (0.34, 'ARE'), (0.68, 'MY'), (0.88, 'KEYS?'), (1.46, 'I'), (1.54, 'LOST'), (1.84, 'MY'),
         (2.10, 'PHONE'), (2.82, 'OH'), (3.54, 'NO'), (4.70, None), (5.50, "WHAT'S", 1), (6.22, 'GOING'), (6.94, 'ON'),
         (8.30, None), (8.48, 'ON'), (8.80, 'THE', 1), (8.94, 'FLOOR?'), (9.74, 'I'), (9.86, 'LOVE'), (10.16, 'THIS'),
         (10.50, 'RECORD,', 1), (11.20, 'BABY'), (11.46, 'BUT'), (12.02, 'I'), (12.30, "CAN'T"), (12.70, 'SEE'),
         (12.80, 'STRAIGHT'), (13.16, 'ANYMORE'), (14.00, 'KEEP'), (15.06, 'IT'), (16.22, 'COOL'), (16.82, "WHAT'S"),
         (17.42, 'THE'), (17.58, 'NAME'), (18.00, 'OF'), (18.32, 'THIS'), (18.48, 'CLUB?', 1), (19.20, 'I'),
         (19.32, "CAN'T"), (19.78, 'REMEMBER'), (20.30, 'BUT'), (20.98, "IT'S"), (21.34, 'ALRIGHT,'), (21.92, 'ALRIGHT'),
         (22.56, 'JUST')]
CARD_T = 0.13


def lyric_at(t):
    cur = None
    for w in WORDS:
        if w[0] <= t: cur = w
    if cur is None or cur[1] is None: return None
    card = len(cur) > 2 and t - cur[0] < CARD_T
    return cur[1], t - cur[0], card


# --------------------------------------------------------------- shots: (start, end, kind, spec)
SHOTS = [
    (0.00, 0.88, 'full', dict(c=('mk35223', 1.0), behind=True, ty=-0.205)),
    (0.88, 1.46, 'full', dict(c=('keys', 1.2))),
    (1.46, 2.82, 'full', dict(c=('phone', 3.0))),
    (2.82, 4.88, 'full', dict(c=('wporsche', 7.2, 0.3), push=True, ty=-0.2)),
    (4.88, 5.50, 'full', dict(c=('mk53', 1.0, 0.45), hit=True)),
    (5.50, 6.22, 'full', dict(c=('gas', 2.0))),
    (6.22, 6.94, 'full', dict(c=('zx_lights', 0.3, 0.45))),
    (6.94, 7.87, 'full', dict(c=('neon', 0.5, 0.35))),
    (7.87, 8.48, 'pip', dict(bg=('neon', 1.43, 0.35), fg=('mk35231', 4.0))),
    (8.48, 9.74, 'full', dict(c=('pedal', 1.0), punch_at=[8.94])),
    (9.74, 10.50, 'diag', dict(a=('music', 2.0), b=('bop1', 4.0))),
    (10.50, 11.46, 'halves', dict(a=('bop1', 4.76, 0.62), b=('zx_rain', 3.0, 0.55))),
    (11.46, 12.80, 'dizzy', dict(c=('blurlights', 5.0))),
    (12.80, 14.00, 'quad', dict(q=[('gt3', 3.0), ('m4', 2.0), ('p911', 2.0), ('wporsche', 11.0)])),
    (14.00, 16.82, 'full', dict(c=('zx_lights', 3.0, 0.35, 0.5), calm=True)),
    (16.82, 18.00, 'full', dict(c=('vegas2', 1.0))),
    (18.00, 19.20, 'full', dict(c=('vegas', 2.0))),
    (19.20, 20.30, 'full', dict(c=('blurhead', 8.0), breathe=True)),
    (20.30, END, 'full', dict(c=('mk35223', 5.0), behind=True, outro=True, ty=-0.205)),
]


def mk(spec, w=W, h=H):
    name, src = spec[0], spec[1]
    cx = spec[2] if len(spec) > 2 else 0.5
    speed = spec[3] if len(spec) > 3 else 1.0
    return Clip(name, src, w, h, cx, speed)


def open_shot(s):
    k, sp = s[2], s[3]
    if k == 'full' or k == 'dizzy': return {'c': mk(sp['c'])}
    if k == 'pip': return {'bg': mk(sp['bg']), 'fg': mk(sp['fg'], 760, 1350)}
    if k == 'diag': return {'a': mk(sp['a']), 'b': mk(sp['b'])}
    if k == 'halves': return {'a': mk(sp['a'], W // 2, H), 'b': mk(sp['b'], W // 2, H)}
    if k == 'quad': return {f'q{i}': mk(q, W // 2, H // 2) for i, q in enumerate(sp['q'])}


DIAG = None
def render_shot(s, st, t):
    start, end, k, sp = s; lt, dur = t - start, end - start
    mask = None
    if k in ('full', 'dizzy'):
        a = grade(st['c'].frame())
        if sp.get('behind'): mask = car_mask(a)
        if sp.get('push'):
            a = zoom(a, 1.0 + 0.04 * lt / dur + 0.3 * ease((lt - (dur - 0.18)) / 0.18)); mask = None if lt > dur - 0.18 else mask
            if lt > dur - 0.18: a = gblur(a, 30 * ease((lt - (dur - 0.18)) / 0.18))
        if sp.get('hit'):
            a = zoom(a, 1 + 0.18 * dec(lt, 0.12)); a = flash(a, 0.9 * dec(lt, 0.1)); a = chroma(a, 14 * dec(lt, 0.1))
        if 'punch_at' in sp:
            for pt in sp['punch_at']:
                if t >= pt: a = zoom(a, 1 + 0.15 * dec(t - pt, 0.1))
        if k == 'dizzy':   # "can't see straight": double vision + colour split + wobble
            a = np.clip(a * 1.9 + 0.03, 0, 1)
            off = int(26 + 22 * math.sin(lt * 9))
            a = 0.6 * a + 0.4 * np.roll(a, off, 1)
            a = chroma(a, 10 + 6 * math.sin(lt * 13))
            a = zoom(a, 1.06 + 0.04 * math.sin(lt * 7), 0.5 + 0.03 * math.sin(lt * 5))
        if sp.get('breathe'):
            a = gblur(a, 10 + 9 * math.sin(lt * 6))
        if sp.get('outro') and t > END - 0.7:
            a = a * (1 - ease((t - (END - 0.7)) / 0.7))
    elif k == 'pip':
        a = grade(st['bg'].frame()) * 0.55
        a = gblur(a, 8)
        fg = grade(st['fg'].frame()); s_ = 0.82 + 0.18 * ease(lt / 0.2)
        im = Image.fromarray((fg * 255).astype(np.uint8)); fw, fh = int(760 * s_), int(1350 * s_)
        im = np.asarray(im.resize((fw, fh), Image.BILINEAR)).astype(np.float32) / 255
        x0, y0 = (W - fw) // 2, (H - fh) // 2
        a[y0 - 6:y0 + fh + 6, x0 - 6:x0 + fw + 6] = 1.0
        a[y0:y0 + fh, x0:x0 + fw] = im
        a = flash(a, 0.5 * dec(lt, 0.06))
    elif k == 'diag':
        A, B = grade(st['a'].frame()), grade(st['b'].frame())
        thresh = 0.3 + 0.5 * ease(lt / 0.25)                             # diagonal wipes across
        d = _x / W + (_y / H) * 0.6
        m = (d < thresh).astype(np.float32)[..., None]
        a = A * m + B * (1 - m)
        a[np.abs(d - thresh) < 0.004] = 1.0
    elif k == 'halves':
        a = np.concatenate([grade(st['a'].frame()), grade(st['b'].frame())], axis=1)
        a[:, W // 2 - 3:W // 2 + 3] = 1.0
        a = flash(a, 0.4 * dec(lt, 0.06))
    elif k == 'quad':
        q = [grade(st[f'q{i}'].frame()) for i in range(4)]
        n = 1 + min(3, int(lt / 0.12))                                       # panels pop in one by one
        q = [q[i] if i < n else q[i] * 0.0 for i in range(4)]
        a = np.concatenate([np.concatenate(q[:2], 1), np.concatenate(q[2:], 1)], 0)
        a[H // 2 - 3:H // 2 + 3] = 1.0; a[:, W // 2 - 3:W // 2 + 3] = 1.0
        a = zoom(a, 1.03 + 0.03 * math.sin(lt * 8))
    return a, mask


def render(f, states):
    t = f / FPS
    s = next(x for x in SHOTS if x[0] <= t < x[1])
    if id(s) not in states:
        for old in states.values():
            for c in old.values():
                if c.p: c.p.kill()
        states.clear(); states[id(s)] = open_shot(s)
    a, mask = render_shot(s, states[id(s)], t)
    ly = lyric_at(t)
    if ly:
        a = put_text(a, ly[0], ly[1], card=ly[2], behind_mask=mask if not ly[2] else None, ty=s[3].get('ty', 0.0))
    a = a * VIG + GRAIN[f % 4]
    return np.clip(a, 0, 1)


if __name__ == '__main__':
    states = {}
    if len(sys.argv) > 1:   # preview: render the requested times by running through from each shot start
        for ts in sys.argv[1:]:
            t = float(ts); states = {}
            s = next(x for x in SHOTS if x[0] <= t < x[1])
            for f in range(int(round(s[0] * FPS)), int(round(t * FPS)) + 1):
                a = render(f, states)
            Image.fromarray((a * 255).astype(np.uint8)).save(os.path.join(ROOT, 'out', f'C_{t:.2f}.jpg'))
        sys.exit()
    tmp = OUT + '.v.mp4'
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS),
                          '-i', '-', '-c:v', 'libx264', '-preset', 'slow', '-crf', '18', '-pix_fmt', 'yuv420p', tmp], stdin=subprocess.PIPE)
    n = int(END * FPS)
    for f in range(n):
        p.stdin.write((render(f, states) * 255).astype(np.uint8).tobytes())
        if f % 60 == 0: print(f, '/', n, flush=True)
    p.stdin.close(); p.wait()
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', tmp, '-i', SONG, '-map', '0:v', '-map', '1:a', '-c:v', 'copy',
                    '-c:a', 'aac', '-b:a', '256k', '-af', f'loudnorm=I=-11:TP=-1,afade=t=out:st={END - 0.7}:d=0.7',
                    '-t', str(END), '-movflags', '+faststart', OUT], check=True)
    os.remove(tmp); print('done', OUT)
