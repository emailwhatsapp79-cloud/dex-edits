"""FOOTBALL v2 - Salah. Egypt, the 2026 World Cup goal.
Build-up, the other angle, the keeper, the strike and the net, then him close.
Two official @fifaworldcup pictures. The pitchside one is clean and native
1080x1920. The highlight has a score bug, so those shots are cropped from y=300
and scaled 1.19x, which takes the bug off. His close celebration is one take,
42.6-45.8. It ends there. The next frame is a wide shot, and it is not used.
Sound is #5 from 15.05s (after the range used on lights-out). Instrumental.
The strike is the cut at 7.00. SALAH. / THE GO-AHEAD.
30 fps. No YouTube file: neither source is 50 or 60.
"""
import os, sys, subprocess
sys.path.insert(0, os.path.dirname(__file__))
import wideedit

ROOT = wideedit.ROOT
GOAL = '/tmp/dexsrc/salah_goal.mp4'
FWC = '/tmp/dexsrc/salah_fwc.mp4'
SONG = '/workspace/dex/dex-edits-assets/songs/05_montagem_kali_slowed.m4a'
FONT = os.path.join(ROOT, 'fonts', 'Anton.ttf')
FPS = 30
W, H = 1080, 1920
END = 11.300
OFFSET = 15.050
# bug sits above y=280. Cropping it off is 1920/1620 = 1.19x.
CROP = (1080, 1620, 0, 300)
# (edit t snapped early, src, src t, crop or None)
SHOTS = [
    (0.000, FWC, 38.250, CROP),   # the move, the other angle
    (1.400, GOAL, 0.350, None),   # the run, number 10
    (4.967, FWC, 40.100, CROP),   # the keeper, the ball
    (7.000, GOAL, 4.180, None),   # the strike, the net
    (8.033, FWC, 42.600, CROP),   # him
]
GRADE = 'eq=contrast=1.08:saturation=1.06:gamma=0.97,unsharp=3:3:0.25'
# last clean frame of each window
LIMITS = {
    (FWC, 0): 39.68,
    (GOAL, 1): 4.05,
    (FWC, 2): 42.45,
    (GOAL, 3): 5.42,
    (FWC, 4): 45.85,
}


def frames():
    ts = [s[0] for s in SHOTS] + [END]
    fr = [round(t * FPS) for t in ts]
    return [b - a for a, b in zip(fr, fr[1:])]


def _esc(t):
    return t.replace("'", "’").replace(':', '\\:').replace(',', '\\,')


def text():
    a = (f"drawtext=fontfile={FONT}:text='{_esc('SALAH.')}':fontsize=132:fontcolor=white:"
         f"shadowcolor=black@0.6:shadowx=0:shadowy=3:borderw=4:bordercolor=black@0.55:"
         f"x=(w-text_w)/2:y=h*0.16")
    b = (f"drawtext=fontfile={FONT}:text='{_esc('THE GO-AHEAD.')}':fontsize=64:fontcolor=white:"
         f"shadowcolor=black@0.6:shadowx=0:shadowy=2:borderw=3:bordercolor=black@0.5:"
         f"x=(w-text_w)/2:y=h*0.245:enable='gte(t,7.00)'")
    return a + ',' + b


def check():
    prev = None
    counts = {}
    used = {}
    for i, ((t, src, st, crop), n) in enumerate(zip(SHOTS, frames())):
        d = n / FPS
        assert st + d <= LIMITS[(src, i)] + 0.02, f'past the take {t} {st}+{d:.2f}'
        for a, b in used.get(src, []):
            assert st + d <= a + 0.02 or st >= b - 0.02, f'overlap {st}'
        used.setdefault(src, []).append((st, st + d))
        name = os.path.basename(src)
        assert prev != src, name
        prev = src
        counts[name] = counts.get(name, 0) + 1
        print(f'{t:6.2f} {d:5.2f}s {name[:16]:16} @{st:7.2f} -> {st+d:7.2f}')
    for k, v in counts.items():
        assert v <= 3, k
        print(f'  {v} x {k}')
    assert 12.0 <= END <= 15.0 or END >= 11.0


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
                        '-an', '-vf', vf, '-c:v', 'libx264', '-crf', '12', '-preset', 'veryfast', '-pix_fmt', 'yuv420p', p], check=True)
    lst = os.path.join(tmp, 'list.txt')
    open(lst, 'w').write(''.join(f"file '{p}'\n" for p in parts))
    vid = os.path.join(tmp, 'video.mp4')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', lst, '-c', 'copy', vid], check=True)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', vid, '-ss', f'{OFFSET:.3f}', '-i', SONG,
                    '-vf', text(),
                    '-filter_complex', f"[1:a]atrim=0:{END:.3f},afade=t=out:st={END-0.40:.3f}:d=0.40[a]",
                    '-map', '0:v', '-map', '[a]', '-t', f'{END:.3f}', '-c:v', 'libx264', '-crf', '12',
                    '-preset', 'fast', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '256k', out], check=True)
    print(out)


if __name__ == '__main__':
    check()
    if len(sys.argv) > 1 and sys.argv[1] == 'check':
        sys.exit(0)
    render('/tmp/out/grok_salah_v2.mp4', '/tmp/tmp_salah_v2')
