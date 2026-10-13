"""Edit D - Football: "The Last Tango". Direction: Messi's last night in an Argentina shirt.
Hook = his last goal -> look back (VHS, Rosario, 2005, the glory) -> drop on the penalty -> the night -> Gracias, Leo.
Song: 06 Brazilian funk, lyrics translated on screen ("just look back", "slowly", "the glory")."""
import os, sys, math, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.argv_backup = sys.argv; sys.argv = [sys.argv[0]]
from edit_c_justdance import Clip, flash, chroma, zoom, gblur, dec, ease, fnt, VIG, GRAIN, W, H, FPS, ROOT
sys.argv = sys.argv_backup

FB = os.path.join(ROOT, 'src_fb', 'x')
SONG = os.path.join(ROOT, 'songs', 'named', '06_oya_sa_funk_144bpm.mp3')
OUT = os.path.join(ROOT, 'out', 'edit_D_messi_last_tango.mp4')
END = 28.4
WIDE_H = 409                           # 2.6:1 flashback strip (subtitles cropped off)


def grade_now(a):
    """Farewell night: punchy, cool blacks, Argentina sky-blue kept clean."""
    lum = a @ np.array([0.299, 0.587, 0.114], np.float32)
    a = lum[..., None] + (a - lum[..., None]) * 1.12
    a = np.clip((a - 0.03) * 1.07, 0, 1)
    s = a * a * (3 - 2 * a); a = s * 0.45 + a * 0.55
    l = lum[..., None]
    return np.clip(a + (1 - l) * np.array([-0.01, 0.0, 0.025]), 0, 1)


def grade_past(a, vhs=False):
    """Memories: warm, softer, slightly faded."""
    lum = a @ np.array([0.299, 0.587, 0.114], np.float32)
    a = lum[..., None] + (a - lum[..., None]) * (0.6 if vhs else 0.85)
    a = a * 0.92 + 0.04
    return np.clip(a + np.array([0.03, 0.012, -0.025]), 0, 1)


class Src:
    def __init__(self, name, src_in, speed=1.0, wide=False, cx=0.5, cy=0.5, z=1.0, zcy=0.5):
        self.wide, self.z, self.zcy = wide, z, zcy
        w, h = (W, int(W / 1276 * 718)) if wide else (W, H)
        self.c = Clip(name, src_in, w, h, cx, speed, cy)
        self.c.args = (name, src_in, w, h, cx, speed, cy)
        global_path = os.path.join(FB, name + '.mp4')
        self.c_path = global_path

    def frame(self):
        name = self.c.args[0]
        # Clip() reads from clips/hd; point it at the football folder
        import edit_c_justdance as ec
        old = ec.CL; ec.CL = FB
        try:
            a = self.c.frame()
        finally:
            ec.CL = old
        return a


