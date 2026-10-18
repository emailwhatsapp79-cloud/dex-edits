"""F1 - I get it. Max Verstappen.
The text idea from the M26 flow edit, drawn sharp: a white vertical bar, IT over GET,
the third stamp gold, a thin double frame that punches in on the hit. No blur.
Sound is the 11.8s "I get it" flow edit (library has no #105 file). Stamps at the
asked times 0.48 / 2.80 / 5.34 / 7.36, which sit on the kicks in this recording.
Official formula1.com, 1280x720, 1:1. Master at 50 fps.
Hook is the 2023 Abu Dhabi #1 donuts. That is the season-finale tyre smoke, not the
race the title was decided in. Said so in NOTES.
"""
import os, sys, subprocess
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, os.path.dirname(__file__))
import wideedit

ROOT = wideedit.ROOT
FONT = os.path.join(ROOT, 'fonts', 'Anton.ttf')
FPS = 50
W, H = 1280, 720
END = 10.900
SONG = '/tmp/dexsrc/igetit.wav'
D23 = '/tmp/dexsrc/f1_donuts23.mp4'
D22 = '/tmp/dexsrc/max_donuts22.mp4'
BH = '/tmp/dexsrc/max_bh_line.mp4'
SG = '/tmp/dexsrc/max_sg_line.mp4'
# edit t snapped with int(hit*FPS)/FPS so the cut is early, never late.
# (t, src path, src_t)
SHOTS = [
    (0.000, D23, 1.600),  # tyre smoke, the hook
    (1.640, BH, 0.300),   # head-on, Sepang
    (2.780, D22, 5.400),  # 2022 Abu Dhabi smoke
    (3.800, D23, 12.600), # arms up, before the donut film's own cut
    (5.320, BH, 1.700),   # the car, side-on
    (7.160, D23, 16.200), # helmet off
    (8.740, SG, 0.400),   # Singapore, the line
]
STAMPS = [0.48, 2.80, 5.34, 7.36]  # third is gold
GRADE = 'eq=contrast=1.10:saturation=1.08:gamma=0.94,unsharp=3:3:0.25'


def frames():
    ts = [s[0] for s in SHOTS] + [END]
    fr = [round(t * FPS) for t in ts]
    return [b - a for a, b in zip(fr, fr[1:])]


def check():
    used = {}
    prev = None
    counts = {}
    for (t, src, st), n in zip(SHOTS, frames()):
        d = n / FPS
        assert d > 0.2, t
        for a, b in used.get(src, []):
            assert st + d <= a + 0.02 or st >= b - 0.02, f'overlap {os.path.basename(src)} {st}'
        used.setdefault(src, []).append((st, st + d))
        name = os.path.basename(src)
        counts[name] = counts.get(name, 0) + 1
        assert prev != src, f'same source twice in a row {name}'
        prev = src
        print(f'{t:6.2f} {d:5.2f}s {name[:22]:22} @{st:6.2f}')
    for k, v in counts.items():
        assert v <= 3, k
        print(f'  {v} x {k}')


def _stamp_frame(color, scale, font):
    canvas = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    col = color + (255,)
    for inset, width in ((34, 3), (50, 2)):
        d.rectangle([inset, inset, W - 1 - inset, H - 1 - inset], outline=col, width=width)
    bx, by, bw, bh = W // 2 - 250, H // 2 - 160, 18, 320
    d.rectangle([bx, by, bx + bw, by + bh], fill=col)
    it = 'IT'
    gt = 'GET'
    # IT over GET, heavy, left of centre so the bar leads
    x = bx + bw + 28
    y_it = H // 2 - 150
    d.text((x, y_it), it, font=font, fill=col)
    d.text((x, y_it + 150), gt, font=font, fill=col)
    if abs(scale - 1) < 0.01:
        return layer
    nw, nh = int(W * scale), int(H * scale)
    big = layer.resize((nw, nh), Image.Resampling.LANCZOS)
    canvas.paste(big, ((W - nw) // 2, (H - nh) // 2), big)
    return canvas


def build_stamps(tmp):
    font = ImageFont.truetype(FONT, 150)
    white = (255, 255, 255)
    gold = (212, 168, 72)
    # 8 punch frames then 18 hold frames = 0.52s at 50 fps
    for name, color in (('white', white), ('gold', gold)):
        frames_dir = os.path.join(tmp, name)
        os.makedirs(frames_dir, exist_ok=True)
        seq = []
        for i in range(8):
            scale = 1.14 - 0.14 * (i / 7)
            seq.append(_stamp_frame(color, scale, font))
        hold = _stamp_frame(color, 1.0, font)
        for _ in range(18):
            seq.append(hold)
        for i, im in enumerate(seq):
            im.save(os.path.join(frames_dir, f'{i:02d}.png'))
        mov = os.path.join(tmp, f'stamp_{name}.mov')
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-framerate', str(FPS), '-i',
                        os.path.join(frames_dir, '%02d.png'), '-c:v', 'qtrle', mov], check=True)


