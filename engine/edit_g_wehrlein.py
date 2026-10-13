"""Edit G - VELOCITY edit. Direction: "Pole on Saturday. P14 on Sunday. Still world champion."
Pascal Wehrlein's 2026 Formula E title weekend in London (Porsche newsroom footage).
Song: Montagem Kali (slowed). Every cut sits on a detected drum hit (snapped grid), 60 fps."""
import os, sys, json, math, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, os.path.dirname(__file__))
from velocity import prep, Seq, frame_for, cut_frames, W, H, FPS
_a = sys.argv; sys.argv = [sys.argv[0]]
from edit_c_justdance import flash, chroma, zoom, dec, ease, fnt, VIG, GRAIN, ROOT
sys.argv = _a

SRC = os.path.join(ROOT, 'src_car')
SONG = os.path.join(ROOT, 'songs', 'named', '05_montagem_kali_slowed.m4a')
OUT = os.path.join(ROOT, 'out', 'edit_G_wehrlein_velocity.mp4')
CUTS = json.load(open(os.path.join(ROOT, 'songs', '05_grid.json')))['cuts']
SAT, SUN = 'p338752.mp4', 'p338815.mp4'

# (file, src_in, cx, mode) - one per cut segment, story order
PLAN = [                       # every shot from a DIFFERENT take (checked in __main__)
    (SUN, 59.60, 0.50, 'hero'),   # hook: champion on the podium
    (SAT, 3.07, 0.50, 'hero'),    # helmet on
    (SAT, 7.00, 0.62, 'vel'),     # start lights
    (SUN, 8.80, 0.55, 'vel'),     # launch
    (SAT, 15.00, 0.50, 'vel'),    # into turn 1
    (SAT, 26.00, 0.55, 'vel'),    # Porsche cornering close
    (SAT, 30.00, 0.45, 'vel'),    # SATURDAY.
    (SAT, 19.00, 0.50, 'vel'),
    (SAT, 21.00, 0.68, 'vel'),    # big screen: 1st PASCAL WEHRLEIN
    (SAT, 57.30, 0.35, 'vel'),
    (SAT, 62.40, 0.50, 'vel'),    # finish + fireworks
    (SAT, 66.90, 0.50, 'slow'),   # arms up, Saturday win
    (SUN, 36.40, 0.50, 'slow'),   # SUNDAY. on-board
    (SUN, 37.60, 0.38, 'vel'),    # wheel to wheel
    (SUN, 31.00, 0.50, 'vel'),    # chaos, smoke
    (SUN, 28.00, 0.45, 'vel'),    # P14.
    (SUN, 24.50, 0.50, 'vel'),
    (SUN, 19.50, 0.50, 'vel'),
    (SUN, 15.20, 0.50, 'vel'),
    (SUN, 11.00, 0.50, 'vel'),
    (SUN, 17.50, 0.50, 'vel'),
    (SUN, 51.50, 0.50, 'vel'),    # BUT… finish sparks
    (SUN, 52.80, 0.50, 'vel'),
    (SUN, 48.00, 0.55, 'hero'),   # STILL WORLD CHAMPION (the screen)
    (SUN, 57.40, 0.45, 'slow'),   # crew in tears
    (SUN, 61.60, 0.60, 'vel'),    # trophy lift
    (SUN, 66.50, 0.50, 'vel'),    # confetti
    (SUN, 54.60, 0.50, 'vel'),    # hugs
    (SUN, 62.90, 0.50, 'hero'),   # 169 PTS on stage
    (SUN, 70.40, 0.45, 'hero'),   # PASCAL WEHRLEIN on shoulders
]
END = 26.6
bounds = [0.0] + CUTS[1:len(PLAN)] + [END]
SHOTS = [dict(file=p[0], src=p[1], cx=p[2], mode=p[3], t0=bounds[i], t1=bounds[i + 1]) for i, p in enumerate(PLAN)]
CF = cut_frames([s['t0'] for s in SHOTS[1:]])                 # hit frames

TEXT = [(0.128, 1.30, '2X WORLD|CHAMPION'), (1.30, 2.48, 'LONDON.|AUGUST 2026.'),
        (5.704, 7.17, 'SATURDAY.'), (7.171, 8.63, 'POLE.|WIN.'),
        (10.39, 11.85, 'SUNDAY.'), (12.74, 14.21, 'P14.'),
        (17.425, 18.89, 'BUT…'), (18.892, 20.06, 'STILL|WORLD CHAMPION.'),
        (23.582, 24.75, '169 PTS.|5 CLEAR.'), (24.752, END, 'PASCAL|WEHRLEIN')]

