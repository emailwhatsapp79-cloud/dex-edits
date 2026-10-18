"""F1 v3 - AROUND THE WORLD. One 2026 track per shot. The line is song #100,
'Bound the Wheels Around the World', and the bracket builds on those words, then stays.
formula1.com 1280x720 50 fps, kept 1:1. Master is 50. TikTok brand is 30. YouTube Short is 50.
No lap counter, no timing tower, no speed ramp. Ranges do not overlap lights-out.
Harbour opens it. The night aerial is held to the fade."""
import os, subprocess, sys

S = os.environ.get('SCRATCH', '/tmp')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.environ.get('DEX_ASSETS', os.path.join(os.path.dirname(ROOT), 'dex-edits-assets'))
D = os.path.join(S, 'dexsrc', 'f1')
SONG = os.path.join(ASSETS, 'songs', '100_simple_edit_mb_i_ve_been_busy_scp_piastr.mp3')
FONT = os.path.join(ROOT, 'fonts', 'Anton.ttf')
FPS = int(os.environ.get('DEX_FPS', '50'))
# Cuts snapped early of hits 5.830, 9.798, 11.688. The edit holds to 15.28.
# A red SINGAPORE banner sits in the night reel around 106.3-107.0, so the
# night shot starts after it, on the clean aerial, and stops before the next angle.
# Harbour is clean through 465.7 (the ident is at 466.5). Barcelona stops before 5.36.
SHOTS = [
    ('monaco', 459.90),
    ('barcelona', 1.18),
    ('sepang', 14.32),
    ('singapore', 107.55),
]
FRAMES = [0, 291, 489, 584, 764]  # 0, 5.820, 9.780, 11.680, 15.280
END = FRAMES[-1] / FPS
GRADE = 'eq=contrast=1.10:saturation=1.08:gamma=0.94,unsharp=3:3:0.25'
# The vocal says Bound / the / Wheels before Around. The bracket waits for the word.
TEXT = [
    (2.46, 3.10, '[AROUND]', 42, 0.82),
    (3.10, 3.92, '[AROUND THE]', 42, 0.82),
    (3.92, END, '[AROUND THE WORLD]', 42, 0.82),
]


def dt(t0, t1, text, fs, y):
    text = text.replace("'", '’').replace(':', '\\:').replace(',', '\\,').replace('[', '\\[').replace(']', '\\]')
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
            for label, t in (('in', st + 0.04), ('out', st + n / FPS - 0.08)):
                p = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{t:.3f}', '-i', os.path.join(D, name + '.mp4'),
                                    '-frames:v', '1', '-vf', 'scale=400:-2', '-f', 'image2pipe', '-vcodec', 'mjpeg', '-'],
                                   capture_output=True)
                im = Image.open(io.BytesIO(p.stdout)).convert('RGB')
                c = Image.new('RGB', (im.width, im.height + 16), (0, 0, 0))
                c.paste(im, (0, 16))
                ImageDraw.Draw(c).text((4, 1), f'{label} {name} {t:.2f}', fill=(255, 220, 0))
                ims.append(c)
        cols = 5
        sheet = Image.new('RGB', (cols * ims[0].width, 2 * ims[0].height), (0, 0, 0))
        for i, im in enumerate(ims):
            sheet.paste(im, ((i % cols) * ims[0].width, (i // cols) * ims[0].height))
        out = '/workspace/screenshots/v3/around_stills.jpg'
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
    master = os.path.join(S, 'out', 'grok_around_the_world_v3.mp4')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', *inp, '-filter_complex', fc, '-map', '[v]', '-map', '[a]',
                    '-t', f'{END:.3f}', '-r', str(FPS), '-c:v', 'libx264', '-crf', '12', '-preset', 'fast',
                    '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '256k', master], check=True)
    import brand, ytshort
    tik = os.path.join(ROOT, 'grok', '2026-10-24-around-the-world.mp4')
    yt = os.path.join(ROOT, 'grok', '2026-10-24-around-the-world-yt.mp4')
    print(brand.brand(master, tik, fps=30))
    print(ytshort.make(master, yt, 'AROUND|THE WORLD', fps=FPS))


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else 'render')
