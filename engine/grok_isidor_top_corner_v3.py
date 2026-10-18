"""FOOTBALL v3 - Wilson Isidor, Haiti 18. One goal: the top corner, then the celebration held.
Official @fifaworldcup caption names him. The celebration is a blue 18. The pile also shows
Joseph 16, 17 and 22, so the edit does not stamp a number. Native 1080x1920, source is 30 fps.
Song #5 is instrumental. Ends at 15.03s, before any lyric."""
import os, subprocess, sys

S = os.environ.get('SCRATCH', '/tmp')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.environ.get('DEX_ASSETS', os.path.join(os.path.dirname(ROOT), 'dex-edits-assets'))
SRC = os.path.join(S, 'dexsrc', 'fw_7694302696496532758.mp4')
SONG = os.path.join(ASSETS, 'songs', '05_montagem_kali_slowed.m4a')
FONT = os.path.join(ROOT, 'fonts', 'Anton.ttf')
FPS = 30
# Real source cuts: 4.33, 6.33, 7.93, 11.1, 16.23, 18.57. One window per take.
# (src_t, edit frame). Durations are the gaps on the 30 fps grid.
# Hits: 2.867, 5.658, 10.343, 12.658, 15.048. Cuts are on the frame, never late.
FRAMES = [0, 86, 169, 310, 379, 451]  # 0, 2.867, 5.633, 10.333, 12.633, 15.033
SRC_T = [8.10, 1.00, 11.49, 16.26, 18.62]
END = FRAMES[-1] / FPS
GRADE = 'eq=contrast=1.10:saturation=1.08:gamma=0.94,unsharp=3:3:0.25'
# TOP CORNER only while the ball is in the net. The name stays. No number.
TEXT = [
    (0.00, END, 'ISIDOR', 118, 0.74),
    (0.00, FRAMES[1] / FPS, 'TOP CORNER', 72, 0.82),
]


def dt(t0, t1, text, fs, y):
    text = text.replace("'", '’').replace(':', '\\:').replace(',', '\\,')
    return (f",drawtext=fontfile={FONT}:text='{text}':fontsize={fs}:fontcolor=white:borderw=4:bordercolor=black@0.55:"
            f"shadowcolor=black@0.6:shadowy=4:x=(w-text_w)/2:y=h*{y}:enable='between(t,{t0:.3f},{t1:.3f})'")


def spans():
    return [b - a for a, b in zip(FRAMES, FRAMES[1:])]


def main(mode='render'):
    os.makedirs(os.path.join(S, 'out'), exist_ok=True)
    ns = spans()
    if mode == 'check':
        used = []
        for st, n, fr in zip(SRC_T, ns, FRAMES):
            d = n / FPS
            print(f'{fr / FPS:6.3f} {d:5.2f}s @{st:.2f} -> {st + d:.2f}')
            for a, b in used:
                assert st + d <= a + 1e-3 or st >= b - 1e-3, 'overlap'
            used.append((st, st + d))
        print('end', round(END, 3))
        return
    if mode == 'stills':
        from PIL import Image, ImageDraw
        import io
        ims = []
        for st, n, fr in zip(SRC_T, ns, FRAMES):
            for label, t in (('in', st + 0.04), ('mid', st + n / FPS / 2)):
                p = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{t:.3f}', '-i', SRC, '-frames:v', '1',
                                    '-vf', 'scale=270:-2', '-f', 'image2pipe', '-vcodec', 'mjpeg', '-'], capture_output=True)
                im = Image.open(io.BytesIO(p.stdout)).convert('RGB')
                ImageDraw.Draw(im).text((6, 6), f'{label} {fr / FPS:.2f} @{t:.2f}', fill=(255, 220, 0))
                ims.append(im)
        sheet = Image.new('RGB', (ims[0].width * 5, ims[0].height * 2))
        for i, im in enumerate(ims):
            sheet.paste(im, ((i % 5) * ims[0].width, (i // 5) * ims[0].height))
        out = os.path.join(ROOT, '..', '..', 'screenshots', 'v3', 'isidor_stills.jpg')
        os.makedirs(os.path.dirname(out), exist_ok=True)
        # screenshots live at /workspace/screenshots
        out = '/workspace/screenshots/v3/isidor_stills.jpg'
        sheet.save(out, quality=86)
        print(out)
        return
    inp, fc, cat = [], '', ''
    for i, (st, n) in enumerate(zip(SRC_T, ns)):
        inp += ['-ss', f'{st:.3f}', '-i', SRC]
        fc += f'[{i}:v]fps={FPS},trim=end_frame={n},setpts=PTS-STARTPTS,{GRADE},setsar=1[v{i}];'
        cat += f'[v{i}]'
    k = len(SRC_T)
    fc += f'{cat}concat=n={k}:v=1:a=0[vc];[vc]fade=t=out:st={END - 0.8:.3f}:d=0.8' + ''.join(dt(*x) for x in TEXT) + '[v];'
    inp += ['-i', SONG]
    fc += f"[{k}:a]atrim=0:{END:.3f},asetpts=PTS-STARTPTS,afade=t=out:st={END - 0.8:.3f}:d=0.8[a]"
    out = os.path.join(S, 'out', 'grok_isidor_top_corner_v3.mp4')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', *inp, '-filter_complex', fc, '-map', '[v]', '-map', '[a]',
                    '-t', f'{END:.3f}', '-c:v', 'libx264', '-crf', '12', '-preset', 'fast', '-pix_fmt', 'yuv420p',
                    '-c:a', 'aac', '-b:a', '256k', out], check=True)
    import brand
    dst = os.path.join(ROOT, 'grok', '2026-10-24-isidor-top-corner.mp4')
    print(brand.brand(out, dst, fps=30))


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else 'render')