# (start, end, source spec, options)
K = [13.79, 14.65, 15.51, 16.37, 17.23, 18.09, 18.95, 19.81, 20.67, 21.52, 22.38, 23.22, 24.08, 24.94]
SHOTS = [
    (0.00, 1.36, dict(src=('goal_angle', 6.85, 0.5), look='now', z=1.3, zcy=0.3, push=0.06)),
    (1.36, 2.80, dict(src=('drone_fox', 1.2, 1.0), look='now', z=2.2, zcx=0.56, zcy=0.2, push=0.08)),
    (2.80, 3.74, dict(src=('handshake', 0.4, 1.0), look='now', z=1.4, zcy=0.0)),
    (3.74, 4.92, dict(src=('afa_tribute', 1.6, 1.0), look='vhs', wide=True)),
    (4.92, 5.94, dict(src=('afa_tribute', 3.9, 1.0), look='vhs', wide=True)),
    (5.94, 7.64, dict(src=('afa_tribute', 4.95, 0.8), look='past', wide=True)),
    (7.64, 8.48, dict(src=('afa_tribute', 6.5, 1.0), look='past', wide=True)),
    (8.48, 9.32, dict(src=('afa_tribute', 8.0, 1.0), look='past', wide=True)),
    (9.32, 10.36, dict(src=('afa_tribute', 47.3, 0.8), look='past', wide=True, glow=True)),
    (10.36, 10.76, dict(src=('afa_tribute', 21.0, 1.0), look='past', wide=True, punch=True)),
    (10.76, 11.54, dict(src=('afa_tribute', 18.6, 1.0), look='past', wide=True, punch=True)),
    (11.54, 11.98, dict(src=('afa_tribute', 29.0, 1.0), look='past', wide=True, punch=True)),
    (11.98, 12.40, dict(src=('afa_tribute', 21.9, 1.0), look='past', wide=True, punch=True)),
    (12.40, 12.70, dict(src=('afa_tribute', 52.4, 1.0), look='past', wide=True, punch=True)),
    (12.70, 13.79, dict(src=('goal_angle', 2.0, 1.0), look='now', z=1.3, zcy=0.3, build=True)),
    (13.79, 14.65, dict(src=('goal_angle', 3.25, 1.0), look='now', z=1.3, zcy=0.3, hit=True)),
    (14.65, 15.51, dict(src=('goal_angle', 5.5, 1.0), look='now', z=1.3, zcy=0.3, punch=True)),
    (15.51, 16.37, dict(src=('goal_angle', 6.6, 1.0), look='now', z=1.3, zcy=0.3, punch=True)),
    (16.37, 17.23, dict(src=('goal_angle', 7.8, 1.0), look='now', z=1.3, zcy=0.3, punch=True)),
    (17.23, 18.09, dict(src=('handshake', 5.0, 1.0), look='now', z=1.4, zcy=0.0, punch=True)),
    (18.09, 18.95, dict(src=('handshake', 11.0, 1.0), look='now', z=1.4, zcy=0.0, punch=True)),
    (18.95, 19.81, dict(src=('afa_tribute', 65.3, 1.0), look='past', wide=True, punch=True)),
    (19.81, 20.67, dict(src=('drone_fox', 2.4, 1.0), look='now', z=2.2, zcx=0.56, zcy=0.2, punch=True)),
    (20.67, 21.52, dict(src=('drone_fox', 8.0, 1.0), look='now', z=1.35, zcx=0.3, zcy=0.75, punch=True)),
    (21.52, 22.38, dict(src=('afa_tribute', 73.3, 1.0), look='past', wide=True, punch=True)),
    (22.38, 23.22, dict(src=('drone_fox', 12.4, 1.0), look='now', z=1.35, zcx=0.3, zcy=0.75, punch=True)),
    (23.22, 24.08, dict(src=('afa_tribute', 52.4, 0.8), look='past', wide=True, punch=True)),
    (24.08, 24.94, dict(src=('goal_angle', 6.6, 0.5), look='now', z=1.3, zcy=0.3, punch=True)),
    (24.94, END, dict(src=('drone_fox', 1.2, 0.6), look='now', z=2.2, zcx=0.56, zcy=0.2, push=0.1, outro=True)),
]

# text: (start, end, text, style) style: big | sub (lyric translation) | num
TEXT = [
    (0.00, 0.62, 'HIS LAST GOAL', 'big'), (0.62, 1.36, 'FOR ARGENTINA.', 'big'),
    (1.36, 2.80, '85,000 CAME|TO SAY GOODBYE', 'big'),
    (2.80, 3.74, 'THE 10TH MINUTE.', 'big'),
    (3.74, 5.94, '"just look back"', 'sub'),
    (5.94, 7.64, '"slowly…"', 'sub'), (6.30, 7.64, 'ROSARIO', 'big'),
    (7.64, 9.32, '"slowly…"', 'sub'), (8.00, 9.32, '2005', 'big'),
    (9.32, 10.36, '"the glory"', 'sub'), (9.50, 10.36, '2022', 'big'),
    (10.36, 11.54, '208 GAMES', 'big'), (11.54, 11.98, '126 GOALS', 'big'), (11.98, 12.70, '1 WORLD CUP', 'big'),
    (13.79, 15.51, '126.', 'num'),
    (24.94, 26.66, '126 GOALS.|208 GAMES.', 'big'), (26.66, END, 'GRACIAS, LEO.', 'big'),
]

