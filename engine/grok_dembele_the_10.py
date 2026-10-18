"""FOOTBALL - Ousmane Dembélé, the number 10. One story: the first World Cup goal, then the hat-trick.
VERTICAL native 1080x1920 from official @fifaworldcup clips. Nothing cropped, nothing scaled.
Song #37 (Montagem Rune, slowed) is instrumental until a 'thanks for watching' sting at 16.5s.
The hat-trick clip is only 6.7s with one cut, so the edit lands at 13.49s (inside 12-22s) instead of
being padded. The drop (7.42) cuts to the hat-trick. Source commentary is muted: the words on screen
are ours and they are not fighting a voice."""
import os, subprocess, sys

S = os.environ.get('SCRATCH', '/tmp')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.environ.get('DEX_ASSETS', os.path.join(os.path.dirname(ROOT), 'dex-edits-assets'))
F = os.path.join(S, 'dexsrc', 'fwc_7654401416228031747.mp4')   # first World Cup goal
H = os.path.join(S, 'dexsrc', 'fwc_7666790102982495510.mp4')   # the hat-trick
SONG = os.path.join(ASSETS, 'songs', '37_montagem_rune_slowed.mp3')
FONT = os.path.join(ROOT, 'fonts', 'Anton.ttf')
# (src, in, dur). Joins sit on song #37's beats. 7.42 is the drop: cut to the hat-trick.
# The hat-trick clip is 6.7s with one cut at 3.84, so each side is used once. Edit lands at 13.49s.
SHOTS = [
    (F, 4.45, 1.89),    # 0.00 THE 10. blue, on the ball
    (F, 6.45, 2.47),    # 1.89 the strike and the net
    (F, 9.20, 3.06),    # 4.36 FIRST. the celebration
    (H, 0.35, 2.47),    # 7.42 DROP AGAIN. number 10
    (H, 2.86, 0.94),    # 9.89 the finish, stops before the cut at 3.84
    (H, 4.02, 2.66),    # 10.83 HAT-TRICK.
]
TEXT = [
    (0.05, 1.85, 'THE 10.', 168, 0.40),
    (4.36, 7.35, 'FIRST.', 150, 0.40),
    (7.42, 9.80, 'AGAIN.', 140, 0.40),
    (10.83, 13.40, 'HAT-TRICK.', 112, 0.40),
]
END = 13.49


def dt(t0, t1, text, fs, y):
    text = text.replace("'", '’').replace(':', '\\:').replace(',', '\\,')
    return (f",drawtext=fontfile={FONT}:text='{text}':fontsize={fs}:fontcolor=white:borderw=4:bordercolor=black@0.55:"
            f"shadowcolor=black@0.6:shadowy=4:x=(w-text_w)/2:y=h*{y}:enable='between(t,{t0},{t1})'")


def main(mode='render'):
    os.makedirs(os.path.join(S, 'out'), exist_ok=True)
    os.makedirs(os.path.join(S, 'qc'), exist_ok=True)
    if mode == 'stills':
        from PIL import Image, ImageDraw
        import io
        ims = []
        acc = 0.0
        for src, a, d in SHOTS:
            p = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{a + d / 2:.3f}', '-i', src, '-frames:v', '1',
                                '-vf', 'scale=270:-2', '-f', 'image2pipe', '-vcodec', 'mjpeg', '-'], capture_output=True)
            im = Image.open(io.BytesIO(p.stdout)).convert('RGB')
            dr = ImageDraw.Draw(im)
            dr.rectangle((0, 0, 140, 18), fill=(0, 0, 0))
            dr.text((2, 2), f'{acc:.2f} @{a:.2f}', fill=(255, 220, 0))
            ims.append(im)
            acc += d
        tw, th = ims[0].size
        Sht = Image.new('RGB', (tw * len(ims), th))
        for i, im in enumerate(ims):
            Sht.paste(im, (i * tw, 0))
        out = os.path.join(S, 'qc', 'grok_dembele_stills.jpg')
        Sht.save(out, quality=88)
        print(out)
        return
    ts = [0.0]
    for _, _, d in SHOTS:
        ts.append(ts[-1] + d)
    # snap the joins to frames so the drop frame is the first frame of the net
    fr = [round(t * 30) for t in ts]
    # rebuild durations from the frame grid, last frame = END
    fr[-1] = round(END * 30)
    inp, fc, cat = [], '', ''
    for i, ((src, a, _), n) in enumerate(zip(SHOTS, [b - c for c, b in zip(fr, fr[1:])])):
        inp += ['-ss', f'{a:.3f}', '-i', src]
        fc += f'[{i}:v]fps=30,trim=end_frame={n},setpts=PTS-STARTPTS,setsar=1[v{i}];'
        cat += f'[v{i}]'
    k = len(SHOTS)
    fc += f'{cat}concat=n={k}:v=1:a=0[vc];[vc]null' + ''.join(dt(*x) for x in TEXT) + '[v];'
    inp += ['-i', SONG]
    fc += (f"[{k}:a]atrim=0:{END},asetpts=PTS-STARTPTS,afade=t=out:st={END - 0.8}:d=0.8[a]")
    out = os.path.join(S, 'out', 'grok_dembele_the_10.mp4')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', *inp, '-filter_complex', fc, '-map', '[v]', '-map', '[a]',
                    '-t', f'{END}', '-c:v', 'libx264', '-crf', '10', '-preset', 'slow', '-pix_fmt', 'yuv420p',
                    '-c:a', 'aac', '-b:a', '256k', out], check=True)
    sys.path.insert(0, os.path.dirname(__file__))
    import brand
    print(brand.brand(out, out.replace('.mp4', '_DEX.mp4')))


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else 'render')
