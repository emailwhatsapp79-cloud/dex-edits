"""FOOTBALL v2 - Kevin Pina, Cape Verde 6. One goal: from range, into the net, then the celebration held.
Official @fifaworldcup caption names him ("Kevin Pina from WAY out"). The shirt on the celebration is red 6,
which is his 2026 number, against Uruguay in sky blue. Native 1080x1920, nothing scaled or cropped.
Song #37 is instrumental until "thank you for watching" at 16.48s, so the edit ends at 15.77s.
Source commentary is muted."""
import os, subprocess, sys

S = os.environ.get('SCRATCH', '/tmp')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.environ.get('DEX_ASSETS', os.path.join(os.path.dirname(ROOT), 'dex-edits-assets'))
SRC = os.path.join(S, 'dexsrc', 'fw_7693949914702679318.mp4')
SONG = os.path.join(ASSETS, 'songs', '37_montagem_rune_slowed.mp3')
FONT = os.path.join(ROOT, 'fonts', 'Anton.ttf')
# Source cuts at 10.00 and 14.00. One window per take.
# (src_t, edit_t). Durations come from the frame grid below.
SHOTS = [
    (2.40, 0.000),    # the range. he is on the ball by the end of the take
    (10.18, 7.433),   # DROP. the goal, then he runs
    (14.30, 10.833),  # the celebration, held. red 6, face in frame
]
END = 15.767
GRADE = 'eq=contrast=1.10:saturation=1.08:gamma=0.94,unsharp=3:3:0.25'
TEXT = [
    (0.00, 7.40, 'PINA', 150, 0.38),
    (0.00, 7.40, 'WAY OUT', 92, 0.50),
    (7.43, 10.80, 'GOAL.', 140, 0.40),
]


def dt(t0, t1, text, fs, y):
    text = text.replace("'", '’').replace(':', '\\:').replace(',', '\\,')
    return (f",drawtext=fontfile={FONT}:text='{text}':fontsize={fs}:fontcolor=white:borderw=4:bordercolor=black@0.55:"
            f"shadowcolor=black@0.6:shadowy=4:x=(w-text_w)/2:y=h*{y}:enable='between(t,{t0},{t1})'")


def spans():
    ts = [t for _, t in SHOTS] + [END]
    fr = [round(t * 30) for t in ts]
    return [b - a for a, b in zip(fr, fr[1:])]


def main(mode='render'):
    os.makedirs(os.path.join(S, 'out'), exist_ok=True)
    os.makedirs(os.path.join(S, 'qc'), exist_ok=True)
    ns = spans()
    if mode == 'check':
        used = []
        for (st, t), n in zip(SHOTS, ns):
            d = n / 30
            print(f'{t:6.2f} {d:5.2f}s @{st:.2f} -> {st+d:.2f}')
            for a, b in used:
                assert st + d <= a or st >= b, 'overlap'
            used.append((st, st + d))
        return
    if mode == 'stills':
        from PIL import Image, ImageDraw
        import io
        ims = []
        for (st, t), n in zip(SHOTS, ns):
            mid = st + (n / 30) / 2
            p = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{mid:.3f}', '-i', SRC, '-frames:v', '1',
                                '-vf', 'scale=270:-2,' + GRADE, '-f', 'image2pipe', '-vcodec', 'mjpeg', '-'], capture_output=True)
            im = Image.open(io.BytesIO(p.stdout)).convert('RGB')
            ImageDraw.Draw(im).text((8, 8), f'{t:.2f} @{st:.2f}', fill=(255, 220, 0))
            ims.append(im)
        Sht = Image.new('RGB', (ims[0].width * len(ims), ims[0].height))
        for i, im in enumerate(ims):
            Sht.paste(im, (i * ims[0].width, 0))
        out = os.path.join(S, 'qc', 'grok_pina_v2_stills.jpg')
        Sht.save(out, quality=88)
        print(out)
        return
    inp, fc, cat = [], '', ''
    for i, ((st, _), n) in enumerate(zip(SHOTS, ns)):
        inp += ['-ss', f'{st:.3f}', '-i', SRC]
        fc += f'[{i}:v]fps=30,trim=end_frame={n},setpts=PTS-STARTPTS,{GRADE},setsar=1[v{i}];'
        cat += f'[v{i}]'
    k = len(SHOTS)
    fc += f'{cat}concat=n={k}:v=1:a=0[vc];[vc]fade=t=out:st={END - 0.8:.3f}:d=0.8' + ''.join(dt(*x) for x in TEXT) + '[v];'
    inp += ['-i', SONG]
    fc += f"[{k}:a]atrim=0:{END},asetpts=PTS-STARTPTS,afade=t=out:st={END - 0.8:.3f}:d=0.8[a]"
    out = os.path.join(S, 'out', 'grok_pina_way_out_v2.mp4')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', *inp, '-filter_complex', fc, '-map', '[v]', '-map', '[a]',
                    '-t', f'{END}', '-c:v', 'libx264', '-crf', '10', '-preset', 'slow', '-pix_fmt', 'yuv420p',
                    '-c:a', 'aac', '-b:a', '256k', out], check=True)
    import brand
    print(brand.brand(out, out.replace('.mp4', '_DEX.mp4')))


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else 'render')
