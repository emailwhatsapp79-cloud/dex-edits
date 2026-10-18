"""F1 v2 - I get it. Max Verstappen.
Donut opener and the M26 stamps stay. The wide finish lines are gone.
After the smoke, every shot is a close one: his Singapore onboard (name tag
cropped), arms up in the 2023 car, the 2022 cockpit, then Max himself.
Sound #105. Stamps at 0.48 / 2.80 / 5.34 / 7.36. Third stamp gold. No blur.
Master 1280x720, 50 fps, 1:1. Cuts snapped early onto the hits in this file.
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
SONG = '/tmp/dexsrc/song105.wav'
D23 = '/tmp/dexsrc/f1_donuts23.mp4'
D22 = '/tmp/dexsrc/max_donuts22.mp4'
ONB = '/tmp/dexsrc/f1_sg_onboards.mp4'
# (edit t snapped with int(hit*FPS)/FPS, src, src_t, crop or None)
# crop is (w, h, x, y) before the scale back to 1280x720.
# Onboard name tag sits in the lowest ~110 px. Cropping it is ~1.18x.
SHOTS = [
    (0.000, D23, 2.200, None),                 # tyre smoke, the hook
    (3.340, ONB, 9.550, (1280, 610, 0, 0)),    # his car fills the frame
    (4.740, D23, 12.600, None),                # arms up, the #1 fills it
    (7.480, D22, 10.100, None),                # 2022 cockpit
    (9.900, D23, 18.300, None),                # Max himself, 1.00 s
]
STAMPS = [0.48, 2.80, 5.34, 7.36]
GRADE = 'eq=contrast=1.10:saturation=1.08:gamma=0.94,unsharp=3:3:0.25'
# one clean take each. Tight, so a shot cannot cross a cut.
LIMITS = {
    D23: [(1.5, 7.2), (12.50, 15.40), (17.8, 20.2)],
    D22: [(9.95, 12.55)],
    ONB: [(9.40, 11.28)],
}


def frames():
    ts = [s[0] for s in SHOTS] + [END]
    fr = [round(t * FPS) for t in ts]
    return [b - a for a, b in zip(fr, fr[1:])]


def check():
    used = {}
    prev = None
    counts = {}
    for (t, src, st, crop), n in zip(SHOTS, frames()):
        d = n / FPS
        assert d > 0.3, t
        name = os.path.basename(src)
        ok = False
        for a, b in LIMITS[src]:
            if st >= a - 0.02 and st + d <= b + 0.02:
                ok = True
        assert ok, f'outside a clean take {name} {st}+{d:.2f}'
        for a, b in used.get(src, []):
            assert st + d <= a + 0.02 or st >= b - 0.02, f'overlap {name} {st}'
        used.setdefault(src, []).append((st, st + d))
        counts[name] = counts.get(name, 0) + 1
        assert prev != src, f'same source twice in a row {name}'
        prev = src
        print(f'{t:6.2f} {d:5.2f}s {name[:22]:22} @{st:6.2f}')
    assert SHOTS[-1][0] >= END - 1.21
    for k, v in counts.items():
        assert v <= 3, k
        print(f'  {v} x {k}')


def _stamp_frame(color, scale, font):
    layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    col = color + (255,)
    for inset, width in ((34, 3), (50, 2)):
        d.rectangle([inset, inset, W - 1 - inset, H - 1 - inset], outline=col, width=width)
    bx, by, bw, bh = W // 2 - 250, H // 2 - 160, 18, 320
    d.rectangle([bx, by, bx + bw, by + bh], fill=col)
    x = bx + bw + 28
    y_it = H // 2 - 150
    d.text((x, y_it), 'IT', font=font, fill=col)
    d.text((x, y_it + 150), 'GET', font=font, fill=col)
    if abs(scale - 1) < 0.01:
        return layer
    nw, nh = int(W * scale), int(H * scale)
    canvas = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    big = layer.resize((nw, nh), Image.Resampling.LANCZOS)
    canvas.paste(big, ((W - nw) // 2, (H - nh) // 2), big)
    return canvas


def build_stamps(tmp):
    font = ImageFont.truetype(FONT, 150)
    white, gold = (255, 255, 255), (212, 168, 72)
    for name, color in (('white', white), ('gold', gold)):
        frames_dir = os.path.join(tmp, name)
        os.makedirs(frames_dir, exist_ok=True)
        seq = []
        for i in range(8):
            seq.append(_stamp_frame(color, 1.14 - 0.14 * (i / 7), font))
        hold = _stamp_frame(color, 1.0, font)
        seq += [hold] * 18
        for i, im in enumerate(seq):
            im.save(os.path.join(frames_dir, f'{i:02d}.png'))
        mov = os.path.join(tmp, f'stamp_{name}.mov')
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-framerate', str(FPS), '-i',
                        os.path.join(frames_dir, '%02d.png'), '-c:v', 'qtrle', mov], check=True)


def render(out, tmp):
    os.makedirs(tmp, exist_ok=True)
    parts = []
    for i, ((t, src, st, crop), n) in enumerate(zip(SHOTS, frames())):
        p = os.path.join(tmp, f's{i:02d}.mp4')
        parts.append(p)
        if crop:
            cw, ch, cx, cy = crop
            vf = f'crop={cw}:{ch}:{cx}:{cy},scale={W}:{H}:flags=lanczos,fps={FPS},{GRADE},setsar=1'
        else:
            vf = f'fps={FPS},scale={W}:{H}:flags=lanczos,{GRADE},setsar=1'
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{st:.3f}', '-i', src, '-frames:v', str(n),
                        '-an', '-vf', vf, '-c:v', 'libx264', '-crf', '10', '-preset', 'fast', '-pix_fmt', 'yuv420p', p], check=True)
    lst = os.path.join(tmp, 'list.txt')
    open(lst, 'w').write(''.join(f"file '{p}'\n" for p in parts))
    vid = os.path.join(tmp, 'video.mp4')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', lst, '-c', 'copy', vid], check=True)
    build_stamps(tmp)
    cmd = ['ffmpeg', '-v', 'error', '-y', '-i', vid]
    for i, _t in enumerate(STAMPS):
        color = 'gold' if i == 2 else 'white'
        cmd += ['-i', os.path.join(tmp, f'stamp_{color}.mov')]
    cmd += ['-i', SONG]
    audio_idx = 1 + len(STAMPS)
    fc = ''
    last = '0:v'
    for i, t in enumerate(STAMPS):
        tag = f's{i}'
        fc += f"[{i+1}:v]setpts=PTS+{t:.3f}/TB[{tag}];"
        outv = 'vout' if i == len(STAMPS) - 1 else f'v{i}'
        fc += f"[{last}][{tag}]overlay=0:0:enable='between(t,{t:.3f},{t+0.52:.3f})'[{outv}];"
        last = outv
    fc += f"[{audio_idx}:a]atrim=0:{END:.3f},afade=t=out:st={END-0.45:.3f}:d=0.45[a]"
    cmd += ['-filter_complex', fc, '-map', '[vout]', '-map', '[a]', '-t', f'{END:.3f}',
            '-c:v', 'libx264', '-crf', '10', '-preset', 'slow', '-pix_fmt', 'yuv420p',
            '-c:a', 'aac', '-b:a', '256k', out]
    subprocess.run(cmd, check=True)
    print(out)


if __name__ == '__main__':
    check()
    if len(sys.argv) > 1 and sys.argv[1] == 'check':
        sys.exit(0)
    render('/tmp/out/grok_i_get_it_v2.mp4', '/tmp/tmp_igetit_v2')
