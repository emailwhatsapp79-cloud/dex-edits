"""F1 v5 - AROUND THE WORLD. Same pace and song as v4. Every shot re-picked so the
top-left is only the small F1 logo: no LAP line, no REPLAY, no timing tower.
formula1.com 1280x720 50 fps, kept 1:1. Master 50. TikTok brand 30. YouTube Short 50.
"""
import os, subprocess, sys

S = os.environ.get('SCRATCH', '/tmp')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.environ.get('DEX_ASSETS', os.path.join(os.path.dirname(ROOT), 'dex-edits-assets'))
D = os.path.join(S, 'dexsrc', 'f1')
SONG = os.path.join(ASSETS, 'songs', '100_simple_edit_mb_i_ve_been_busy_scp_piastr.mp3')
FONT = os.path.join(ROOT, 'fonts', 'Anton.ttf')
FPS = int(os.environ.get('DEX_FPS', '50'))
# Real percussive hits (beatsync), one frame early at 50 fps, never late.
# Two-beat spacing until the drop (~11.4), then one beat. Final hold < 2s.
HITS = [1.085, 2.175, 3.179, 4.210, 5.264, 6.303, 7.380, 8.397, 9.347, 10.452,
        11.398, 11.923, 12.436, 12.954, 13.478, 14.036, 14.604, 15.145, 15.726,
        16.272, 17.752]
# (file, src_t, TRACK). Each window is inside one take and was pixel-checked:
# 260x130 corner, logo only, no LAP text, no red REPLAY word.
# These source times do not overlap v4.
SHOTS = [
    ('japan',     416.50, 'SUZUKA'),       # McLaren onboard, the hook
    ('singapore', 112.72, 'SINGAPORE'),    # two cars, after the v3 range
    ('australia',  18.75, 'MELBOURNE'),    # field, after the 18.52 cut
    ('singapore',  97.22, 'SINGAPORE'),    # Haas onboard
    ('japan',       3.42, 'SUZUKA'),       # race start, cars moving
    ('singapore',  91.50, 'SINGAPORE'),    # green onboard
    ('hungary',   228.75, 'HUNGARY'),      # Red Bull onboard
    ('singapore', 116.55, 'SINGAPORE'),    # head-on, after the 115.08 cut
    ('britain',   312.38, 'SILVERSTONE'),  # Mercedes onboard
    ('singapore',  88.68, 'SINGAPORE'),    # green onboard, earlier cut
    ('australia',  16.92, 'MELBOURNE'),    # gantry, before the 18.52 cut
    ('singapore', 120.40, 'SINGAPORE'),    # side tracking
    ('singapore', 102.26, 'SINGAPORE'),    # Haas onboard, different take
    ('china',      13.36, 'SHANGHAI'),     # after v4's 12.20-13.24
    ('singapore',  94.80, 'SINGAPORE'),    # green onboard, after the 94.50 cut
    ('belgium',   334.96, 'SPA'),          # pink onboard
    ('singapore', 130.48, 'SINGAPORE'),    # Haas onboard, after 130.28
    ('belgium',     5.20, 'SPA'),          # live grid, logo only
    ('singapore', 133.42, 'SINGAPORE'),    # Haas onboard, after 132.08
    ('miami',       2.20, 'MIAMI'),        # the only clean Miami window
    ('singapore', 124.42, 'SINGAPORE'),    # straight, the hold
]
GRADE = 'eq=contrast=1.10:saturation=1.08:gamma=0.94,unsharp=3:3:0.25'
# LIBRARY #100: Around 2.46, the 3.10, World 3.92. The phrase stays up through World.
PHRASE = (2.46, 4.20, 'AROUND THE WORLD')


def snap(t):
    return int(t * FPS) / FPS   # frame at or before the hit


FRAMES = [0] + [round(snap(t) * FPS) for t in HITS]
END = FRAMES[-1] / FPS


def spans():
    return [b - a for a, b in zip(FRAMES, FRAMES[1:])]


def dt(t0, t1, text, fs, y):
    text = text.replace("'", '’').replace(':', '\\:').replace(',', '\\,')
    return (f",drawtext=fontfile={FONT}:text='{text}':fontsize={fs}:fontcolor=white:"
            f"borderw=4:bordercolor=black@0.9:shadowcolor=black@0.4:shadowy=2:"
            f"x=(w-text_w)/2:y=h*{y}:enable='between(t,{t0:.3f},{t1:.3f})'")


