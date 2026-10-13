"""Edit F - Car: Porsche Taycan GTS + E-Shift. Direction: "Electric. Silent. Boring? - not anymore."
One car (red Taycan GTS) from Porsche's official 4K press film. Calm, clean shots while the vocal says
"I'll leave this behind / promise me just one thing"; "destroy it all" = paddle pull; drop = rev needle snaps."""
import os, sys, math, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
_argv = sys.argv; sys.argv = [sys.argv[0]]
import edit_c_justdance as ec
from edit_c_justdance import Clip, flash, chroma, zoom, gblur, dec, ease, fnt, VIG, GRAIN, W, H, FPS, ROOT
sys.argv = _argv

CAR = os.path.join(ROOT, 'src_car')
SONG = os.path.join(ROOT, 'songs', 'named', '19_destroy_it_all_yuji_slowed.mp3')
OUT = os.path.join(ROOT, 'out', 'edit_F_taycan_eshift.mp4')
END = 25.2
DROP = 5.5

S = []
def shot(a, b, src, cx=0.5, speed=1.0, **fx): S.append((a, b, src, cx, speed, fx))
shot(0.00, 1.20, 98.9, 0.50, 0.7, push=0.05)          # car at camera, dusk - "ELECTRIC."
shot(1.20, 2.30, 140.2, 0.45, 0.6, push=0.04)          # sunset pass - "SILENT."
shot(2.30, 3.30, 138.5, 0.50, 1.0, push=0.05)          # GTS dial idle - "BORING?"
shot(3.30, 4.10, 143.4, 0.40, 1.0)                     # driver reaches - "NOT ANYMORE."
shot(4.10, 5.50, 144.4, 0.50, 0.6, build=True)         # paddle pull - "destroy it all"
shot(5.50, 6.29, 148.5, 0.50, 1.0, hit=True)           # DROP: needle snaps - "E-SHIFT"
shot(6.29, 7.29, 147.0, 0.50, 1.0, punch=True)         # night city
shot(7.29, 8.34, 5.0, 0.42, 1.0, punch=True)           # track pass - "8 VIRTUAL GEARS."
shot(8.34, 8.86, 20.5, 0.50, 1.0, punch=True)          # paddle
shot(8.86, 9.38, 19.5, 0.45, 1.0, punch=True)          # dial 32 -> 40
shot(9.38, 10.43, 10.0, 0.55, 1.0, punch=True)         # car side, motion blur
shot(10.43, 11.35, 19.0, 0.50, 1.0, punch=True)        # driver's eyes
shot(11.35, 12.31, 18.0, 0.45, 1.0, punch=True)        # car low front, sun
shot(12.31, 12.82, 20.0, 0.45, 1.0, punch=True)        # dial climbing
shot(12.82, 13.84, 128.2, 0.50, 1.0, punch=True)       # car on the road
shot(13.84, 14.40, 65.0, 0.45, 1.0, punch=True)        # paddle tap
shot(14.40, 15.58, 123.0, 0.50, 1.0, punch=True)       # cornering at camera
shot(15.58, 16.60, 118.6, 0.62, 3.0, punch=True)       # speedo 48 -> 100
shot(16.60, 17.67, 122.0, 0.35, 1.0, punch=True)       # wheel close
shot(17.67, 18.74, 114.0, 0.50, 1.0, punch=True)       # drives away
shot(18.74, 19.37, 92.0, 0.40, 1.0, punch=True)        # paddle
shot(19.37, 20.97, 140.0, 0.55, 0.7, push=0.05)        # sunset again
shot(20.97, 22.13, 149.4, 0.50, 1.0, punch=True)       # dial at night
shot(22.13, END, 150.0, 0.50, 0.6, push=0.06, outro=True)  # night street - title

TEXT = [(0.00, 1.20, 'ELECTRIC.'), (1.20, 2.30, 'SILENT.'), (2.30, 3.30, 'BORING?'), (3.30, 4.10, 'NOT ANYMORE.'),
        (5.50, 7.29, 'E-SHIFT'), (7.29, 8.34, '8 VIRTUAL|GEARS.'), (22.30, 23.60, 'PORSCHE|TAYCAN GTS'), (23.60, END, 'E-SHIFT')]


def look(a):
    lum = a @ np.array([0.299, 0.587, 0.114], np.float32)
    a = lum[..., None] + (a - lum[..., None]) * 1.08
    a = np.clip((a - 0.02) * 1.06, 0, 1)
    s = a * a * (3 - 2 * a); a = s * 0.45 + a * 0.55
    l = lum[..., None]
    return np.clip(a + (1 - l) * np.array([-0.02, 0.005, 0.03]) + l * np.array([0.02, 0.005, -0.015]), 0, 1)


