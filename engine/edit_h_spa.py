"""Edit H - DOCUMENTARY / voice-over edit. Direction: "From the pit lane to the top step."
Lionspeed GP's Porsche 911 GT3 R won the 2026 24 Hours of Spa after starting from the pit lane.
The drivers' own words tell the story; music sits under them; every cut snaps to a drum hit (60 fps)."""
import os, sys, json, math, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, os.path.dirname(__file__))
_a = sys.argv; sys.argv = [sys.argv[0]]
from edit_c_justdance import flash, chroma, zoom, gblur, dec, ease, fnt, VIG, GRAIN, ROOT
sys.argv = _a
from velocity import cut_frames

W, H, FPS = 1080, 1920, 60
SRC = os.path.join(ROOT, 'src_car', 'p336980.mp4')
SONG = os.path.join(ROOT, 'songs', 'named', '17_urn_edits_comeback.mp3')
OUT = os.path.join(ROOT, 'out', 'edit_H_spa_documentary.mp4')
GRID = [t for t, a in json.load(open(os.path.join(ROOT, 'songs', '17_grid.json')))['grid']]
snap = lambda t: min(GRID, key=lambda g: abs(g - t))

# voice-over: (src_start, src_end, video_start)
VO = [(82.15, 90.06, 2.40), (28.65, 32.65, 11.80 - 1.35), (42.45, 45.55, 16.0), (96.6, 102.35, 26.95)]
END = 33.4

# shots: (target_time -> snapped to beat, src_in, cx, sync)   sync=True plays src in step with VO
PLAN = [
    (0.00, 102.36, 0.52, False),   # hook: champagne on the top step
    (2.79, 0.05, 0.42, False),     # HOUR 24 pit board
    (3.99, 17.15, 0.50, False),    # the car in the box
    (5.19, 5.80, 0.55, False),     # crew ready
    (6.39, 7.25, 0.55, False),     # wheel change
    (7.59, 23.55, 0.50, False),    # back in the fight
    (9.37, 27.47, 0.55, False),    # #80 Porsche at camera
    (11.80, 30.0, 0.60, 'sync'),   # cut to Preining on a beat, lips in sync with his voice
    (14.19, 51.60, 0.50, False),   # #80 on track
    (15.99, 37.55, 0.50, False),   # "…four hours can be cruel." over the fight
    (17.19, 59.15, 0.50, False),
    (19.00, 56.0, 0.55, False),    # race montage
    (19.59, 49.15, 0.45, False),
    (20.19, 64.0, 0.55, False),
    (20.79, 66.2, 0.50, False),
    (21.40, 69.6, 0.45, False),
    (22.46, 74.5, 0.45, False),
    (22.89, 75.0, 0.55, False),
    (23.49, 76.25, 0.42, 'keep'),  # finish line (clean take 76.2-77.36)
    (24.09, 80.50, 0.50, 'keep'),  # hugs in the pit lane
    (24.86, 81.45, 0.50, 'keep'),
    (25.90, 89.95, 0.50, 'keep'),  # helmets up on the podium
    (26.79, 87.75, 0.50, 'keep'),  # Buus' words over the team photo
    (28.60, 100.20, 0.50, 'keep'), # trophies
    (30.39, 102.36, 0.52, 'keep'), # champagne again: the video loops
]
T0 = [0.0] + [snap(p[0]) for p in PLAN[1:]]
CF = cut_frames(T0[1:])
import velocity; velocity.DETECTOR = 'scene'
from velocity import clean_span
_ends = T0[1:] + [END]
for _i, _p in enumerate(PLAN):                                   # keep every shot inside one source take
    if _p[3] is False:
        _n = clean_span(SRC, _p[1], _ends[_i] - T0[_i] + 0.02)
        if abs(_n - _p[1]) > 1e-3: PLAN[_i] = (_p[0], _n, _p[2], _p[3])

