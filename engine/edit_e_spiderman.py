"""Edit E - Movie: Spider-Man: Brand New Day. Direction: "The boy nobody remembers".
Cold open on Peter's line -> Tame Impala 'Loser' carries the story (forgotten -> Spider-Man -> heartbreak ->
mutation -> fight) -> ends on MJ meeting him again: "A friendly neighbor."
Dialogue comes from the official trailer and sits in the gaps between the sung lines; music ducks under it."""
import os, sys, math, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
_argv = sys.argv; sys.argv = [sys.argv[0]]
import edit_c_justdance as ec
from edit_c_justdance import Clip, flash, chroma, zoom, gblur, dec, ease, fnt, VIG, GRAIN, W, H, FPS, ROOT
sys.argv = _argv

MV = os.path.join(ROOT, 'src_mv')
TRAILER = os.path.join(MV, 'tt_official.mp4')
SONG = os.path.join(ROOT, 'songs', 'named', '18_loser_tame_impala.mp3')
OUT = os.path.join(ROOT, 'out', 'edit_E_spiderman_bnd.mp4')
OFF = 2.85                                   # song starts after the cold open
v = lambda s: OFF + s                         # song time -> video time

# dialogue: (src_start, src_end, video_start)
DIALOGUE = [(30.50, 33.32, 0.0), (26.55, 28.65, v(4.0)), (45.65, 47.10, v(8.15)),
            (67.30, 69.15, v(15.9)), (73.30, 74.85, v(19.6)), (146.65, 150.60, v(29.0))]
END = v(29.0) + 4.0 + 1.6

# shots: (video_start, video_end, src_in, speed, fx)
S = []
def shot(a, b, src, speed=1.0, **fx): S.append((a, b, src, speed, fx))
shot(0.0, OFF, 31.95, 0.5, push=0.08)                       # Peter: "You don't remember me…"
shot(v(0.0), v(1.88), 10.0, 1.0)                            # MJ laughing, first day at MIT
shot(v(1.88), v(3.9), 12.5, 1.0, push=0.05)                 # Peter alone on the roof
shot(v(3.9), v(6.0), 26.5, 1.0)                             # "Hi, my name is Peter Parker."
shot(v(6.0), v(8.06), 15.0, 1.0, hit=True)                  # mask goes on - "I'm a hunter, babe"
shot(v(8.06), v(9.36), 44.3, 1.0)                           # "I'm Spider-Man." - jumps
shot(v(9.36), v(10.10), 18.2, 1.0, punch=True)
shot(v(10.10), v(10.80), 46.0, 1.0, punch=True)
shot(v(10.80), v(11.54), 120.3, 1.0, punch=True)
shot(v(11.54), v(13.26), 65.0, 1.0)                         # MJ at the party - "Do you wanna…"
shot(v(13.26), v(15.64), 69.4, 0.7, push=0.06)              # Peter watching her - "…tear my heart out?"
shot(v(15.64), v(18.0), 72.5, 1.0, push=0.05)               # "…even if it breaks Peter Parker's heart."
shot(v(18.0), v(19.5), 76.2, 1.0, hit=True)                 # "I'm a tragedy" - webs
shot(v(19.5), v(21.0), 78.6, 1.0)                           # "What is happening to me?"
shot(v(21.0), v(21.66), 112.4, 1.0, punch=True)
shot(v(21.66), v(22.38), 118.0, 1.0, punch=True)
shot(v(22.38), v(23.13), 132.0, 1.0, punch=True)
shot(v(23.13), v(23.82), 133.0, 1.0, punch=True)
shot(v(23.82), v(24.57), 124.0, 1.0, punch=True)
shot(v(24.57), v(25.29), 125.3, 1.0, punch=True)
shot(v(25.29), v(26.01), 128.0, 1.0, punch=True)
shot(v(26.01), v(26.73), 129.0, 1.0, punch=True)
shot(v(26.73), v(27.45), 134.0, 1.0, punch=True)
shot(v(27.45), v(29.0), 137.0, 0.8, push=0.05)
shot(v(29.0), v(29.0) + 0.85, 146.65, 1.0)                  # "I'm MJ."
shot(v(29.0) + 0.85, v(29.0) + 2.1, 147.5, 1.0)             # Peter's face
shot(v(29.0) + 2.1, v(29.0) + 3.1, 148.6, 1.0)              # MJ: "…across the hall."
shot(v(29.0) + 3.1, v(29.0) + 4.0, 150.0, 1.0)              # Peter: "A friendly neighbor." - smile
shot(v(29.0) + 4.0, END, 141.6, 0.6, title=True)            # title card