_tc = {}
def text_layer(text, glow=False):
    key = (text, glow)
    if key in _tc: return _tc[key]
    lines = text.split('|'); size = 150 if text == 'E-SHIFT' else 116
    f = fnt(size)
    while max(f.getbbox(l)[2] for l in lines) > 960: size -= 6; f = fnt(size)
    m = Image.new('L', (W, H), 0); d = ImageDraw.Draw(m)
    lh = int(size * 1.12); y0 = H // 2 - lh * len(lines) // 2
    for i, l in enumerate(lines):
        bb = f.getbbox(l); d.text(((W - bb[2]) / 2, y0 + i * lh), l, font=f, fill=255)
    m = np.asarray(m).astype(np.float32) / 255
    sh = np.asarray(Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(16))).astype(np.float32) / 255
    col = np.array([1.0, 0.25, 0.22], np.float32) if glow else np.array([1, 1, 1], np.float32)
    rgb = np.where(m[..., None] > 0.01, col, col * 0.9 if glow else 0).astype(np.float32)
    al = np.clip(m + sh * (1.2 if glow else 0.6), 0, 1)[..., None]
    _tc[key] = (rgb, al)
    return _tc[key]


def render(f, st):
    t = f / FPS
    i = next(i for i, s in enumerate(S) if s[0] <= t < s[1])
    a0, a1, src, cx, speed, fx = S[i]; lt, dur = t - a0, a1 - a0
    if i not in st:
        for c in st.values():
            if c.p: c.p.kill()
        st.clear(); st[i] = Clip('p337658', src, W, H, cx, speed)
    old = ec.CL; ec.CL = CAR
    try: raw = st[i].frame()
    finally: ec.CL = old
    a = look(raw)
    z = 1.0 + fx.get('push', 0) * lt / dur
    if fx.get('punch'): z += 0.08 * dec(lt, 0.08)
    if fx.get('hit'): z += 0.25 * dec(lt, 0.12)
    if fx.get('build'): z += 0.3 * ease((lt - (dur - 0.35)) / 0.35)
    a = zoom(a, z)
    if fx.get('build') and lt > dur - 0.25: a = gblur(a, 26 * ease((lt - (dur - 0.25)) / 0.25))
    if fx.get('punch'): a = flash(a, 0.22 * dec(lt, 0.05)); a = chroma(a, 6 * dec(lt, 0.06))
    if fx.get('hit'):
        a = flash(a, 0.95 * dec(lt, 0.1)); a = chroma(a, 18 * dec(lt, 0.12))
        a = np.roll(a, int(20 * dec(lt, 0.18) * math.sin(lt * 80)), 1)
    if fx.get('outro') and t > END - 1.0: a = a * (1 - ease((t - (END - 1.0)) / 1.0))
    for (s0, s1, txt) in TEXT:
        if s0 <= t < s1:
            rgb, al = text_layer(txt, glow=(txt == 'E-SHIFT'))
            p = ease((t - s0) / 0.1); k = p * (1 - ease((t - (s1 - 0.08)) / 0.08))
            if p < 1:
                sc = 1 + 0.18 * (1 - p)
                im = Image.fromarray((np.dstack([rgb, al]) * 255).astype(np.uint8), 'RGBA')
                nw, nh = int(W * sc), int(H * sc)
                im = im.resize((nw, nh)).crop(((nw - W) // 2, (nh - H) // 2, (nw - W) // 2 + W, (nh - H) // 2 + H))
                arr = np.asarray(im).astype(np.float32) / 255; rgb, al = arr[..., :3], arr[..., 3:]
            a = a * (1 - al * k) + rgb * al * k
    a = a * VIG + GRAIN[f % 4] * 0.6
    return np.clip(a, 0, 1)


if __name__ == '__main__':
    st = {}
    if len(sys.argv) > 1:
        for ts in sys.argv[1:]:
            t = float(ts); st = {}
            i = next(i for i, s in enumerate(S) if s[0] <= t < s[1])
            for f in range(int(round(S[i][0] * FPS)), int(round(t * FPS)) + 1):
                a = render(f, st)
            Image.fromarray((a * 255).astype(np.uint8)).save(os.path.join(ROOT, 'out', f'F_{t:.2f}.jpg'))
        sys.exit()
    tmp = OUT + '.v.mp4'
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS),
                          '-i', '-', '-c:v', 'libx264', '-preset', 'slow', '-crf', '18', '-pix_fmt', 'yuv420p', tmp], stdin=subprocess.PIPE)
    n = int(END * FPS)
    for f in range(n):
        p.stdin.write((render(f, st) * 255).astype(np.uint8).tobytes())
        if f % 90 == 0: print(f, '/', n, flush=True)
    p.stdin.close(); p.wait()
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', tmp, '-i', SONG, '-map', '0:v', '-map', '1:a', '-c:v', 'copy',
                    '-af', f'volume=-1dB,alimiter=limit=0.9,afade=t=out:st={END - 1.2}:d=1.2', '-c:a', 'aac', '-b:a', '256k',
                    '-t', str(END), '-movflags', '+faststart', OUT], check=True)
    os.remove(tmp); print('done', OUT)
