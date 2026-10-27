"""#157 keny4580 dance sound (112 BPM, clean instrumental) x Oct 2026 films.

Open: Vision, "But I'm not a hero anymore" (VisionQuest, his own voice, song dipped).
Hard bars: one contact per strong drum hit, that shot's own sound on top.
Quiet bars: a stare, a walk, a reaction.
End: Ken, "I'm going to win it all" (Street Fighter).

Official 1080p IMDb trailers, pixels 1:1. Song is music only.
"""
import os, subprocess, sys
sys.path.insert(0, os.path.dirname(__file__))
import wmtext

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SONG = os.path.join(os.path.dirname(ROOT), 'dex-edits-assets', 'songs',
                    '157_original_sound_official_quality.mp3')
SRC = {
    'sf1': '/tmp/dexsrc/movies/now/sf_t1.mp4',
    'sf2': '/tmp/dexsrc/movies/now/sf_t2.mp4',
    'spN': '/tmp/dexsrc/movies/now/sp_new.mp4',
    'spF': '/tmp/dexsrc/movies/now/sp_final.mp4',
    'vqA': '/tmp/dexsrc/movies/now/vq_a.mp4',
    'vqB': '/tmp/dexsrc/movies/now/vq_b.mp4',
    'doom': '/tmp/dexsrc/movies/now/doom_t.mp4',
}
FPS, W, H = 30, 1920, 1080
GRADE = 'eq=contrast=1.06:saturation=1.06:gamma=0.90,unsharp=3:3:0.18'
GOLD = (232, 206, 140)   # Vision
RED = (214, 46, 38)      # Ken

# (name, key, f0, f1, extra). f0/f1 are output frames. Hits store the source contact
# and the output frame the contact must sit on.
RAW = [
    ('open', 'vqB', 0, 57, dict(src=40.08, speech="BUT I'M NOT A HERO ANYMORE", color=GOLD,
                                what='Vision says he is not a hero anymore')),
    ('ryu-rain', 'sf2', 57, 83, dict(src=2.98, what='Ryu walks in the rain')),
    ('ken-punch', 'sf2', 83, 102, dict(contact=38.01, hf=91, what='Ken punch lands')),
    ('sp-fist', 'spN', 102, 113, dict(contact=90.04, hf=107, what='Spider-Man punch to the lens')),
    ('red-punch', 'sf1', 113, 119, dict(contact=40.88, hf=117, what='red punch')),
    ('spidey-look', 'spN', 119, 146, dict(src=148.32, what='Spider-Man stare')),
    ('ryu-ken', 'sf2', 146, 176, dict(src=151.12, what='Ryu and Ken')),
    ('glove', 'sf2', 176, 192, dict(contact=50.55, hf=182, what='glove hits the lens')),
    ('symbiote', 'spN', 192, 208, dict(contact=123.04, hf=206, what='symbiote blast')),
    ('ultron', 'vqB', 208, 224, dict(contact=89.29, hf=222, what='Ultron beam')),
    ('welcome', 'vqB', 224, 240, dict(src=46.90, what='Vision, a look')),
    ('flame', 'sf1', 240, 257, dict(contact=138.08, hf=246, what='flame kick')),
    ('doom-punch', 'doom', 257, 287, dict(contact=98.75, hf=278, what='Doom punch')),
    ('chun', 'sf2', 287, 304, dict(src=108.20, what='Chun-Li')),
    ('beam', 'vqB', 304, 312, dict(contact=72.37, hf=310, what='energy beam')),
    ('doom-face', 'doom', 312, 335, dict(src=82.08, what='Doom stare')),
    ('street', 'spF', 335, 352, dict(contact=124.62, hf=343, what='body hits the street')),
    ('flykick', 'sf2', 352, 367, dict(contact=137.07, hf=358, what='flying kick lands')),
    ('vision-beam', 'vqA', 367, 377, dict(contact=90.33, hf=375, what='Vision beam')),
    ('ken-yell', 'sf2', 377, 390, dict(src=135.15, what='Ken reacts')),
    ('collide', 'spF', 390, 409, dict(contact=129.54, hf=398, what='two bodies collide')),
    ('doom-close', 'doom', 409, 432, dict(src=62.40, what='Doom close')),
    ('canvas', 'sf1', 432, 450, dict(contact=20.59, hf=439, what='body hits the canvas')),
    ('bar', 'vqB', 450, 473, dict(src=8.28, what='Vision at the counter')),
    ('web', 'spN', 473, 495, dict(contact=43.66, hf=479, what='web yanks him off his feet')),
    ('chun-kick', 'sf1', 495, 514, dict(contact=122.33, hf=503, what="Chun-Li's kick")),
    ('green', 'sf1', 514, 556, dict(contact=80.16, hf=525, what='green kick')),
    ('blanka', 'sf1', 556, 566, dict(src=81.193, what='Blanka reacts')),
    ('group', 'doom', 566, 578, dict(contact=95.36, hf=567, what='punch to the face')),
    ('knew', 'spF', 578, 623, dict(src=27.40, what='a look between them')),
    ('boom', 'vqB', 623, 633, dict(contact=118.91, hf=631, what='explosion')),
    ('scramble', 'sf2', 633, 645, dict(contact=140.87, hf=640, what='ground fight')),
    ('beam2', 'vqB', 645, 666, dict(contact=101.46, hf=664, what='beam hits')),
    ('sp-punch', 'spF', 666, 691, dict(contact=97.55, hf=688, what='Spider-Man punch')),
    ('ground', 'sf2', 691, 699, dict(contact=118.05, hf=696, what='ground punch')),
    ('win', 'sf2', 699, 732, dict(src=48.50, speech="I'M GOING TO WIN IT ALL", color=RED,
                                 what="Ken: I'm going to win it all")),
]


