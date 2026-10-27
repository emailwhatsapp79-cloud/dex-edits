"""Hard times hit. He still has gas in the tank.

Horizontal 1920x1080, native trailer pixels, 30 fps. Trailers are 23.976/24,
so this is not a 60 fps master. TikTok file is the 30 fps master. YouTube is
ytshort.py of that same file (no invented 60).

Song #139 Hard Times (Paramore), chorus only. Cold open is Damien's line from
the Creed III trailer. Punches are one contact each, each from a different take
of Creed III, John Wick 4, and The Equalizer 3. Button is Catwoman in The Batman.
Cuts are the strong drum hits. Stamps lead the word they name and never fight
the voice that is actually speaking.
"""
import os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONT = os.path.join(ROOT, 'fonts', 'Anton.ttf')
SONG = os.environ.get('DEX_SONG', '/workspace/dex/dex-edits-assets/songs/139_hard_times.mp3')
CREED = '/tmp/dexsrc/movies/creed3.mp4'
WICK = '/tmp/dexsrc/movies/wick4.mp4'
EQ = '/tmp/dexsrc/movies/equalizer3.mp4'
BAT = '/tmp/dexsrc/movies/batman.mp4'
FPS = 30
GRADE = 'eq=contrast=1.10:saturation=1.08:gamma=0.94,unsharp=3:3:0.25'
GRADE_NIGHT = 'eq=contrast=1.06:brightness=0.03:saturation=1.02:gamma=1.06,unsharp=3:3:0.25'

# Song starts here so the first snare (0.328) is the first punch,
# and "Hard" begins just after "tank".
DELAY = 1.105333
# Song hits. The last one is the cut TO the button, not a punch.
HITS = [0.328, 2.583, 3.323, 4.571, 6.826, 7.818, 9.838, 10.828, 12.343, 13.830, 15.831, 18.323]

# name, src, contact, take_end, grade. Order is the punch order.
PUNCHES = [
    ('eq35', EQ, 35.48, 38.208, GRADE),
    ('c113', CREED, 113.30, 114.239, GRADE),
    ('eq46', EQ, 46.53, 47.958, GRADE),
    ('c109', CREED, 109.40, 113.113, GRADE),
    ('eq62', EQ, 62.16, 63.167, GRADE),
    ('c119', CREED, 119.70, 121.788, GRADE),
    ('eq139', EQ, 139.41, 140.417, GRADE),
    ('eq86', EQ, 86.16, 87.750, GRADE),
    ('c114', CREED, 114.28, 116.033, GRADE),
    ('wick', WICK, 105.86, 120.203, GRADE),
    ('eq49', EQ, 49.48, 54.042, GRADE),
]


def snap(t):
    """Nearest frame. If that frame is more than 8 ms late, take the one before."""
    f = round(t * FPS)
    if f / FPS > t + 0.008:
        f -= 1
    return f


def build():
    open_f = snap(DELAY + HITS[0])
    cut_f = [open_f] + [snap(DELAY + h) for h in HITS[1:]]
    btn_src = 62.15
    # hold through "will" (~64.18) and stop before the next line (~65.3)
    end_f = snap(cut_f[-1] / FPS + (64.32 - btn_src))
    frames = [open_f] + [b - a for a, b in zip(cut_f, cut_f[1:])] + [end_f - cut_f[-1]]
    times = [0.0] + [f / FPS for f in cut_f] + [end_f / FPS]
    shots = [('open', CREED, 51.80, 53.300, GRADE)] + PUNCHES + [('btn', BAT, btn_src, 79.204, GRADE_NIGHT)]
    assert len(shots) == len(frames)
    plan = []
    for (name, src, st, tend, grade), n, t0, t1 in zip(shots, frames, times, times[1:]):
        dur = n / FPS
        assert n > 0, name
        assert st + dur <= tend - 0.004, f'{name} crosses take {st:.3f}+{dur:.3f} > {tend:.3f}'
        plan.append(dict(name=name, src=src, st=st, n=n, t0=t0, t1=t1, dur=dur, grade=grade))
    return plan, times[-1]


