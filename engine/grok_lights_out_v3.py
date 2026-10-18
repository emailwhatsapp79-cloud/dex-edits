"""F1 v3 - LIGHTS OUT. Five reds go out in the first two seconds, then 2026 starts
from six different Grands Prix. Ends on AUSTIN. TODAY. No picture of Austin.
formula1.com 1280x720 50 fps, kept 1:1. Master is 50. TikTok brand is 30.
YouTube Short is 50. Song #5 is instrumental. No lap counter, no timing tower.
Small F1 bug and trackside sponsors stay. Ranges do not overlap around-the-world."""
import os, subprocess, sys

S = os.environ.get('SCRATCH', '/tmp')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.environ.get('DEX_ASSETS', os.path.join(os.path.dirname(ROOT), 'dex-edits-assets'))
D = os.path.join(S, 'dexsrc', 'f1')
SONG = os.path.join(ASSETS, 'songs', '05_montagem_kali_slowed.m4a')
FONT = os.path.join(ROOT, 'fonts', 'Anton.ttf')
FPS = int(os.environ.get('DEX_FPS', '50'))
# (file, src_t). Edit cuts are the frame list. One clean take each.
# Monaco lights on at 3.22, out by ~4.4 (inside the first 1.2s). RACE bug is at 6.2, we stop at 5.06.
# Singapore launch ends at 9.00; the RACE bug is on screen at 9.35.
# Spain hold: lights still on at 6.60, cars gone by 9.00, source cut at 9.2.
SHOTS = [
    ('monaco', 3.22),
    ('singapore', 6.94),
    ('austria', 1.50),
    ('sepang', 3.40),
    ('baku', 1.70),
    ('spain', 4.32),
]
# Hits 1.840, 3.900, 5.640, 8.580, 10.340, 15.040 are exact 50 fps frames.
FRAMES = [0, 92, 195, 282, 429, 517, 752]
END = FRAMES[-1] / FPS
GRADE = 'eq=contrast=1.10:saturation=1.08:gamma=0.94,unsharp=3:3:0.25'
TEXT = [
    (0.00, FRAMES[5] / FPS, 'LIGHTS OUT', 54, 0.80),
    (FRAMES[5] / FPS, END, 'AUSTIN. TODAY.', 58, 0.80),
]


def dt(t0, t1, text, fs, y):
    text = text.replace("'", '’').replace(':', '\\:').replace(',', '\\,')
    return (f",drawtext=fontfile={FONT}:text='{text}':fontsize={fs}:fontcolor=white:borderw=3:bordercolor=black@0.55:"
            f"shadowcolor=black@0.55:shadowy=3:x=(w-text_w)/2:y=h*{y}:enable='between(t,{t0:.3f},{t1:.3f})'")


def spans():
    return [b - a for a, b in zip(FRAMES, FRAMES[1:])]


def main(mode='render'):
    os.makedirs(os.path.join(S, 'out'), exist_ok=True)
    ns = spans()
    if mode == 'check':
        used = {}
        for (name, st), n, fr in zip(SHOTS, ns, FRAMES):
            d = n / FPS
            print(f'{fr / FPS:6.3f} {d:5.2f}s {name:12} @{st:.2f} -> {st + d:.2f}')
            for a, b in used.get(name, []):
                assert st + d <= a + 1e-3 or st >= b - 1e-3, name
            used.setdefault(name, []).append((st, st + d))
        print('end', round(END, 3), 'fps', FPS)
        return
    if mode == 'stills':
        from PIL import Image, ImageDraw
        import io
        ims = []
        for (name, st), n, fr in zip(SHOTS, ns, FRAMES):
            for label, t in (('in', st + 0.02), ('out', st + n / FPS - 0.06)):
                p = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{t:.3f}', '-i', os.path.join(D, name + '.mp4'),
                                    '-frames:v', '1', '-vf', 'scale=400:-2', '-f', 'image2pipe', '-vcodec', 'mjpeg', '-'],
                                   capture_output=True)
                im = Image.open(io.BytesIO(p.stdout)).convert('RGB')
                c = Image.new('RGB', (im.width, im.height + 16), (0, 0, 0))
                c.paste(im, (0, 16))
                ImageDraw.Draw(c).text((4, 1), f'{label} {name} {t:.2f}', fill=(255, 220, 0))
                ims.append(c)
        cols = 4
        sheet = Image.new('RGB', (cols * ims[0].width, 3 * ims[0].height), (0, 0, 0))
        for i, im in enumerate(ims):
            sheet.paste(im, ((i % cols) * ims[0].width, (i // cols) * ims[0].height))
        out = '/workspace/screenshots/v3/lights_stills.jpg'
        sheet.save(out, quality=84)
        print(out)
        return
    inp, fc, cat = [], '', ''
    for i, ((name, st), n) in enumerate(zip(SHOTS, ns)):
        inp += ['-ss', f'{st:.3f}', '-i', os.path.join(D, name + '.mp4')]
        fc += f'[{i}:v]fps={FPS},trim=end_frame={n},setpts=PTS-STARTPTS,{GRADE},setsar=1[v{i}];'
        cat += f'[v{i}]'
    k = len(SHOTS)
    fc += f'{cat}concat=n={k}:v=1:a=0[vc];[vc]fade=t=out:st={END - 0.8:.3f}:d=0.8' + ''.join(dt(*x) for x in TEXT) + '[v];'
    inp += ['-i', SONG]
    fc += f"[{k}:a]atrim=0:{END:.3f},asetpts=PTS-STARTPTS,afade=t=out:st={END - 0.8:.3f}:d=0.8[a]"
    master = os.path.join(S, 'out', 'grok_lights_out_v3.mp4')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', *inp, '-filter_complex', fc, '-map', '[v]', '-map', '[a]',
                    '-t', f'{END:.3f}', '-r', str(FPS), '-c:v', 'libx264', '-crf', '12', '-preset', 'fast',
                    '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '256k', master], check=True)
    import brand, ytshort
    tik = os.path.join(ROOT, 'grok', '2026-10-25-lights-out.mp4')
    yt = os.path.join(ROOT, 'grok', '2026-10-25-lights-out-yt.mp4')
    print(brand.brand(master, tik, fps=30))
    print(ytshort.make(master, yt, 'LIGHTS OUT|AUSTIN. TODAY.', fps=FPS))


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else 'render')