def render(out, tmp):
    os.makedirs(tmp, exist_ok=True)
    parts = []
    for i, ((t, src, st), n) in enumerate(zip(SHOTS, frames())):
        p = os.path.join(tmp, f's{i:02d}.mp4')
        parts.append(p)
        vf = f'fps={FPS},scale={W}:{H}:flags=lanczos,{GRADE},setsar=1'
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{st:.3f}', '-i', src, '-frames:v', str(n),
                        '-an', '-vf', vf, '-c:v', 'libx264', '-crf', '10', '-preset', 'fast', '-pix_fmt', 'yuv420p', p], check=True)
    lst = os.path.join(tmp, 'list.txt')
    open(lst, 'w').write(''.join(f"file '{p}'\n" for p in parts))
    vid = os.path.join(tmp, 'video.mp4')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', lst, '-c', 'copy', vid], check=True)
    build_stamps(tmp)
    # overlay four stamps. third is gold.
    cmd = ['ffmpeg', '-v', 'error', '-y', '-i', vid]
    stamps = []
    for i, t in enumerate(STAMPS):
        color = 'gold' if i == 2 else 'white'
        cmd += ['-i', os.path.join(tmp, f'stamp_{color}.mov')]
        stamps.append(t)
    # chain overlays
    fc = ''
    last = '0:v'
    for i, t in enumerate(stamps):
        tag = f's{i}'
        fc += f"[{i+1}:v]setpts=PTS+{t:.3f}/TB[{tag}];"
        outv = 'vout' if i == len(stamps) - 1 else f'v{i}'
        fc += f"[{last}][{tag}]overlay=0:0:enable='between(t,{t:.3f},{t+0.52:.3f})'[{outv}];"
        last = outv
    fc += f"[4:a]anull[a]"  # placeholder replaced below
    # audio is input index 5
    cmd += ['-i', SONG]
    audio_idx = 1 + len(stamps)
    fc = fc.replace('[4:a]', f'[{audio_idx}:a]')
    fc = fc[:-1]  # drop trailing semicolon from the anull line if I added one... check
    # rebuild cleanly
    fc = ''
    last = '0:v'
    for i, t in enumerate(stamps):
        tag = f's{i}'
        fc += f"[{i+1}:v]setpts=PTS+{t:.3f}/TB[{tag}];"
        outv = 'vout' if i == len(stamps) - 1 else f'v{i}'
        fc += f"[{last}][{tag}]overlay=0:0:enable='between(t,{t:.3f},{t+0.52:.3f})'[{outv}];"
        last = outv
    fc += f"[{audio_idx}:a]atrim=0:{END:.3f},afade=t=out:st={END-0.5:.3f}:d=0.5[a]"
    cmd += ['-filter_complex', fc, '-map', '[vout]', '-map', '[a]', '-t', f'{END:.3f}',
            '-c:v', 'libx264', '-crf', '10', '-preset', 'slow', '-pix_fmt', 'yuv420p',
            '-c:a', 'aac', '-b:a', '256k', out]
    subprocess.run(cmd, check=True)
    print(out)


if __name__ == '__main__':
    check()
    if len(sys.argv) > 1 and sys.argv[1] == 'check':
        sys.exit(0)
    render('/tmp/out/grok_i_get_it.mp4', '/tmp/tmp_igetit')
