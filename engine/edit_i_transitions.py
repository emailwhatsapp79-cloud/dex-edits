"""Edit I - TRANSITION edit. Direction: "One car. One road. One day." The red Taycan GTS from midday sun
to golden hour to night. Every cut is a designed transition (zoom-through / whip / spin) whose swap frame
is the drum-hit frame; the drop is a hard flash cut. Song: 20 (malvini), 60 fps, Porsche 4K press film."""
import os, sys, json, math, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, os.path.dirname(__file__))
import velocity
from velocity import prep, Seq, frame_for, cut_frames, W, H, FPS
velocity.DETECTOR = 'scene'
_a = sys.argv; sys.argv = [sys.argv[0]]
from edit_c_justdance import flash, chroma, zoom, gblur, dec, ease, fnt, VIG, GRAIN, ROOT
sys.argv = _a
from beatsync import grid

SRC = os.path.join(ROOT, 'src_car')
FILM = 'p337658.mp4'
SONG = os.path.join(ROOT, 'songs', 'named', '20_mbappe_malvini_sound.mp3')
OUT = os.path.join(ROOT, 'out', 'edit_I_taycan_transitions.mp4')
G = [t for t, a in grid(SONG, duration=30)[0]]
snap = lambda t: min(G, key=lambda g: abs(g - t))

# (target cut time, src, cx, mode, transition INTO this shot)
PLAN = [                                   # every shot from a DIFFERENT take of the film (checked below)
    (0.00, 98.40, 0.50, 'real', None),     # hook: front, centred
    (1.31, 79.60, 0.55, 'real', 'zoom'),
    (2.53, 83.40, 0.50, 'real', 'whip'),
    (3.71, 86.60, 0.50, 'real', 'spin'),
    (4.67, 114.20, 0.50, 'real', 'zoom'),
    (5.90, 95.80, 0.50, 'real', 'whip'),
    (6.96, 69.00, 0.50, 'real', 'spin'),   # parked in the field
    (8.05, 122.10, 0.40, 'slow', 'zoom'),  # wheel - the build (slow-mo)
    (8.68, 122.90, 0.50, 'real', 'drop'),  # DROP: hard flash cut
    (9.59, 128.05, 0.55, 'real', 'whip'),
    (10.50, 129.50, 0.55, 'real', 'zoom'),
    (11.42, 132.60, 0.50, 'real', 'spin'),
    (12.42, 37.75, 0.50, 'real', 'whip'),  # with the driver in the field
    (13.41, 17.80, 0.50, 'real', 'zoom'),  # low sun on the track
    (14.49, 137.30, 0.45, 'real', 'spin'), # golden hour
    (15.38, 139.60, 0.55, 'real', 'whip'),
    (16.32, 146.90, 0.50, 'slow', 'zoom'), # nightfall
    (17.35, 143.66, 0.50, 'slow', 'whip'), # driver at night (slow-mo, clean part of the take)
    (18.31, 147.83, 0.50, 'hero', 'spin'), # headlights
    (19.39, 148.40, 0.50, 'hero', 'zoom'), # GTS dial at night (stops before the black frame)
    (20.30, 150.00, 0.50, 'slow', 'whip'),
]
END = 22.6
T0 = [0.0] + [snap(p[0]) for p in PLAN[1:]]
CF = cut_frames(T0[1:])
SHOTS = [dict(file=FILM, src=p[1], cx=p[2], mode=p[3], t0=T0[i], t1=(T0[i + 1] if i + 1 < len(T0) else END))
         for i, p in enumerate(PLAN)]
TR = 5                                                           # transition frames each side of the hit

TEXT = [(0.0, T0[1], 'ONE ROAD.'), (T0[1], T0[2], 'ONE DAY.'), (T0[14], T0[15], 'GOLDEN HOUR'),
        (T0[16], T0[17], 'NIGHTFALL'), (T0[20] + 0.3, END, 'PORSCHE|TAYCAN GTS')]

_tc = {}
def tl(text):
    if text in _tc: return _tc[text]
    lines = text.split('|'); size = 120; f = fnt(size)
    while max(f.getbbox(l)[2] for l in lines) > 960: size -= 6; f = fnt(size)
    m = Image.new('L', (W, H), 0); d = ImageDraw.Draw(m); lh = int(size * 1.1); y0 = H // 2 - lh * len(lines) // 2
    for i, l in enumerate(lines):
        bb = f.getbbox(l); d.text(((W - bb[2]) / 2, y0 + i * lh), l, font=f, fill=255)
    m = np.asarray(m).astype(np.float32) / 255
    sh = np.asarray(Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(14))).astype(np.float32) / 255
    _tc[text] = (np.where(m[..., None] > 0.01, 1.0, 0.0).astype(np.float32), np.clip(m + sh * 0.6, 0, 1)[..., None])
    return _tc[text]


def look(a):
    lum = a @ np.array([0.299, 0.587, 0.114], np.float32)
    a = lum[..., None] + (a - lum[..., None]) * 1.1
    a = np.clip((a - 0.02) * 1.06, 0, 1); s = a * a * (3 - 2 * a); a = s * 0.45 + a * 0.55
    return np.clip(a + (1 - lum[..., None]) * np.array([-0.02, 0.0, 0.03]) + lum[..., None] * np.array([0.02, 0.006, -0.015]), 0, 1)


