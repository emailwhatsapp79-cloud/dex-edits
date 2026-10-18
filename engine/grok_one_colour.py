"""CAR - one colour. Porsche 911 Carrera T Sonderwunsch "Formosa".
Paint to Sample Ipanema Blue Metallic. One car, one body colour.
Official newsroom film 328485, 3840x2160 25 fps, used full-frame at 1920x1080 (a downscale).
Side at the shop, the mirror, the light, the rear, then the ridge. No title card
(the film's "THERE IS NO SUBSTITUTE" line is after 117.4s and is not used).
The red car later in the same film is a different car and is not used.
Sound #104 is not in the library. Song #73 is the Paint-to-Sample showroom sound.
Used 0.00-7.04s only, inside the 10.90s line. The lyric in that window is not explicit.
No text on the picture. Dark, cool grade.
"""
import os, sys, subprocess
sys.path.insert(0, os.path.dirname(__file__))
import wideedit

ROOT = wideedit.ROOT
ASSETS = os.environ.get('DEX_ASSETS', os.path.join(os.path.dirname(ROOT), 'dex-edits-assets'))
SRC = '/tmp/dexsrc/porsche_328485.mp4'
SONG = os.path.join(ASSETS, 'songs', '73_gt3_rs_gulf_blue_showroom_porschebakersf.mp3')
FPS = 25
W, H = 1920, 1080
END = 6.440
# darker and cooler than the usual grade, so the blue reads
GRADE = 'eq=contrast=1.16:saturation=1.12:gamma=0.84:brightness=-0.03,colorbalance=bs=0.06:bm=0.03:bh=0.02,unsharp=3:3:0.2'
# (edit t snapped early of a hit, src t). Different takes, no overlap.
SHOTS = [
    (0.000, 52.080),  # side, parked, Ipanema Blue
    (0.640, 55.280),  # mirror
    (2.080, 57.620),  # the light
    (2.760, 58.960),  # rear
    (5.160, 115.120), # the ridge, before the title
]


def frames():
    ts = [s[0] for s in SHOTS] + [END]
    fr = [round(t * FPS) for t in ts]
    return [b - a for a, b in zip(fr, fr[1:])]


def check():
    spans = []
    for (t, st), n in zip(SHOTS, frames()):
        d = n / FPS
        # title fades in ~117.4; interior cut ~53.0; mirror hold through ~56.8; front light through ~58.4
        assert st + d <= 131.0
        for a, b in spans:
            assert st + d <= a or st >= b, f'overlap {st}'
        spans.append((st, st + d))
        print(f'{t:6.2f} {d:5.2f}s @{st:7.2f} -> {st+d:7.2f}')
    # hard windows
    assert SHOTS[0][1] + frames()[0] / FPS < 52.85
    assert SHOTS[1][1] + frames()[1] / FPS < 56.90
    assert SHOTS[2][1] + frames()[2] / FPS < 58.45
    assert SHOTS[4][1] + frames()[4] / FPS < 116.45


def render(out, tmp):
    os.makedirs(tmp, exist_ok=True)
    parts = []
    for i, ((t, st), n) in enumerate(zip(SHOTS, frames())):
        p = os.path.join(tmp, f's{i:02d}.mp4')
        parts.append(p)
        vf = f'fps={FPS},scale={W}:{H}:flags=lanczos,{GRADE},setsar=1'
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{st:.3f}', '-i', SRC, '-frames:v', str(n),
                        '-an', '-vf', vf, '-c:v', 'libx264', '-crf', '10', '-preset', 'fast', '-pix_fmt', 'yuv420p', p], check=True)
    lst = os.path.join(tmp, 'list.txt')
    open(lst, 'w').write(''.join(f"file '{p}'\n" for p in parts))
    vid = os.path.join(tmp, 'video.mp4')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', lst, '-c', 'copy', vid], check=True)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', vid, '-ss', '0', '-i', SONG,
                    '-filter_complex', f"[1:a]atrim=0:{END:.3f},afade=t=out:st={END-0.5:.3f}:d=0.5[a]",
                    '-map', '0:v', '-map', '[a]', '-t', f'{END:.3f}', '-c:v', 'libx264', '-crf', '10',
                    '-preset', 'slow', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '256k', out], check=True)
    print(out)


if __name__ == '__main__':
    check()
    if len(sys.argv) > 1 and sys.argv[1] == 'check':
        sys.exit(0)
    render('/tmp/out/grok_one_colour.mp4', '/tmp/tmp_onecolour')