def _esc(t):
    return t.replace('\\', '\\\\').replace("'", '’').replace(':', '\\:').replace(',', '\\,')


def words(end):
    # Each stamp is the line being said, a little early, and it ends before a different line.
    rows = [
        (0.00, 1.04, 'GAS IN THE TANK'),
        (1.06, 2.90, 'HARD TIMES'),
        (2.95, 5.45, 'WHY YOU TRY'),
        (5.50, 6.90, 'HARD TIMES'),
        (6.95, 8.20, 'TAKE YOU DOWN'),
        (8.25, 9.70, 'WHEN YOU CRY'),
        (9.75, 11.20, 'HARD TIMES'),
        (11.22, 12.40, "STILL DON'T KNOW"),
        (12.45, 13.70, 'EVEN SURVIVE'),
        (13.75, 16.85, 'HARD TIMES'),
        (16.90, 19.35, 'ROCK BOTTOM'),
        (19.43, 20.20, "IF WE DON'T"),
        (20.20, 20.95, 'STAND UP'),
        (20.95, end, 'NO ONE WILL'),
    ]
    return [(a, min(b, end), w) for a, b, w in rows if min(b, end) > a]


def text_filter(end):
    parts = []
    for a, b, w in words(end):
        parts.append(
            f"drawtext=fontfile={FONT}:text='{_esc(w)}':fontsize=104:fontcolor=white:"
            f"shadowcolor=black@0.60:shadowx=0:shadowy=4:borderw=5:bordercolor=black@0.50:"
            f"x=(w-text_w)/2:y=(h-text_h)/2-30:enable='between(t,{a:.3f},{b:.3f})'"
        )
    return ','.join(parts)


def grab(src, st, n, grade, dst):
    pre = max(0.0, st - 1.0)
    post = st - pre
    vf = f'fps={FPS},scale=1920:1080:flags=lanczos,setsar=1,{grade}'
    subprocess.run(
        ['ffmpeg', '-v', 'error', '-y', '-ss', f'{pre:.3f}', '-i', src, '-ss', f'{post:.3f}',
         '-frames:v', str(n), '-an', '-vf', vf,
         '-c:v', 'libx264', '-crf', '12', '-preset', 'veryfast', '-pix_fmt', 'yuv420p', dst],
        check=True)


def cut_wav(src, st, dur, dst):
    pre = max(0.0, st - 1.0)
    subprocess.run(
        ['ffmpeg', '-v', 'error', '-y', '-ss', f'{pre:.3f}', '-i', src, '-ss', f'{st - pre:.3f}',
         '-t', f'{dur:.3f}', '-vn', '-ac', '2', '-ar', '48000', dst],
        check=True)