# subtitles from the trailer's word timings: (src_time, word) shifted to video time
import json
WORDS = json.load(open(os.path.join(MV, 'tt_words.json')))
SUBS = []
for (s0, s1, vt) in DIALOGUE:
    line = [(w0 - s0 + vt, w) for (w0, w1, w) in WORDS if s0 - 0.05 <= w0 < s1 - 0.08]
    SUBS.append((vt, vt + (s1 - s0) + 0.25, line))
# big lyric moments
LYRICS = [(v(2.44), v(3.9), "YOU COULDN'T|WRITE THIS"), (v(13.26), v(15.64), 'TEAR MY|HEART OUT?'),
          (v(18.0), v(19.45), "I'M A|TRAGEDY")]


def look(a):
    lum = a @ np.array([0.299, 0.587, 0.114], np.float32)
    a = np.clip((a - 0.02) * 1.05, 0, 1)
    s = a * a * (3 - 2 * a); a = s * 0.35 + a * 0.65
    return np.clip(a + (1 - lum[..., None]) * np.array([-0.01, 0.0, 0.02]), 0, 1)


_tc = {}
def layer(key, draw_fn):
    if key not in _tc:
        m = Image.new('L', (W, H), 0); draw_fn(ImageDraw.Draw(m))
        m = np.asarray(m).astype(np.float32) / 255
        sh = np.asarray(Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(10))).astype(np.float32) / 255
        rgb = np.where(m[..., None] > 0.01, 1.0, 0.0).astype(np.float32)
        _tc[key] = (rgb, np.clip(m + sh * 0.75, 0, 1)[..., None])
    return _tc[key]


def sub_layer(words):
    """Dialogue subtitle: words appear as they are spoken, wrapped to 2 lines, lower third."""
    text = ' '.join(words)
    f = fnt(54)
    def draw(d):
        lines, cur = [], ''
        for w in words:
            t = (cur + ' ' + w).strip()
            if f.getbbox(t)[2] > 900: lines.append(cur); cur = w
            else: cur = t
        lines.append(cur)
        lh = 70; y0 = int(H * 0.76) - lh * (len(lines) - 1) // 2
        for i, l in enumerate(lines):
            bb = f.getbbox(l); d.text(((W - bb[2]) / 2, y0 + i * lh), l, font=f, fill=255)
    return layer(('sub', text), draw)


def lyric_layer(text):
    f = fnt(124)
    def draw(d):
        lines = text.split('|'); lh = 140; y0 = H // 2 - lh * len(lines) // 2
        for i, l in enumerate(lines):
            size = 124; ff = f
            while ff.getbbox(l)[2] > 960: size -= 6; ff = fnt(size)
            bb = ff.getbbox(l); d.text(((W - bb[2]) / 2, y0 + i * lh), l, font=ff, fill=255)
    return layer(('lyr', text), draw)


def comp(a, lay, k):
    rgb, al = lay
    return a * (1 - al * k) + rgb * al * k


def render(f, st):
    t = f / FPS
    i = next(i for i, s in enumerate(S) if s[0] <= t < s[1])
    a0, a1, src, speed, fx = S[i]; lt, dur = t - a0, a1 - a0
    if i not in st:
        for c in st.values():
            if c.p: c.p.kill()
        st.clear(); st[i] = Clip('tt_official', src, W, H, 0.5, speed)
    old = ec.CL; ec.CL = MV
    try: raw = st[i].frame()
    finally: ec.CL = old
    a = look(raw)
    z = 1.0 + fx.get('push', 0) * lt / dur
    if fx.get('punch'): z += 0.07 * dec(lt, 0.08)
    if fx.get('hit'): z += 0.15 * dec(lt, 0.12)
    a = zoom(a, z)
    if fx.get('punch'): a = flash(a, 0.25 * dec(lt, 0.05))
    if fx.get('hit'): a = flash(a, 0.7 * dec(lt, 0.08)); a = chroma(a, 10 * dec(lt, 0.1))
    if fx.get('title'): a = a * (1 - ease((t - (END - 0.6)) / 0.6))
    for (s0, s1, txt) in LYRICS:
        if s0 <= t < s1:
            k = ease((t - s0) / 0.15) * (1 - ease((t - (s1 - 0.12)) / 0.12))
            a = comp(a, lyric_layer(txt), k)
    for (s0, s1, line) in SUBS:
        if s0 <= t < s1:
            shown = [w for (wt, w) in line if wt <= t + 0.02]
            if shown:
                a = comp(a, sub_layer(shown), 1 - ease((t - (s1 - 0.15)) / 0.15))
    a = a * VIG + GRAIN[f % 4] * 0.7
    return np.clip(a, 0, 1)