def build():
    segs = []
    for i, (name, key, f0, f1, extra) in enumerate(RAW):
        if i and f0 != RAW[i - 1][2 + 1]:
            # f1 of previous is index 3
            pass
        if i and f0 != RAW[i - 1][3]:
            raise SystemExit(f'gap {RAW[i-1][0]} -> {name}')
        s = dict(name=name, key=key, f0=f0, f1=f1, **extra)
        s['n'] = f1 - f0
        s['t0'] = f0 / FPS
        s['t1'] = f1 / FPS
        s['dur'] = s['n'] / FPS
        if 'hf' in s:
            if not (f0 <= s['hf'] < f1):
                raise SystemExit(f"{name}: hit frame {s['hf']} not in {f0}-{f1}")
            s['hit'] = s['hf'] / FPS
            s['src'] = s['contact'] - (s['hf'] - f0) / FPS
        if s['n'] < 2 or s['src'] < 0:
            raise SystemExit(f'bad seg {name} n={s["n"]} src={s["src"]}')
        segs.append(s)
    by = {}
    for s in segs:
        by.setdefault(s['key'], []).append(s)
    for k, xs in by.items():
        xs.sort(key=lambda s: s['src'])
        for a, b in zip(xs, xs[1:]):
            if b['src'] < a['src'] + a['dur'] - 0.03:
                raise SystemExit(
                    f"overlap {k}: {a['name']} {a['src']:.2f}+{a['dur']:.2f} vs {b['name']} {b['src']:.2f}")
    return segs


def grab(src, st, n, dst):
    pre = max(0.0, st - 0.8)
    post = st - pre
    vf = f'fps={FPS},scale={W}:{H}:flags=lanczos,setsar=1,{GRADE}'
    subprocess.run(
        ['ffmpeg', '-v', 'error', '-y', '-ss', f'{pre:.3f}', '-i', src, '-ss', f'{post:.3f}',
         '-frames:v', str(n), '-an', '-vf', vf,
         '-c:v', 'libx264', '-crf', '14', '-preset', 'veryfast', '-pix_fmt', 'yuv420p', dst],
        check=True)


