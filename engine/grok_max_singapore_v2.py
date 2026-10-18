"""F1 v2 - Max Verstappen, Singapore 2026. Not Austin, not a race week, no timing tower.
M21 shape: black title cards on the beat, then one driver. The race is already run (11 Oct 2026):
he won it, his first Singapore Grand Prix, from pole. Official @f1 TikTok of that weekend.
Native 1080x1920 (the file is 50 fps; this export is 30). No crop, no upscale.
Frames with a lap counter, a position board or a panning smear are not used.
Song #5 is instrumental, so the cards are ours and they are not fighting a voice."""
import os, subprocess, sys

S = os.environ.get('SCRATCH', '/tmp')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.environ.get('DEX_ASSETS', os.path.join(os.path.dirname(ROOT), 'dex-edits-assets'))
SRC = os.path.join(S, 'dexsrc', 'f1_7696506664224296214.mp4')
SONG = os.path.join(ASSETS, 'songs', '05_montagem_kali_slowed.m4a')
FONT = os.path.join(ROOT, 'fonts', 'Anton.ttf')
# (kind, src_t or '', edit_t). Cards are black. Footage takes:
# garage 0.00-2.12, helmet 2.12-6.25 (stop before the burned quote), wide 8.75-11.62, podium 39.50-end.
SHOTS = [
    ('card', '', 0.000),
    ('card', '', 1.833),
    ('card', '', 3.900),
    ('vid', 0.45, 5.667),
    ('vid', 2.40, 7.133),
    ('vid', 8.92, 8.600),
    ('vid', 39.72, 11.233),
]
END = 15.033
GRADE = 'hue=s=0,eq=contrast=1.08:gamma=0.97,unsharp=3:3:0.2'
TEXT = [
    (0.00, 1.80, 'MAX', 160),
    (1.83, 3.85, 'SINGAPORE', 110),
    (3.90, 5.60, 'FIRST WIN', 120),
]


def dt(t0, t1, text, fs):
    text = text.replace("'", '’').replace(':', '\\:').replace(',', '\\,')
    return (f",drawtext=fontfile={FONT}:text='{text}':fontsize={fs}:fontcolor=white:"
            f"x=(w-text_w)/2:y=(h-text_h)/2:enable='between(t,{t0},{t1})'")


def spans():
    ts = [t for *_, t in SHOTS] + [END]
    fr = [round(t * 30) for t in ts]
    return [b - a for a, b in zip(fr, fr[1:])]


def main(mode='render'):
    os.makedirs(os.path.join(S, 'out'), exist_ok=True)
    os.makedirs(os.path.join(S, 'qc'), exist_ok=True)
    ns = spans()
    if mode == 'check':
        for (kind, st, t), n in zip(SHOTS, ns):
            d = n / 30
            print(f'{t:6.2f} {d:5.2f}s {kind:4} {st}')
        return
    if mode == 'stills':
        from PIL import Image, ImageDraw
        import io
        ims = []
        for (kind, st, t), n in zip(SHOTS, ns):
            if kind == 'card':
                im = Image.new('RGB', (270, 480), (0, 0, 0))
            else:
                mid = float(st) + (n / 30) / 2
                p = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{mid:.3f}', '-i', SRC, '-frames:v', '1',
                                    '-vf', 'scale=270:-2,' + GRADE, '-f', 'image2pipe', '-vcodec', 'mjpeg', '-'], capture_output=True)
                im = Image.open(io.BytesIO(p.stdout)).convert('RGB')
            ImageDraw.Draw(im).text((8, 8), f'{t:.2f}', fill=(255, 220, 0))
            ims.append(im)
        Sht = Image.new('RGB', (270 * len(ims), 480))
        for i, im in enumerate(ims):
            Sht.paste(im, (i * 270, 0))
        out = os.path.join(S, 'qc', 'grok_max_v2_stills.jpg')
        Sht.save(out, quality=88)
        print(out)
        return
    inp, fc, cat = [], '', ''
    for i, ((kind, st, _), n) in enumerate(zip(SHOTS, ns)):
        if kind == 'card':
            inp += ['-f', 'lavfi', '-t', f'{n/30 + 0.1:.3f}', '-i', 'color=c=black:s=1080x1920:r=30']
            fc += f'[{i}:v]fps=30,trim=end_frame={n},setpts=PTS-STARTPTS,setsar=1[v{i}];'
        else:
            inp += ['-ss', f'{float(st):.3f}', '-i', SRC]
            fc += f'[{i}:v]fps=30,trim=end_frame={n},setpts=PTS-STARTPTS,{GRADE},setsar=1[v{i}];'
        cat += f'[v{i}]'
    k = len(SHOTS)
    fc += f'{cat}concat=n={k}:v=1:a=0[vc];[vc]fade=t=out:st={END - 0.8:.3f}:d=0.8' + ''.join(dt(*x) for x in TEXT) + '[v];'
    inp += ['-i', SONG]
    fc += f"[{k}:a]atrim=0:{END},asetpts=PTS-STARTPTS,afade=t=out:st={END - 0.8:.3f}:d=0.8[a]"
    out = os.path.join(S, 'out', 'grok_max_singapore_v2.mp4')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', *inp, '-filter_complex', fc, '-map', '[v]', '-map', '[a]',
                    '-t', f'{END}', '-c:v', 'libx264', '-crf', '10', '-preset', 'slow', '-pix_fmt', 'yuv420p',
                    '-c:a', 'aac', '-b:a', '256k', out], check=True)
    import brand
    print(brand.brand(out, out.replace('.mp4', '_DEX.mp4')))


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else 'render')
