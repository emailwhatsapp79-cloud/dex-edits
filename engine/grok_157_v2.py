"""#157 v2 — Something bad. New shot list. Not a patch of any earlier cut.

Peter, trailer 1, over the red suit in the washer: "Something bad was going to happen."
Then the fight, hero and villain answering, one contact per drum, the best hits held
about two beats. Ends on the dive: "I'm Spider-Man."

Song is the clean keny4580 dance only. On top of it: those two lines, in his voice,
and each hit's own sound from the shot on screen. Nothing else.
Footage: Street Fighter, Spider-Man Brand New Day (trailer 1 + the June trailer only),
VisionQuest, Avengers: Doomsday. Official 1080p, pixels 1:1, letterbox kept.
"""
import os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import wmtext

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SONG = os.path.join(os.path.dirname(ROOT), 'dex-edits-assets', 'songs',
                    '157_original_sound_official_quality.mp3')
FPS, W, H = 30, 1920, 1080
GRADE = 'eq=contrast=1.04:saturation=1.05'
RED = (198, 36, 44)   # Peter
F = {
    'spt1': '/tmp/f157v2/sp_t1.mp4',
    'spN': '/tmp/dexsrc/movies/now/sp_new.mp4',
    'sf1': '/tmp/dexsrc/movies/now/sf_t1.mp4',
    'sf2': '/tmp/dexsrc/movies/now/sf_t2.mp4',
    'vqB': '/tmp/dexsrc/movies/now/vq_b.mp4',
    'doom': '/tmp/dexsrc/movies/now/doom_t.mp4',
}
FILM = {
    'spt1': 'Spider-Man: Brand New Day',
    'spN': 'Spider-Man: Brand New Day',
    'sf1': 'Street Fighter',
    'sf2': 'Street Fighter',
    'vqB': 'VisionQuest',
    'doom': 'Avengers: Doomsday',
}

def at(hit_f, hit_src, start_f):
    """Source time of start_f so that hit_f shows hit_src."""
    return hit_src - (hit_f - start_f) / FPS

# f0, f1, key, src, what, hit frame or None, drum time or None, contact source or None
# Frames are the edit. A hit frame shows that source instant, on the snapped drum.
SHOTS = [
    (0,   34,  'spt1', 34.52,                 'washer — he says it',       None, None,   None),
    (34,  70,  'vqB',  109.55,                'villain walks the wreck',   None, None,   None),
    (70,  123, 'spN',  at(91, 129.46, 70),    'through the wall',          91,  3.044,  129.46),
    (123, 162, 'sf2',  57.40,                 'Ken, the quiet room',       None, None,   None),
    (162, 218, 'doom', at(182, 64.54, 162),   'jet hits the water',        182, 6.061,  64.54),
    (218, 245, 'sf1',  at(222, 118.087, 218), 'the kick',                  222, 7.402,  118.087),
    (245, 254, 'vqB',  at(246, 96.853, 245),  'the beam',                  246, 8.204,  96.853),
    (254, 303, 'spt1', 8.48,                  'on the roof',               None, None,   None),
    (303, 340, 'doom', at(310, 88.727, 303),  'the blast',                 310, 10.341, 88.727),
    (340, 375, 'spt1', 51.88,                 'low, over the street',      None, None,   None),
    (375, 404, 'spN',  117.043,               'through the building',      375, 12.491, 117.043),
    (404, 432, 'doom', 114.15,                'two of them in the smoke',  None, None,   None),
    (432, 434, 'sf1',  118.88,                'the kick lands',            None, None,   None),
    (434, 440, 'sf2',  at(439, 122.833, 434), 'the blast takes him',       439, 14.632, 122.833),
    (440, 499, 'spt1', 18.78,                 'he swings',                 None, None,   None),
    (499, 513, 'sf1',  at(503, 142.51, 499),  'the boot',                  503, 16.770, 142.51),
    (513, 567, 'spt1', 127.95,                'over the city',             None, None,   None),
    (567, 599, 'spt1', 110.72,                'into the bus',              567, 18.915, 110.72),
    (599, 631, 'sf1',  15.40,                 'he watches',                None, None,   None),
    (631, 650, 'spt1', 120.22,                'the punch',                 631, 21.045, 120.22),
    (650, 682, 'spt1', 46.05,                 "the dive — I'm Spider-Man", None, None,   None),
]
END_F = SHOTS[-1][1]
END = END_F / FPS

# same-file ranges must not overlap (a repeated take)
def _check():
    prev = 0
    used = {}
    for i, (f0, f1, key, src, what, hit, drum, csrc) in enumerate(SHOTS):
        assert f0 == prev, (i, f0, prev)
        assert f1 - f0 >= 2, i
        prev = f1
        t1 = src + (f1 - f0) / FPS
        if hit is not None:
            assert f0 <= hit < f1
            got = src + (hit - f0) / FPS
            assert abs(got - csrc) < 0.001, (what, got, csrc)
            off = abs(hit / FPS - drum)
            assert off <= 1 / FPS + 0.001, (what, off)
        for a, b in used.get(key, []):
            assert t1 <= a + 0.03 or src >= b - 0.03, (key, src, t1, a, b)
        used.setdefault(key, []).append((src, t1))
    assert prev == END_F
_check()

# spoken lines, edit times. The washer picture starts as he says "bad".
WORDS = [
    (0.04, 0.46, 'SOMETHING BAD'),
    (0.46, 1.10, 'WAS GOING TO HAPPEN'),
    (650 / FPS + 0.06, 650 / FPS + 1.05, "I'M SPIDER-MAN"),
]
# (edit start, duration) of his voice, taken from the same frames
SPEECH = [
    ('spt1', 34.52, 0.00, 1.08),             # through "happen", still on the washer
    ('spt1', 46.05, 650 / FPS, 0.92),        # "I'm Spider-Man"
]