_tc = {}
def tl(text):
    if text in _tc: return _tc[text]
    lines = text.split('|'); size = 128; f = fnt(size)
    while max(f.getbbox(l)[2] for l in lines) > 960: size -= 6; f = fnt(size)
    m = Image.new('L', (W, H), 0); d = ImageDraw.Draw(m); lh = int(size * 1.1); y0 = int(H * 0.5) - lh * len(lines) // 2
    for i, l in enumerate(lines):
        bb = f.getbbox(l); d.text(((W - bb[2]) / 2, y0 + i * lh), l, font=f, fill=255)
    m = np.asarray(m).astype(np.float32) / 255
    sh = np.asarray(Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(14))).astype(np.float32) / 255
    _tc[text] = (np.where(m[..., None] > 0.01, 1.0, 0.0).astype(np.float32), np.clip(m + sh * 0.65, 0, 1)[..., None])
    return _tc[text]


def look(a):
    lum = a @ np.array([0.299, 0.587, 0.114], np.float32)
    a = lum[..., None] + (a - lum[..., None]) * 1.15
    a = np.clip((a - 0.03) * 1.08, 0, 1); s = a * a * (3 - 2 * a); a = s * 0.45 + a * 0.55
    return np.clip(a + (1 - lum[..., None]) * np.array([-0.015, 0.0, 0.03]), 0, 1)


def render(f, seqs, paths):
    t = f / FPS
    i = next(i for i, s in enumerate(SHOTS) if (CF[i - 1] if i else 0) <= f < (CF[i] if i < len(CF) else 10 ** 9))
    s = SHOTS[i]
    start_f = CF[i - 1] if i else 0
    end_f = CF[i] if i < len(CF) else int(END * FPS)
    lt, dur = (f - start_f) / FPS, (end_f - start_f) / FPS
    if i not in seqs:
        for q in seqs.values(): q.close()
        seqs.clear(); seqs[i] = Seq(paths[i])
    a = look(frame_for(seqs[i], s['mode'], lt, dur))
    hitk = (f - start_f) / FPS if i else 99            # time since this shot's hit (0 on the hit frame)
    big = s['mode'] == 'hero' or i in (8, 21, 23, 25)
    z = 1.0 + (0.16 if big else 0.09) * dec(hitk, 0.09)
    a = zoom(a, z)
    a = flash(a, (0.85 if big else 0.4) * dec(hitk, 0.05))      # peaks on the hit frame
    a = chroma(a, (14 if big else 7) * dec(hitk, 0.08))
    if hitk < 0.12: a = np.roll(a, int(14 * dec(hitk, 0.05) * (1 if f % 2 else -1)), 1)
    if t > END - 0.8: a = a * (1 - ease((t - (END - 0.8)) / 0.8))
    for (s0, s1, txt) in TEXT:
        if s0 <= t < s1:
            rgb, al = tl(txt); p = ease((t - s0) / 0.08); k = p * (1 - ease((t - (s1 - 0.06)) / 0.06))
            a = a * (1 - al * k) + rgb * al * k
    a = a * VIG + GRAIN[f % 4] * 0.5
    return np.clip(a, 0, 1)


if __name__ == '__main__':
    import velocity
    _t = []
    for sh in SHOTS:
        sh['src'] = velocity.clean_span(os.path.join(SRC, sh['file']), sh['src'],
                                        velocity.src_needed(sh['mode'], sh['t1'] - sh['t0']) + 0.15)
        _c = velocity.source_cuts(os.path.join(SRC, sh['file'])); _t.append((sh['file'], sum(1 for x in _c if x <= sh['src'] + 0.02)))
    assert len(set(_t)) == len(_t), f'repeated take: {_t}'
    paths = prep(SHOTS, SRC, os.path.join(ROOT, 'tmp_g'))
    seqs = {}
    if len(sys.argv) > 1:
        for ts in sys.argv[1:]:
            t = float(ts); seqs = {}
            i = next(i for i, s in enumerate(SHOTS) if s['t0'] <= t < s['t1'])
            for f in range((CF[i - 1] if i else 0), int(t * FPS) + 1):
                a = render(f, seqs, paths)
            Image.fromarray((a * 255).astype(np.uint8)).save(os.path.join(ROOT, 'out', f'G_{t:.2f}.jpg'))
        sys.exit()
    tmp = OUT + '.v.mp4'
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS),
                          '-i', '-', '-c:v', 'libx264', '-preset', 'medium', '-crf', '17', '-pix_fmt', 'yuv420p', tmp], stdin=subprocess.PIPE)
    for f in range(int(END * FPS)):
        p.stdin.write((render(f, seqs, paths) * 255).astype(np.uint8).tobytes())
        if f % 120 == 0: print(f, flush=True)
    p.stdin.close(); p.wait()
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', tmp, '-i', SONG, '-map', '0:v', '-map', '1:a', '-c:v', 'copy',
                    '-af', f'afade=t=out:st={END - 1.0}:d=1.0', '-c:a', 'aac', '-b:a', '256k', '-t', str(END),
                    '-movflags', '+faststart', OUT], check=True)
    os.remove(tmp); print('done', OUT)