_tc = {}
def text_layer(text, style):
    key = (text, style)
    if key in _tc: return _tc[key]
    lines = text.split('|')
    if style == 'sub':
        f = fnt(56); f2 = None
    elif style == 'num':
        f = fnt(330)
    else:
        f = fnt(118)
    # shrink to fit
    size = f.size
    while max(f.getbbox(l)[2] for l in lines) > 940 and size > 50:
        size -= 6; f = fnt(size)
    asc, desc = f.getmetrics(); lh = int((asc + desc) * 1.02)
    m = Image.new('L', (W, H), 0); d = ImageDraw.Draw(m)
    cy = {'sub': int(H * 0.73), 'num': H // 2, 'big': H // 2}[style]
    y0 = cy - lh * len(lines) // 2
    for i, l in enumerate(lines):
        bb = f.getbbox(l); d.text(((W - (bb[2] - bb[0])) / 2 - bb[0], y0 + i * lh), l, font=f, fill=255)
    m = np.asarray(m).astype(np.float32) / 255
    sh = np.asarray(Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(16))).astype(np.float32) / 255
    col = np.array([1.0, 1.0, 1.0], np.float32) if style != 'sub' else np.array([0.92, 0.95, 1.0], np.float32)
    if style == 'num':
        col = np.array([0.72, 0.87, 1.0], np.float32)      # Argentina sky blue
    rgb = np.where(m[..., None] > 0.01, col, 0).astype(np.float32)
    al = np.clip(m + sh * 0.6, 0, 1)[..., None]
    _tc[key] = (rgb, al)
    return _tc[key]