def render(out):
    tmp = '/tmp/f157v2/build'
    os.makedirs(tmp, exist_ok=True)
    parts = []
    for i, (f0, f1, key, src, *_) in enumerate(SHOTS):
        part = os.path.join(tmp, f's{i:02d}.mp4')
        parts.append(part)
        n = f1 - f0
        subprocess.run([
            'ffmpeg', '-v', 'error', '-y', '-ss', f'{src:.4f}', '-i', F[key],
            '-frames:v', str(n), '-an',
            '-vf', f'fps={FPS},scale={W}:{H}:flags=lanczos,{GRADE},setsar=1',
            '-c:v', 'libx264', '-crf', '12', '-preset', 'veryfast', '-pix_fmt', 'yuv420p',
            part], check=True)
    lst = os.path.join(tmp, 'list.txt')
    open(lst, 'w').write(''.join(f"file '{p}'\n" for p in parts))
    vid = os.path.join(tmp, 'video.mp4')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', lst,
                    '-c', 'copy', vid], check=True)

    cmd = ['ffmpeg', '-v', 'error', '-y', '-i', vid, '-i', SONG]
    pngs = []
    for i, (_, _, text) in enumerate(WORDS):
        p = os.path.join(tmp, f'w{i}.png')
        wmtext.word_png(text, W, H, p, size=78, opacity=0.80, cy=0.6, color=RED)
        pngs.append(p)
        cmd += ['-loop', '1', '-framerate', str(FPS), '-t', f'{END:.3f}', '-i', p]
    # hit sounds, one per contact, from that shot
    hits = [(f0, f1, key, src, what, hit, drum, csrc)
            for (f0, f1, key, src, what, hit, drum, csrc) in SHOTS if hit is not None]
    n0 = 2 + len(pngs)
    for j, (f0, f1, key, src, what, hit, drum, csrc) in enumerate(hits):
        a = csrc - 0.05
        cmd += ['-ss', f'{a:.4f}', '-t', '0.55', '-i', F[key]]
    for key, ssrc, edit_t, dur in SPEECH:
        cmd += ['-ss', f'{ssrc:.4f}', '-t', f'{dur:.3f}', '-i', F[key]]

    chain, last = wmtext.overlay_filter(WORDS, 2, '[0:v]')
    fx, labels = '', []
    for j, (f0, f1, key, src, what, hit, drum, csrc) in enumerate(hits):
        when = hit / FPS - 0.05
        ms = int(round(when * 1000))
        fx += (f"[{n0 + j}:a]aformat=channel_layouts=stereo,highpass=f=80,"
               f"afade=t=in:d=0.01,afade=t=out:st=0.22:d=0.30,volume=2.0,"
               f"adelay={ms}|{ms}[x{j}];")
        labels.append(f'[x{j}]')
    ns = n0 + len(hits)
    for k, (key, ssrc, edit_t, dur) in enumerate(SPEECH):
        ms = int(round(edit_t * 1000))
        fx += (f"[{ns + k}:a]aformat=channel_layouts=stereo,highpass=f=140,lowpass=f=8000,"
               f"volume=2.4,afade=t=in:d=0.02,afade=t=out:st={max(0.05, dur - 0.18):.3f}:d=0.16,"
               f"adelay={ms}|{ms}[v{k}];")
        labels.append(f'[v{k}]')
    hit_duck = '+'.join(f'between(t,{hit / FPS - 0.02:.3f},{hit / FPS + 0.22:.3f})' for *_, hit, _, _ in 
                        [(a, b, c, d, e, h, dr, cs) for (a, b, c, d, e, h, dr, cs) in SHOTS if h is not None])
    # rebuild cleanly
    hit_terms = '+'.join(
        f'between(t,{h / FPS - 0.02:.3f},{h / FPS + 0.22:.3f})' for *_, h, __, ___ in hits)
    speech_terms = '+'.join(
        f'between(t,{edit_t:.3f},{edit_t + dur:.3f})' for _, _, edit_t, dur in SPEECH)
    fx += (f"[1:a]atrim=0:{END:.3f},asetpts=PTS-STARTPTS,"
           f"volume='1*(1-0.45*min(1,{hit_terms}))*(1-0.70*min(1,{speech_terms}))':eval=frame,"
           f"afade=t=out:st={END - 0.35:.3f}:d=0.35[song];"
           f"[song]{''.join(labels)}amix=inputs={len(labels) + 1}:normalize=0:duration=first,"
           f"alimiter=limit=0.95[a]")
    subprocess.run(cmd + [
        '-filter_complex', chain + fx, '-map', last, '-map', '[a]',
        '-t', f'{END:.3f}', '-r', str(FPS),
        '-c:v', 'libx264', '-crf', '12', '-preset', 'fast', '-pix_fmt', 'yuv420p',
        '-c:a', 'aac', '-b:a', '192k', out], check=True)
    print('master', out, f'{END:.3f}s')


def report():
    print(f'{"edit":>8}  {"film":<28}  {"shot":<36}  {"hits":<22}  off')
    for f0, f1, key, src, what, hit, drum, csrc in SHOTS:
        t = f0 / FPS
        if hit is None:
            print(f'{t:8.3f}  {FILM[key]:<28}  {what:<36}  {"—":<22}  —')
        else:
            off = int(round((hit / FPS - drum) * 1000))
            print(f'{hit / FPS:8.3f}  {FILM[key]:<28}  {what:<36}  contact {csrc:.2f}s       {off:+d} ms')


if __name__ == '__main__':
    report()
    out = sys.argv[1] if len(sys.argv) > 1 else '/tmp/f157v2/master.mp4'
    render(out)