def texts():
    p0, p1, phrase = PHRASE
    out = [dt(p0, p1, phrase, 48, 0.82)]
    for (name, st, track), fr, n in zip(SHOTS, FRAMES, spans()):
        t0, t1 = fr / FPS, (fr + n) / FPS
        if t1 <= p0 or t0 >= p1:
            out.append(dt(t0, t1, track, 42, 0.82))
        elif t0 < p0:
            out.append(dt(t0, p0, track, 42, 0.82))
        elif t1 > p1:
            out.append(dt(p1, t1, track, 42, 0.82))
    return ''.join(out)


def corners():
    """Native 260x130 top-left of each shot, no scale. Saved before the render."""
    from PIL import Image, ImageDraw
    import io
    cells = []
    for (name, st, track), n in zip(SHOTS, spans()):
        t = st + 0.04
        p = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{t:.3f}', '-i', os.path.join(D, name + '.mp4'),
                            '-frames:v', '1', '-vf', 'crop=260:130:0:0', '-f', 'image2pipe', '-vcodec', 'png', '-'],
                           capture_output=True, check=True)
        im = Image.open(io.BytesIO(p.stdout)).convert('RGB')
        assert im.size == (260, 130), im.size
        cell = Image.new('RGB', (260, 148), (0, 0, 0))
        cell.paste(im, (0, 18))
        ImageDraw.Draw(cell).text((4, 2), f'{track}  {t:.2f}', fill=(255, 220, 0))
        cells.append(cell)
    cols = 7
    w, h = cells[0].size
    rows = (len(cells) + cols - 1) // cols
    sheet = Image.new('RGB', (cols * w, rows * h), (0, 0, 0))
    for i, im in enumerate(cells):
        sheet.paste(im, ((i % cols) * w, (i // cols) * h))
    out = os.path.join(ROOT, 'grok', 'around-the-world-v5-corners.jpg')
    sheet.save(out, quality=95)
    print(out, sheet.size)


def main(mode='render'):
    os.makedirs(os.path.join(S, 'out'), exist_ok=True)
    ns = spans()
    assert len(ns) == len(SHOTS)
    if mode == 'check':
        used = {}
        prev = None
        print(f'{"edit":>8} {"dur":>6}  {"track":12} {"src":22}  hit-early')
        for (name, st, track), n, fr, hit in zip(SHOTS, ns, FRAMES, [0] + HITS):
            d = n / FPS
            t = fr / FPS
            err = (t - hit) * 1000 if hit else 0
            assert d <= 1.60 or fr == FRAMES[-2], f'long {track} {d}'
            if fr == FRAMES[-2]:
                assert d <= 2.0
            if prev == track:
                print(f'  adjacent {track}')
            prev = track
            print(f'{t:8.3f} {d:6.3f}  {track:12} {name:10} {st:7.2f}->{st+d:7.2f}  {err:6.1f} ms')
            for a, b in used.get(name, []):
                assert st + d <= a + 1e-3 or st >= b - 1e-3, f'overlap {name}'
            used.setdefault(name, []).append((st, st + d))
        print('shots', len(SHOTS), 'end', round(END, 3), 'fps', FPS)
        return
    if mode == 'corners':
        corners()
        return
    inp, fc, cat = [], '', ''
    for i, ((name, st, _), n) in enumerate(zip(SHOTS, ns)):
        inp += ['-ss', f'{st:.3f}', '-i', os.path.join(D, name + '.mp4')]
        fc += f'[{i}:v]fps={FPS},trim=end_frame={n},setpts=PTS-STARTPTS,{GRADE},setsar=1[v{i}];'
        cat += f'[v{i}]'
    k = len(SHOTS)
    fc += f'{cat}concat=n={k}:v=1:a=0[vc];[vc]fade=t=out:st={END - 0.8:.3f}:d=0.8{texts()}[v];'
    inp += ['-i', SONG]
    fc += f'[{k}:a]atrim=0:{END:.3f},asetpts=PTS-STARTPTS,afade=t=out:st={END - 0.8:.3f}:d=0.8[a]'
    out = os.path.join(S, 'out', 'grok_around_the_world_v5.mp4')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', *inp, '-filter_complex', fc, '-map', '[v]', '-map', '[a]',
                    '-t', f'{END:.3f}', '-c:v', 'libx264', '-crf', '12', '-preset', 'fast', '-pix_fmt', 'yuv420p',
                    '-c:a', 'aac', '-b:a', '256k', out], check=True)
    import brand
    tik = os.path.join(ROOT, 'grok', '2026-10-24-around-the-world-v5.mp4')
    print(brand.brand(out, tik, fps=30))
    import ytshort
    yt = os.path.join(ROOT, 'grok', '2026-10-24-around-the-world-v5-yt.mp4')
    print(ytshort.make(out, yt, 'AROUND THE WORLD|F1 2026', fps=FPS))


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else 'render')