def build_audio(path):
    SR = 44100
    def load(p):
        b = subprocess.run(['ffmpeg', '-v', 'error', '-i', p, '-f', 'f32le', '-ac', '2', '-ar', str(SR), '-'],
                           capture_output=True).stdout
        return np.frombuffer(b, np.float32).reshape(-1, 2).copy()
    song, tr = load(SONG), load(TRAILER)
    n = int(END * SR); out = np.zeros((n, 2), np.float32)
    duck = np.ones(n, np.float32)
    seg = song[: n - int(OFF * SR)]
    out[int(OFF * SR): int(OFF * SR) + len(seg)] += seg * 0.85
    for (s0, s1, vt) in DIALOGUE:
        d = tr[int(s0 * SR): int(s1 * SR)] * 1.6
        r = int(0.03 * SR); env = np.ones(len(d), np.float32); env[:r] = np.linspace(0, 1, r); env[-r:] = np.linspace(1, 0, r)
        i0 = int(vt * SR); out[i0:i0 + len(d)] += d * env[:, None]
        a, b = max(0, i0 - int(0.12 * SR)), min(n, i0 + len(d) + int(0.12 * SR))
        duck[a:b] = np.minimum(duck[a:b], 0.32)
    k = int(0.1 * SR); duck = np.convolve(duck, np.ones(k) / k, 'same')
    # duck only the music: rebuild = dialogue + music*duck
    music = np.zeros((n, 2), np.float32); music[int(OFF * SR): int(OFF * SR) + len(seg)] = seg * 0.85
    final = out - music + music * duck[:, None]
    fo = int(1.5 * SR); final[-fo:] *= np.linspace(1, 0, fo)[:, None]
    # level: bring the music section to about -11 dB RMS, then a limiter catches peaks
    sec = final[int(OFF * SR): int((END - 2) * SR)]
    rms = float(np.sqrt((sec ** 2).mean()) + 1e-9)
    final = final * (10 ** (-11 / 20) / rms)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'f32le', '-ac', '2', '-ar', str(SR), '-i', '-',
                    '-af', 'alimiter=limit=0.89:attack=3:release=60,aresample=48000', path], input=final.astype(np.float32).tobytes(), check=True)


if __name__ == '__main__':
    st = {}
    if len(sys.argv) > 1 and sys.argv[1] == 'audio':
        build_audio(OUT + '.wav'); sys.exit()
    if len(sys.argv) > 1:
        for ts in sys.argv[1:]:
            t = float(ts); st = {}
            i = next(i for i, s in enumerate(S) if s[0] <= t < s[1])
            for f in range(int(round(S[i][0] * FPS)), int(round(t * FPS)) + 1):
                a = render(f, st)
            Image.fromarray((a * 255).astype(np.uint8)).save(os.path.join(ROOT, 'out', f'E_{t:.2f}.jpg'))
        sys.exit()
    wav = OUT + '.wav'; build_audio(wav)
    tmp = OUT + '.v.mp4'
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS),
                          '-i', '-', '-c:v', 'libx264', '-preset', 'slow', '-crf', '18', '-pix_fmt', 'yuv420p', tmp], stdin=subprocess.PIPE)
    n = int(END * FPS)
    for f in range(n):
        p.stdin.write((render(f, st) * 255).astype(np.uint8).tobytes())
        if f % 90 == 0: print(f, '/', n, flush=True)
    p.stdin.close(); p.wait()
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', tmp, '-i', wav, '-map', '0:v', '-map', '1:a', '-c:v', 'copy',
                    '-c:a', 'aac', '-b:a', '256k', '-shortest', '-movflags', '+faststart', OUT], check=True)
    os.remove(tmp); os.remove(wav); print('done', OUT)
