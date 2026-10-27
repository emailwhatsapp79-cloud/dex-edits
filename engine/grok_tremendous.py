"""I'm feeling tremendous. Direction: he's that guy, and the hits say it.

Song is the trending Verified section (Your Favorite Martian), the clean 18s.
The lyric sits top-left like a watermark, not a title in the middle of the punch.
Punches on the drum, a walk and a stare so it moves, and it ends on the last line.
30 fps. Trailers are 24 fps, so there is no 60 fps file.
"""
import os, subprocess, sys

FPS = 30
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CREED = '/tmp/dexsrc/movies/creed3.mp4'
WICK = '/tmp/dexsrc/movies/wick4.mp4'
EQ = '/tmp/dexsrc/movies/equalizer3.mp4'
SONG = '/workspace/dex/dex-edits-assets/songs/155_i_m_feeling_tremendous.mp3'
FONT = os.path.join(ROOT, 'fonts', 'Archivo.ttf')
GRADE = 'eq=contrast=1.08:saturation=1.10:gamma=0.97,unsharp=3:3:0.22'
END = 17.500

# (t, src, src_t, take_end, kind). Punch src_t is the contact frame.
SHOTS = [
    (0.000, CREED,  51.90,  53.300, 'vibe'),
    (0.942, EQ,     35.48,  38.208, 'punch'),
    (2.116, EQ,     46.53,  47.958, 'punch'),
    (3.401, CREED, 113.30, 114.239, 'punch'),
    (4.218, CREED, 114.28, 116.033, 'punch'),
    (5.309, EQ,     62.16,  63.167, 'punch'),
    (6.125, EQ,    139.41, 140.417, 'punch'),
    (6.519, EQ,     86.16,  87.750, 'punch'),
    (7.749, WICK,   99.35, 101.518, 'vibe'),
    (9.253, CREED, 119.70, 121.788, 'punch'),
    (10.478, CREED, 116.55, 117.576, 'vibe'),
    (11.442, EQ,    83.20,  86.000, 'punch'),
    (12.389, CREED, 109.40, 113.113, 'punch'),
    (13.998, EQ,    49.48,  54.042, 'punch'),
    (14.707, CREED, 102.30, 108.150, 'end'),
]


def snap(t):
    f = int(round(t * FPS))
    if f / FPS > t + 0.008:
        f -= 1
    return f


def plan():
    cuts = []
    for s in SHOTS:
        f = snap(s[0])
        if cuts and f <= cuts[-1]:
            f = cuts[-1] + 1
        cuts.append(f)
    end_f = snap(END)
    if end_f <= cuts[-1]:
        end_f = cuts[-1] + 1
    cuts.append(end_f)
    rows = []
    for i, s in enumerate(SHOTS):
        a, b = cuts[i], cuts[i + 1]
        rows.append(dict(kind=s[4], src=s[1], st=s[2], t0=a / FPS, t1=b / FPS,
                         take_end=s[3], n=b - a, dur=(b - a) / FPS, hit=s[0]))
    for r in rows:
        if r['st'] + r['dur'] > r['take_end'] - 0.012:
            raise SystemExit(
                f"past the take: {r['kind']} @{r['st']:.2f} + {r['dur']:.3f}s > {r['take_end']:.3f}")
    return rows


def esc(t):
    return t.replace("'", '’').replace(':', '\\:').replace(',', '\\,')


def text_filter():
    # Top-left, small, white. It sits like a watermark. The line is the one being sung.
    lines = [
        (0.00, 1.42, 'I’M FEELING TREMENDOUS'),
        (1.42, 3.60, 'NOW PEOPLE CLAP WHEN I FINISH UP A SENTENCE'),
        (3.60, 5.72, 'NOW THEY BUILD A STATUE TO HONOR MY EXISTENCE'),
        (5.72, 8.58, 'NOW I GOT THE PRESIDENT FILLING UP MY MENTIONS'),
        (8.58, 10.24, 'I DON’T NEED A CHAUFFEUR'),
        (10.24, 12.28, 'I AIN’T HAD A CAR SINCE LAST OCTOBER'),
        (12.28, 14.36, 'EVER SINCE THEY GAVE ME A NOBEL PRIZE'),
        (14.36, 17.50, 'A CROWD CARRIES ME ON THEIR SHOULDERS'),
    ]
    parts = []
    for a, b, w in lines:
        parts.append(
            f"drawtext=fontfile={FONT}:text='{esc(w)}':fontsize=34:fontcolor=white@0.92:"
            f"shadowcolor=black@0.55:shadowx=2:shadowy=2:"
            f"x=48:y=40:enable='between(t,{a:.3f},{b:.3f})'"
        )
    return ','.join(parts)


def grab(src, st, n, dst):
    pre = max(0.0, st - 1.0)
    post = st - pre
    vf = f'fps={FPS},scale=1920:1080:flags=lanczos,setsar=1,{GRADE}'
    subprocess.run([
        'ffmpeg', '-v', 'error', '-y', '-ss', f'{pre:.3f}', '-i', src, '-ss', f'{post:.3f}',
        '-frames:v', str(n), '-an', '-vf', vf,
        '-c:v', 'libx264', '-crf', '12', '-preset', 'veryfast', '-pix_fmt', 'yuv420p', dst
    ], check=True)


def report(rows):
    print(f"end {rows[-1]['t1']:.3f}s  shots {len(rows)}")
    for r in rows:
        err = (r['t0'] - r['hit']) * 1000
        print(f"  {r['t0']:6.3f}-{r['t1']:6.3f} {r['dur']:5.3f}s {r['kind']:5} @{r['st']:.2f}  {err:+.1f} ms")


def render(rows, out):
    tmp = '/tmp/dexsrc/ht/tr'
    os.makedirs(tmp, exist_ok=True)
    parts = []
    for i, r in enumerate(rows):
        p = os.path.join(tmp, f's{i:02d}.mp4')
        grab(r['src'], r['st'], r['n'], p)
        parts.append(p)
    lst = os.path.join(tmp, 'list.txt')
    open(lst, 'w').write(''.join(f"file '{p}'\n" for p in parts))
    vid = os.path.join(tmp, 'video.mp4')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', lst, '-c', 'copy', vid], check=True)
    end = rows[-1]['t1']
    fc = (
        f"[0:v]{text_filter()}[v];"
        f"[1:a]aformat=sample_rates=48000:channel_layouts=stereo,atrim=0:{end:.3f},asetpts=PTS-STARTPTS,"
        f"afade=t=out:st={end - 0.30:.3f}:d=0.30,volume=1.2[a]"
    )
    subprocess.run([
        'ffmpeg', '-v', 'error', '-y', '-i', vid, '-i', SONG,
        '-filter_complex', fc, '-map', '[v]', '-map', '[a]', '-t', f'{end:.3f}',
        '-c:v', 'libx264', '-crf', '12', '-preset', 'fast', '-pix_fmt', 'yuv420p',
        '-c:a', 'aac', '-b:a', '256k', out
    ], check=True)
    print('rendered', out)


if __name__ == '__main__':
    rows = plan()
    report(rows)
    if len(sys.argv) > 1 and sys.argv[1] == 'render':
        render(rows, sys.argv[2])