def render(out):
    plan, end = build()
    tmp = '/tmp/dexsrc/ht/build'
    os.makedirs(tmp, exist_ok=True)
    parts = []
    for i, s in enumerate(plan):
        p = os.path.join(tmp, f's{i:02d}.mp4')
        print(f"{s['t0']:7.3f} {s['dur']:5.3f}s {s['name']:6} @{s['st']:.2f} n={s['n']}", flush=True)
        grab(s['src'], s['st'], s['n'], s['grade'], p)
        parts.append(p)
    lst = os.path.join(tmp, 'list.txt')
    open(lst, 'w').write(''.join(f"file '{p}'\n" for p in parts))
    vid = os.path.join(tmp, 'video.mp4')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', lst, '-c', 'copy', vid], check=True)

    btn = next(s for s in plan if s['name'] == 'btn')
    face = plan[0]
    talk_w = os.path.join(tmp, 'talk.wav')
    btn_w = os.path.join(tmp, 'btn.wav')
    cut_wav(face['src'], face['st'], face['dur'], talk_w)
    cut_wav(btn['src'], btn['st'], btn['dur'], btn_w)
    fc = (
        f"[0:v]{text_filter(end)}[v];"
        f"[1:a]aformat=sample_rates=48000:channel_layouts=stereo,atrim=0:{face['dur']:.3f},asetpts=PTS-STARTPTS,"
        f"afade=t=out:st={max(0.0, face['dur'] - 0.10):.3f}:d=0.10,volume=1.5[talk];"
        f"[2:a]aformat=sample_rates=48000:channel_layouts=stereo,atrim=0:{end - DELAY:.3f},asetpts=PTS-STARTPTS,"
        f"adelay={int(round(DELAY * 1000))}|{int(round(DELAY * 1000))},"
        f"afade=t=in:st={DELAY:.3f}:d=0.04,"
        f"volume='if(lt(t,{btn['t0'] - 0.05:.3f}),1,0.16)',"
        f"afade=t=out:st={end - 0.70:.3f}:d=0.70[song];"
        f"[3:a]aformat=sample_rates=48000:channel_layouts=stereo,atrim=0:{btn['dur']:.3f},asetpts=PTS-STARTPTS,"
        f"adelay={int(round(btn['t0'] * 1000))}|{int(round(btn['t0'] * 1000))},volume=1.7[btn];"
        f"[talk][song][btn]amix=inputs=3:duration=longest:dropout_transition=0:normalize=0,alimiter=limit=0.95[a]"
    )
    subprocess.run(
        ['ffmpeg', '-v', 'error', '-y', '-i', vid, '-i', talk_w, '-i', SONG, '-i', btn_w,
         '-filter_complex', fc, '-map', '[v]', '-map', '[a]', '-t', f'{end:.3f}',
         '-c:v', 'libx264', '-crf', '12', '-preset', 'fast', '-pix_fmt', 'yuv420p',
         '-c:a', 'aac', '-b:a', '256k', out],
        check=True)
    print('rendered', out, f'{end:.3f}s')
    return end


def stills(sheet):
    plan, end = build()
    os.makedirs('/tmp/dexsrc/ht/stills', exist_ok=True)
    from PIL import Image, ImageDraw
    ims = []
    ws = words(end)
    for s in plan:
        jpg = f"/tmp/dexsrc/ht/stills/{s['name']}.jpg"
        t = s['st']
        if s['name'] == 'open':
            t = s['st'] + 0.50
        elif s['name'] == 'btn':
            t = s['st'] + 1.00
        pre = max(0.0, t - 0.5)
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{pre:.3f}', '-i', s['src'],
                        '-ss', f'{t - pre:.3f}', '-frames:v', '1',
                        '-vf', f'scale=480:-2,{s["grade"]}', jpg], check=True)
        im = Image.open(jpg).convert('RGB')
        w = next((word for a, b, word in ws if a - 0.05 <= s['t0'] < b), '')
        d = ImageDraw.Draw(im)
        d.rectangle((0, 0, im.size[0], 18), fill=(0, 0, 0))
        d.text((4, 2), f"{s['name']} {s['t0']:.2f} {w}", fill=(255, 220, 80))
        ims.append(im)
    cols = 4
    w, h = ims[0].size
    rows = (len(ims) + cols - 1) // cols
    S = Image.new('RGB', (cols * w, rows * h), (0, 0, 0))
    for i, im in enumerate(ims):
        S.paste(im, ((i % cols) * w, (i // cols) * h))
    S.save(sheet, quality=85)
    print(sheet, 'end', round(end, 3))


def report():
    plan, end = build()
    print(f'end {end:.3f}s  delay {DELAY:.3f}  shots {len(plan)}')
    for s in plan:
        print(f"{s['t0']:7.3f}-{s['t1']:7.3f} {s['dur']:5.3f}s {s['name']:6} src {s['st']:.2f}")
    print('cut vs delayed hit:')
    for s, h in zip(plan[1:], HITS):
        err = (s['t0'] - (DELAY + h)) * 1000
        flag = ' LATE' if err > 33 else ''
        print(f"  {s['name']:6} {err:+6.1f} ms{flag}")


if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'report'
    if mode == 'report':
        report()
    elif mode == 'stills':
        stills(sys.argv[2] if len(sys.argv) > 2 else '/workspace/screenshots/ht/pick/plan_stills.jpg')
    elif mode == 'render':
        render(sys.argv[2])
    else:
        raise SystemExit('report | stills | render')