def put(a, text, style, lt, life):
    rgb, al = text_layer(text, style)
    p = ease(lt / (0.10 if style != 'sub' else 0.25))
    fade_out = 1 - ease((lt - (life - 0.08)) / 0.08) if style != 'sub' else 1 - ease((lt - (life - 0.2)) / 0.2)
    k = p * fade_out
    if style in ('big', 'num') and p < 1:
        s = 1 + (0.25 if style == 'num' else 0.12) * (1 - p)
        im = Image.fromarray((np.dstack([rgb, al]) * 255).astype(np.uint8), 'RGBA')
        nw, nh = int(W * s), int(H * s)
        im = im.resize((nw, nh), Image.BILINEAR).crop(((nw - W) // 2, (nh - H) // 2, (nw - W) // 2 + W, (nh - H) // 2 + H))
        arr = np.asarray(im).astype(np.float32) / 255; rgb, al = arr[..., :3], arr[..., 3:]
    return a * (1 - al * k) + rgb * al * k


SCAN = (1 - 0.12 * (np.sin(np.arange(WIDE_H) * math.pi / 2) ** 2))[:, None, None].astype(np.float32)


def render_shot(shot, st, t):
    s0, s1, o = shot; lt, dur = t - s0, s1 - s0
    raw = st.frame()
    if o.get('wide'):
        # crop the burned-in subtitles off the bottom: keep a 2.2:1 strip
        strip = raw[78:78 + WIDE_H]
        if strip.shape[0] < WIDE_H:
            strip = np.pad(strip, ((0, WIDE_H - strip.shape[0]), (0, 0), (0, 0)))
        vhs = o['look'] == 'vhs'
        strip = grade_past(strip, vhs)
        if vhs:
            strip = chroma(strip, 4) * SCAN
            strip = strip + np.random.default_rng(int(t * 100)).normal(0, 0.03, (WIDE_H, 1, 1)).astype(np.float32)
        z = 1.0 + 0.04 * lt / dur
        if o.get('punch'): z += 0.10 * dec(lt, 0.08)
        strip = zoom(np.clip(strip, 0, 1), z)
        if o.get('glow'):
            g = gblur(strip, 24); strip = np.clip(strip + g * 0.35, 0, 1)
        sm = Image.fromarray((np.clip(strip, 0, 1) * 255).astype(np.uint8)).resize((240, 91))
        sm = sm.crop((120 - 26, 0, 120 + 26, 91)).resize((W // 4, H // 4)).filter(ImageFilter.GaussianBlur(9)).resize((W, H))
        a = np.asarray(sm).astype(np.float32) / 255 * 0.33
        y0 = (H - WIDE_H) // 2
        a[y0 - 3:y0] = 0.85; a[y0 + WIDE_H:y0 + WIDE_H + 3] = 0.85      # thin frame lines
        a[y0:y0 + WIDE_H] = strip
        if o.get('punch'): a = flash(a, 0.35 * dec(lt, 0.05))
        return a
    a = grade_now(raw)
    if o['src'][0] == 'drone_fox':            # paint out the news logo with the surrounding sky
        y0, y1, x0, x1 = int(H * 0.13), int(H * 0.21), int(W * 0.60), int(W * 0.86)
        ref = a[y0:y1, x0 - 60:x0 - 10].reshape(-1, 3)
        a = a.copy(); a[y0:y1, x0:x1] = np.median(ref, 0)
        a[y0 - 20:y1 + 20, x0 - 20:x1 + 20] = gblur(a, 6)[y0 - 20:y1 + 20, x0 - 20:x1 + 20]
    z = o.get('z', 1.0) + o.get('push', 0.0) * lt / dur
    if o.get('punch'): z += 0.08 * dec(lt, 0.08)
    if o.get('hit'): z += 0.22 * dec(lt, 0.12)
    if o.get('build'): z += 0.25 * ease((lt - (dur - 0.25)) / 0.25)
    a = zoom(a, z, o.get('zcx', 0.5), o.get('zcy', 0.5))
    if o.get('build') and lt > dur - 0.2: a = gblur(a, 22 * ease((lt - (dur - 0.2)) / 0.2))
    if o.get('hit'):
        a = flash(a, 0.95 * dec(lt, 0.09)); a = chroma(a, 16 * dec(lt, 0.1))
        sx = int(18 * dec(lt, 0.15) * math.sin(lt * 70)); a = np.roll(a, sx, 1)
    if o.get('punch'): a = flash(a, 0.3 * dec(lt, 0.05))
    if o.get('outro') and t > END - 1.4: a = a * (1 - ease((t - (END - 1.4)) / 1.4))
    return a


def render(f, states):
    t = f / FPS
    i, shot = next((i, s) for i, s in enumerate(SHOTS) if s[0] <= t < s[1])
    if i not in states:
        for v in states.values():
            if v.c.p: v.c.p.kill()
        states.clear()
        n, src, sp = shot[2]['src']
        states[i] = Src(n, src, sp, wide=shot[2].get('wide', False))
    a = render_shot(shot, states[i], t)
    for (a0, a1, txt, sty) in TEXT:
        if a0 <= t < a1:
            a = put(a, txt, sty, t - a0, a1 - a0)
    a = a * VIG + GRAIN[f % 4]
    return np.clip(a, 0, 1)


if __name__ == '__main__':
    states = {}
    if len(sys.argv) > 1:
        for ts in sys.argv[1:]:
            t = float(ts); states = {}
            i, shot = next((i, s) for i, s in enumerate(SHOTS) if s[0] <= t < s[1])
            for f in range(int(round(shot[0] * FPS)), int(round(t * FPS)) + 1):
                a = render(f, states)
            Image.fromarray((a * 255).astype(np.uint8)).save(os.path.join(ROOT, 'out', f'D_{t:.2f}.jpg'))
        sys.exit()
    tmp = OUT + '.v.mp4'
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS),
                          '-i', '-', '-c:v', 'libx264', '-preset', 'slow', '-crf', '18', '-pix_fmt', 'yuv420p', tmp], stdin=subprocess.PIPE)
    n = int(END * FPS)
    for f in range(n):
        p.stdin.write((render(f, states) * 255).astype(np.uint8).tobytes())
        if f % 90 == 0: print(f, '/', n, flush=True)
    p.stdin.close(); p.wait()
    crowd = os.path.join(FB, 'goal_angle.mp4')
    # music + real crowd roar from the stands under the goal (13.6s -> 18s)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', tmp, '-i', SONG, '-ss', '3.0', '-t', '5.5', '-i', crowd,
                    '-filter_complex',
                    f'[1:a]loudnorm=I=-11:TP=-1[m];[2:a]volume=0.55,afade=t=in:d=0.15,afade=t=out:st=4.0:d=1.5,adelay=13650|13650[c];'
                    f'[m][c]amix=inputs=2:duration=first:normalize=0,afade=t=out:st={END - 1.4}:d=1.4[a]',
                    '-map', '0:v', '-map', '[a]', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '256k', '-t', str(END),
                    '-movflags', '+faststart', OUT], check=True)
    os.remove(tmp); print('done', OUT)
