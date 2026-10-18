"""FOOTBALL - Salah. Egypt, Vancouver, 21 June 2026.
Official @fifaworldcup/video/7654129160910097686, native 1080x1920, 29.97 fps.
One goal, in order: the run, the strike through the net, his arms-wide celebration.
The live angle ends just after 5.4s, when this clip cuts to a replay of the same goal.
That replay is not used. The longer FIFA highlight carries a score bug the whole way, so it is not used.
Song #4, instrumental until the vocal at 17.8s. This edit ends at 4.90s.
No YouTube file: the source is 29.97, not 50/60.
"""
import os, sys, subprocess
sys.path.insert(0, os.path.dirname(__file__))
import wideedit

ROOT = wideedit.ROOT
ASSETS = os.environ.get('DEX_ASSETS', os.path.join(os.path.dirname(ROOT), 'dex-edits-assets'))
SRC = '/tmp/dexsrc/salah_goal.mp4'
SONG = os.path.join(ASSETS, 'songs', '04_legacy_phonk_108bpm.mp3')
FONT = os.path.join(ROOT, 'fonts', 'Anton.ttf')
FPS = 30
END = 4.860
# (edit_t, src_t). Cuts snapped with int(hit*30)/30, never late.
# Strike (src 4.05) is inside shot 2. Arms-wide is shot 3, before the clip's own cut (~5.50).
SHOTS = [
    (0.000, 0.200),   # the run in, number 10
    (2.167, 2.700),   # the one-two, the strike, the net
    (4.433, 5.020),   # arms wide
]
GRADE = 'eq=contrast=1.08:saturation=1.06:gamma=0.97,unsharp=3:3:0.25'


def frames():
    ts = [s[0] for s in SHOTS] + [END]
    fr = [round(t * FPS) for t in ts]
    return [b - a for a, b in zip(fr, fr[1:])]


def _esc(t):
    return t.replace("'", "’").replace(':', '\\:').replace(',', '\\,')


def text():
    # SALAH. from the first frame. THE GO-AHEAD. as the shot is struck.
    a = (f"drawtext=fontfile={FONT}:text='{_esc('SALAH.')}':fontsize=132:fontcolor=white:"
         f"shadowcolor=black@0.6:shadowx=0:shadowy=3:borderw=4:bordercolor=black@0.55:"
         f"x=(w-text_w)/2:y=h*0.16")
    b = (f"drawtext=fontfile={FONT}:text='{_esc('THE GO-AHEAD.')}':fontsize=64:fontcolor=white:"
         f"shadowcolor=black@0.6:shadowx=0:shadowy=2:borderw=3:bordercolor=black@0.5:"
         f"x=(w-text_w)/2:y=h*0.245:enable='gte(t,3.34)'")
    return a + ',' + b


def check():
    used = []
    for (t, st), n in zip(SHOTS, frames()):
        d = n / FPS
        assert st + d <= 5.48, f'crosses the replay cut {st}+{d}'
        for a, b in used:
            assert st + d <= a or st >= b, 'overlap'
        used.append((st, st + d))
        print(f'{t:6.2f} {d:5.2f}s @{st:6.2f}')


def render(out, tmp):
    os.makedirs(tmp, exist_ok=True)
    parts = []
    for i, ((t, st), n) in enumerate(zip(SHOTS, frames())):
        p = os.path.join(tmp, f's{i:02d}.mp4')
        parts.append(p)
        vf = f'fps={FPS},scale=1080:1920:flags=lanczos,{GRADE},setsar=1'
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{st:.3f}', '-i', SRC, '-frames:v', str(n),
                        '-an', '-vf', vf, '-c:v', 'libx264', '-crf', '10', '-preset', 'fast', '-pix_fmt', 'yuv420p', p], check=True)
    lst = os.path.join(tmp, 'list.txt')
    open(lst, 'w').write(''.join(f"file '{p}'\n" for p in parts))
    vid = os.path.join(tmp, 'video.mp4')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', lst, '-c', 'copy', vid], check=True)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', vid, '-i', SONG,
                    '-vf', text(),
                    '-filter_complex', f"[1:a]atrim=0:{END:.3f},afade=t=out:st={END - 0.45:.3f}:d=0.45[a]",
                    '-map', '0:v', '-map', '[a]', '-t', f'{END:.3f}', '-c:v', 'libx264', '-crf', '10',
                    '-preset', 'slow', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '256k', out], check=True)
    print(out)


if __name__ == '__main__':
    check()
    if len(sys.argv) > 1 and sys.argv[1] == 'check':
        sys.exit(0)
    render('/tmp/out/grok_salah.mp4', '/tmp/tmp_salah')