TEXT = [(0.0, 1.45, 'STARTED FROM|THE PIT LANE.'), (1.45, T0[1], 'WON THE 24 HOURS|OF SPA.'),
        (T0[6] + 1.0, T0[7], '4 HOURS TO GO'), (T0[18], T0[19], 'P1.'),
        (T0[24] + 0.4, END, 'LIONSPEED GP|PORSCHE 911 GT3 R')]
CAPS = []                                                       # spoken subtitles
W_ = json.load(open(os.path.join(ROOT, 'src_car', 'p336980_words.json')))
for s0, s1, vt in VO:
    CAPS.append((vt, vt + (s1 - s0), [(w0 - s0 + vt, w.replace('Floorless', 'Flawless')) for w0, w1, w in W_ if s0 <= w0 < s1]))


class Reader:
    def __init__(self, t, cx):
        x = int((1600 - 1080) * cx)
        vf = (f'fps={FPS},split[a][b];[a]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,'
              f'scale=270:480,gblur=sigma=10,scale=1080:1920,eq=brightness=-0.12:saturation=0.8[bg];'
              f'[b]scale=1600:900:flags=lanczos,crop=1080:900:{x}:0,unsharp=5:5:0.5[fg];[bg][fg]overlay=0:510')
        self.p = subprocess.Popen(['ffmpeg', '-v', 'error', '-ss', f'{t:.3f}', '-i', SRC, '-filter_complex', vf, '-f', 'rawvideo',
                                   '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
        self.last = np.zeros((H, W, 3), np.float32)

    def frame(self):
        b = self.p.stdout.read(W * H * 3)
        if len(b) == W * H * 3: self.last = np.frombuffer(b, np.uint8).reshape(H, W, 3).astype(np.float32) / 255
        return self.last


def look(a):
    lum = a @ np.array([0.299, 0.587, 0.114], np.float32)
    a = lum[..., None] + (a - lum[..., None]) * 0.9
    a = np.clip((a - 0.025) * 1.06, 0, 1); s = a * a * (3 - 2 * a); a = s * 0.4 + a * 0.6
    return np.clip(a + (1 - lum[..., None]) * np.array([-0.01, 0.005, 0.02]) + lum[..., None] * np.array([0.02, 0.008, -0.012]), 0, 1)


_tc = {}
def layer(key, lines, size, y):
    if key in _tc: return _tc[key]
    f = fnt(size)
    while max(f.getbbox(l)[2] for l in lines) > 960: size -= 4; f = fnt(size)
    m = Image.new('L', (W, H), 0); d = ImageDraw.Draw(m); lh = int(size * 1.15); y0 = int(H * y) - lh * len(lines) // 2
    for i, l in enumerate(lines):
        bb = f.getbbox(l); d.text(((W - bb[2]) / 2, y0 + i * lh), l, font=f, fill=255)
    m = np.asarray(m).astype(np.float32) / 255
    sh = np.asarray(Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(10))).astype(np.float32) / 255
    _tc[key] = (np.where(m[..., None] > 0.01, 1.0, 0.0).astype(np.float32), np.clip(m + sh * 0.7, 0, 1)[..., None])
    return _tc[key]


def wrap(words, f, maxw=900):
    lines, cur = [], ''
    for w in words:
        t = (cur + ' ' + w).strip()
        if f.getbbox(t)[2] > maxw and cur: lines.append(cur); cur = w
        else: cur = t
    return lines + [cur]


def render(f, st):
    t = f / FPS
    i = sum(1 for c in CF if c <= f)
    start_f = CF[i - 1] if i else 0
    if i not in st:
        for r in st.values(): r.p.kill()
        st.clear(); p = PLAN[i]; st[i] = Reader(p[1], p[2])
    a = look(st[i].frame()); a[507:510] = 0.9; a[1410:1413] = 0.9
    lt = (f - start_f) / FPS; hit = lt if i else 99
    big = i in (1, 18, 21)
    a = zoom(a, 1.0 + 0.03 * min(lt, 3) / 3 + (0.08 if big else 0.04) * dec(hit, 0.09))
    a = flash(a, (0.7 if big else 0.22) * dec(hit, 0.05))
    if big: a = chroma(a, 8 * dec(hit, 0.08))
    if t > END - 0.9: a = a * (1 - ease((t - (END - 0.9)) / 0.9))
    for s0, s1, txt in TEXT:
        if s0 <= t < s1:
            rgb, al = layer(('t', txt), txt.split('|'), 100, 0.17)
            k = ease((t - s0) / 0.08) * (1 - ease((t - (s1 - 0.08)) / 0.08)); a = a * (1 - al * k) + rgb * al * k
    for ci, (s0, s1, ws) in enumerate(CAPS):
        nxt = min([c[0] for c in CAPS if c[0] > s0] + [99])
        if s0 <= t < min(s1 + 0.3, nxt):
            shown = [w for wt, w in ws if wt <= t + 0.02]
            if shown:
                f52 = fnt(52); lines = wrap(shown, f52)[-2:]
                rgb, al = layer(('c', tuple(lines)), lines, 52, 0.83)
                a = a * (1 - al) + rgb * al
    a = a * VIG + GRAIN[f % 4] * 0.45
    return np.clip(a, 0, 1)


def audio(path):
    SR = 48000
    def load(p, ss=0, t=None):
        cmd = ['ffmpeg', '-v', 'error', '-ss', str(ss), '-i', p] + (['-t', str(t)] if t else [])
        b = subprocess.run(cmd + ['-ac', '2', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True).stdout
        return np.frombuffer(b, np.float32).reshape(-1, 2).copy()
    n = int(END * SR)
    music = load(SONG, 0, END)[:n]; music = np.pad(music, ((0, n - len(music)), (0, 0)))
    duck = np.ones(n, np.float32); voice = np.zeros((n, 2), np.float32)
    for s0, s1, vt in VO:
        v = load(SRC, s0, s1 - s0); r = int(0.04 * SR); env = np.ones(len(v), np.float32)
        env[:r] = np.linspace(0, 1, r); env[-r:] = np.linspace(1, 0, r)
        i0 = int(vt * SR); m = min(len(v), n - i0); voice[i0:i0 + m] += (v * env[:, None])[:m]
        duck[max(0, i0 - int(.25 * SR)): i0 + m + int(.2 * SR)] = 0.28
    k = int(0.18 * SR); duck = np.convolve(duck, np.ones(k) / k, 'same')
    vr = np.sqrt((voice[np.abs(voice).sum(1) > 0] ** 2).mean()); mr = np.sqrt((music ** 2).mean())
    mix = music * (10 ** (-14 / 20) / mr) * duck[:, None] + voice * (10 ** (-13 / 20) / vr)
    fo = int(1.0 * SR); mix[-fo:] *= np.linspace(1, 0, fo)[:, None]
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'f32le', '-ac', '2', '-ar', str(SR), '-i', '-',
                    '-af', 'alimiter=limit=0.89', path], input=mix.astype(np.float32).tobytes(), check=True)


if __name__ == '__main__':
    st = {}
    if len(sys.argv) > 1:
        for ts in sys.argv[1:]:
            t = float(ts); st = {}; i = sum(1 for c in CF if c <= int(t * FPS))
            for f in range(CF[i - 1] if i else 0, int(t * FPS) + 1): a = render(f, st)
            Image.fromarray((a * 255).astype(np.uint8)).save(os.path.join(ROOT, 'out', f'H_{t:.2f}.jpg'))
        sys.exit()
    wav = OUT + '.wav'; audio(wav); tmp = OUT + '.v.mp4'
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS),
                          '-i', '-', '-c:v', 'libx264', '-preset', 'medium', '-crf', '17', '-pix_fmt', 'yuv420p', tmp], stdin=subprocess.PIPE)
    for f in range(int(END * FPS)):
        p.stdin.write((render(f, st) * 255).astype(np.uint8).tobytes())
        if f % 240 == 0: print(f, flush=True)
    p.stdin.close(); p.wait()
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', tmp, '-i', wav, '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac',
                    '-b:a', '256k', '-shortest', '-movflags', '+faststart', OUT], check=True)
    os.remove(tmp); os.remove(wav); print('done', OUT)
