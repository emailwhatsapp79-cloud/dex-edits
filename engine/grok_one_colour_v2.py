"""CAR v2 - one colour. 911 GT3 S/C, Guards Red.
Not a Paint-to-Sample one-off. It is the April 2026 newsroom walkaround
(newstv 332698) because that film actually has the detail grammar N17 uses.
328485 Formosa is not used.
One car, one red. Side profile is the anchor, three times, from the same
tracking take. The other cuts are different details. Dark, cool grade. No text.
Sound #104, 0.00-10.88 only. The explicit line is at 11.00 and is not in the file.
Master 1920x1080, 25 fps (a downscale of the 4K). 
"""
import os, sys, subprocess
sys.path.insert(0, os.path.dirname(__file__))
import wideedit

ROOT = wideedit.ROOT
SRC = '/tmp/dexsrc/porsche_332698.mp4'
SONG = '/tmp/dexsrc/song104.wav'
FPS = 25
W, H = 1920, 1080
END = 10.880
GRADE = 'eq=contrast=1.16:saturation=1.12:gamma=0.84:brightness=-0.03,colorbalance=bs=0.06:bm=0.03:bh=0.02,unsharp=3:3:0.2'
# (edit t snapped early, src t, last src time the detail is still clean)
SHOTS = [
    (0.000, 44.30, 46.20),   # side, the anchor
    (0.520, 49.05, 50.05),   # rear
    (1.000, 50.55, 53.50),   # wheel
    (1.440, 55.98, 56.50),   # lamp
    (1.880, 65.95, 66.50),   # mirror
    (2.320, 124.00, 124.70), # side blade
    (2.840, 126.15, 127.20), # paint
    (3.280, 130.20, 131.10), # wheel, a hand
    (3.840, 133.20, 134.10), # scoop
    (4.320, 45.15, 46.20),   # side, the anchor
    (4.920, 137.95, 139.00), # exhaust
    (5.520, 149.48, 150.00), # tail lamp
    (6.040, 166.85, 167.80), # light bar
    (6.520, 173.30, 174.20), # diffuser
    (7.080, 192.28, 192.85), # mirror
    (7.520, 202.25, 203.05), # the wheel, inside
    (8.080, 45.80, 46.40),   # side, the anchor
    (8.520, 210.50, 211.20), # door card
    (8.960, 240.45, 241.15), # the gear lever
    (9.480, 264.85, 265.40), # the column
    (9.960, 84.85, 85.45),   # hands on the wheel
    (10.440, 156.00, 156.45), # a hand on the deck
]


def frames():
    ts = [s[0] for s in SHOTS] + [END]
    fr = [round(t * FPS) for t in ts]
    return [b - a for a, b in zip(fr, fr[1:])]


def check():
    used = []
    assert len(SHOTS) >= 16
    for (t, st, limit), n in zip(SHOTS, frames()):
        d = n / FPS
        assert d >= 0.36, t
        assert st + d <= limit + 0.02, f'past the clean frame {t} {st}+{d:.2f} > {limit}'
        for a, b in used:
            assert st + d <= a + 0.02 or st >= b - 0.02, f'overlap {st}'
        used.append((st, st + d))
        print(f'{t:6.2f} {d:5.2f}s @{st:7.2f} -> {st+d:7.2f}')
    print('shots', len(SHOTS), 'end', END)


def render(out, tmp):
    os.makedirs(tmp, exist_ok=True)
    parts = []
    for i, ((t, st, limit), n) in enumerate(zip(SHOTS, frames())):
        p = os.path.join(tmp, f's{i:02d}.mp4')
        parts.append(p)
        vf = f'fps={FPS},scale={W}:{H}:flags=lanczos,{GRADE},setsar=1'
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{st:.3f}', '-i', SRC, '-frames:v', str(n),
                        '-an', '-vf', vf, '-c:v', 'libx264', '-crf', '12', '-preset', 'veryfast', '-pix_fmt', 'yuv420p', p], check=True)
    lst = os.path.join(tmp, 'list.txt')
    open(lst, 'w').write(''.join(f"file '{p}'\n" for p in parts))
    vid = os.path.join(tmp, 'video.mp4')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', lst, '-c', 'copy', vid], check=True)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', vid, '-i', SONG,
                    '-filter_complex', f"[1:a]atrim=0:{END:.3f},afade=t=out:st={END-0.40:.3f}:d=0.40[a]",
                    '-map', '0:v', '-map', '[a]', '-t', f'{END:.3f}', '-c:v', 'libx264', '-crf', '12',
                    '-preset', 'fast', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '256k', out], check=True)
    print(out)


if __name__ == '__main__':
    check()
    if len(sys.argv) > 1 and sys.argv[1] == 'check':
        sys.exit(0)
    render('/tmp/out/grok_one_colour_v2.mp4', '/tmp/tmp_onecolour_v2')