def render(out):
    segs = build()
    tmp = '/tmp/f157/build'
    os.makedirs(tmp, exist_ok=True)
    end = segs[-1]['t1']
    print(f'END {end:.3f}  shots {len(segs)}')
    for s in segs:
        hit = f"  HIT {s['hit']:.3f}" if 'hit' in s else ''
        print(f"{s['t0']:7.3f}-{s['t1']:7.3f} {s['key']:4} @{s['src']:.3f} {s['what']}{hit}", flush=True)
    parts = []
    for i, s in enumerate(segs):
        p = os.path.join(tmp, f"s{i:02d}.mp4")
        grab(SRC[s['key']], s['src'], s['n'], p)
        parts.append(p)
    lst = os.path.join(tmp, 'list.txt')
    open(lst, 'w').write(''.join(f"file '{p}'\n" for p in parts))
    vid = os.path.join(tmp, 'video.mp4')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', lst, '-c', 'copy', vid], check=True)

    words = [(s['t0'] + 0.05, s['t1'] - 0.05, s['speech'], s['color']) for s in segs if s.get('speech')]
    pngs = []
    for i, (_, _, text, col) in enumerate(words):
        pngs.append(wmtext.word_png(text, W, H, os.path.join(tmp, f'w{i}.png'),
                                    size=int(H * 0.078), opacity=0.80, cy=0.60, color=col))
    cmd = ['ffmpeg', '-v', 'error', '-y', '-i', vid, '-i', SONG]
    for p in pngs:
        cmd += ['-loop', '1', '-framerate', str(FPS), '-t', f'{end:.3f}', '-i', p]
    speech_segs = [s for s in segs if s.get('speech')]
    for s in speech_segs:
        cmd += ['-ss', f'{s["src"]:.3f}', '-t', f'{s["dur"]:.3f}', '-i', SRC[s['key']]]
    hits = [s for s in segs if 'hit' in s]
    for s in hits:
        a = s['contact'] - 0.05
        cmd += ['-ss', f'{max(0.0, a):.3f}', '-t', '0.55', '-i', SRC[s['key']]]

    chain, last = wmtext.overlay_filter([(a, b, t) for a, b, t, _ in words], 2, '[0:v]')
    n0 = 2 + len(pngs)
    fx, labels = '', []
    for j, s in enumerate(speech_segs):
        fx += (f"[{n0+j}:a]aformat=channel_layouts=stereo,volume=2.4,"
               f"afade=t=in:d=0.02,afade=t=out:st={max(0.05, s['dur']-0.12):.3f}:d=0.12,"
               f"adelay={int(s['t0']*1000)}|{int(s['t0']*1000)}[d{j}];")
        labels.append(f'[d{j}]')
    n1 = n0 + len(speech_segs)
    for j, s in enumerate(hits):
        when = s['hit'] - 0.05
        fx += (f"[{n1+j}:a]aformat=channel_layouts=stereo,volume=2.1,"
               f"afade=t=in:d=0.012,afade=t=out:st=0.22:d=0.30,"
               f"adelay={int(max(0, when)*1000)}|{int(max(0, when)*1000)}[x{j}];")
        labels.append(f'[x{j}]')
    speech_duck = '+'.join(f"between(t,{s['t0']:.3f},{s['t1']:.3f})" for s in speech_segs)
    hit_duck = '+'.join(f"between(t,{s['hit']-0.03:.3f},{s['hit']+0.22:.3f})" for s in hits)
    vol = f"0.82*if(gt({speech_duck},0),0.30,1)*if(gt({hit_duck},0),0.55,1)"
    fx += (f"[1:a]atrim=0:{end:.3f},asetpts=PTS-STARTPTS,volume='{vol}':eval=frame,"
           f"afade=t=in:d=0.04,afade=t=out:st={end-0.45:.3f}:d=0.45[song];"
           f"[song]{''.join(labels)}amix=inputs={len(labels)+1}:normalize=0:duration=first,alimiter=limit=0.92[a]")
    subprocess.run(cmd + ['-filter_complex', chain + fx, '-map', last, '-map', '[a]',
                          '-t', f'{end:.3f}', '-r', str(FPS),
                          '-c:v', 'libx264', '-crf', '16', '-preset', 'veryfast', '-pix_fmt', 'yuv420p',
                          '-c:a', 'aac', '-b:a', '192k', out], check=True)
    print(out)
    return segs


if __name__ == '__main__':
    render(sys.argv[1] if len(sys.argv) > 1 else '/tmp/f157/master.mp4')