def hblur(a, px):
    px = int(px)
    if px < 3: return a
    acc = np.zeros_like(a)
    for k in range(7): acc += np.roll(a, int(px * (k / 6 - 0.5)), 1)
    return acc / 7


def rotate(a, deg, z):
    im = Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8))
    im = im.rotate(deg, resample=Image.BILINEAR, expand=False)
    return zoom(np.asarray(im).astype(np.float32) / 255, z)


def transition(a, kind, k, side):
    """k: 0..1 intensity (1 = at the swap); side: -1 outgoing, +1 incoming."""
    if kind == 'zoom':
        a = zoom(a, 1 + 0.55 * k * k); return gblur(a, 26 * k * k)
    if kind == 'whip':
        a = np.roll(a, int(-side * W * 0.45 * k * k), 1); return hblur(a, 260 * k)
    if kind == 'spin':
        return gblur(rotate(a, -side * 28 * k * k, 1.25 + 0.3 * k), 14 * k * k)
    return a


def render(f, seqs, paths):
    t = f / FPS
    i = sum(1 for c in CF if c <= f)
    s = SHOTS[i]; start_f = CF[i - 1] if i else 0; end_f = CF[i] if i < len(CF) else int(END * FPS)
    if i not in seqs:
        for q in seqs.values(): q.close()
        seqs.clear(); seqs[i] = Seq(paths[i])
    a = look(frame_for(seqs[i], s['mode'], (f - start_f) / FPS, (end_f - start_f) / FPS))
    a = zoom(a, 1.0 + 0.04 * (f - start_f) / max(1, end_f - start_f))          # slow push inside every shot
    nxt = PLAN[i + 1][4] if i + 1 < len(PLAN) else None
    if nxt and nxt != 'drop' and f >= end_f - TR:                               # leaving: build into the hit
        a = transition(a, nxt, (f - (end_f - TR) + 1) / TR, -1)
    cur = PLAN[i][4]
    if i and f - start_f < TR:
        if cur == 'drop':
            a = flash(a, 1.0 * dec((f - start_f) / FPS, 0.06)); a = chroma(a, 20 * dec((f - start_f) / FPS, 0.1))
            a = np.roll(a, int(22 * dec((f - start_f) / FPS, 0.06) * (1 if f % 2 else -1)), 1)
        else:
            a = transition(a, cur, 1 - (f - start_f) / TR, +1)
            if f == start_f: a = flash(a, 0.18)
    if i == 8 and f - start_f >= TR:
        a = flash(a, 0.9 * dec((f - start_f) / FPS, 0.08))
    if t > END - 0.9: a = a * (1 - ease((t - (END - 0.9)) / 0.9))
    for s0, s1, txt in TEXT:
        if s0 <= t < s1:
            rgb, al = tl(txt); k = ease((t - s0) / 0.1) * (1 - ease((t - (s1 - 0.1)) / 0.1)); a = a * (1 - al * k) + rgb * al * k
    a = a * VIG + GRAIN[f % 4] * 0.4
    return np.clip(a, 0, 1)


if __name__ == '__main__':
    from velocity import clean_span, src_needed
    for sh in SHOTS:                                                             # one source take per shot
        n = clean_span(os.path.join(SRC, FILM), sh['src'], src_needed(sh['mode'], sh['t1'] - sh['t0']) + 0.15)
        if abs(n - sh['src']) > 1e-3: print('pre-clean', SHOTS.index(sh), sh['src'], '->', round(n, 2))
        sh['src'] = n
    _c = velocity.source_cuts(os.path.join(SRC, FILM)); _take = [sum(1 for x in _c if x <= sh['src'] + 0.02) for sh in SHOTS]
    assert len(set(_take)) == len(_take), f'repeated take: {_take}'
    paths = prep(SHOTS, SRC, os.path.join(ROOT, 'tmp_i'), 3840, 2160, prescale=True)
    seqs = {}
    if len(sys.argv) > 1:
        for ts in sys.argv[1:]:
            f0 = int(round(float(ts) * FPS)); seqs = {}; i = sum(1 for c in CF if c <= f0)
            for f in range(CF[i - 1] if i else 0, f0 + 1): a = render(f, seqs, paths)
            Image.fromarray((a * 255).astype(np.uint8)).save(os.path.join(ROOT, 'out', f'I_{float(ts):.3f}.jpg'))
        sys.exit()
    tmp = OUT + '.v.mp4'
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS),
                          '-i', '-', '-c:v', 'libx264', '-preset', 'medium', '-crf', '17', '-pix_fmt', 'yuv420p', tmp], stdin=subprocess.PIPE)
    for f in range(int(END * FPS)):
        p.stdin.write((render(f, seqs, paths) * 255).astype(np.uint8).tobytes())
        if f % 240 == 0: print(f, flush=True)
    p.stdin.close(); p.wait()
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', tmp, '-i', SONG, '-map', '0:v', '-map', '1:a', '-c:v', 'copy',
                    '-af', f'afade=t=out:st={END - 1.0}:d=1.0', '-c:a', 'aac', '-b:a', '256k', '-t', str(END),
                    '-movflags', '+faststart', OUT], check=True)
    os.remove(tmp); print('done', OUT)
