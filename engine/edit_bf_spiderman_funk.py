"""BF - MOVIE: SPIDER-MAN: BRAND NEW DAY x "Funk Unico (super slowed)" - ICEDMANE (#13). Shape of ref U1 (Gru, "the moon"):
the film's own line builds over the quiet part of the song, its payoff word IS the drop, then the hero on every beat.
  0-15.8  Peter's letter, his own voice, the trailer's picture in sync with what he says (official trailer 1):
          "Hi, my name is Peter Parker." / "You don't remember me, but we used to know each other." / "Something bad was
          going to happen, and the only way to stop it was to make everyone forget about me." / "Because I'm not just
          Peter Parker... I'm Spider-" - mask on, he runs, he dives off the tower
  15.84   "-MAN" = the drop (song 21.29). SPIDER-MAN on the rooftop, then a cut on every beat (0.627 s): swings, the car
          through the building, the explosion, the Hand, the fight, the mask, the title.
Words: each word appears as he says it, white glow, just below the middle (60% down) - you see the film through them.
Footage: official trailers (IMDb, 1920x1080 23.976, letterbox kept), pixels 1:1. Old-film recap shots of the final trailer
are not used."""
import os, sys, subprocess
sys.path.insert(0, os.path.dirname(__file__))
import wmtext
from PIL import Image, ImageDraw, ImageFont, ImageFilter

S = os.environ.get('SCRATCH', '/tmp')
SRC = os.environ.get('DEX_SM', os.path.join(S, 'sm'))
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SONG = os.path.join(os.path.dirname(ROOT), 'dex-edits-assets', 'songs', '13_funk_unico_super_slowed.mp3')
FPS, W, H = 30, 1920, 1080
GRADE = 'eq=contrast=1.06:saturation=1.08'
F = {k: os.path.join(SRC, k + '.mp4') for k in ('t1', 'new', 'final')}
TALK = [(26.55, 28.95), (30.90, 33.52), (34.35, 40.40), (42.26, 46.92)]   # t1 source spans, voice + picture in sync
PIC_LEAD = {3: 0.19}   # span 4 opens on a fade from black: its picture starts 0.19 s later than his voice (voice-over)
DROP = sum(b - a for a, b in TALK)                                        # 15.84 - "-MAN"
OFF = 21.293 - DROP                                                       # song second that plays at edit 0
BEAT = lambda k: 21.293 + k * 0.6275 - OFF                                # edit time of the k-th beat after the drop
AFTER = [  # (beats held, source, in-point, take end)
    (2, 't1', 8.40, 10.16),      # SPIDER-MAN on the tower
    (1, 't1', 18.70, 21.10),     # swing past the glass
    (1, 'new', 41.36, 42.00),    # swing
    (1, 't1', 127.90, 128.96),   # swing through the city
    (1, 't1', 128.98, 129.88),   # swing
    (1, 'new', 57.20, 58.27),    # the car through the building
    (1, 't1', 104.10, 104.76),   # explosion in the street
    (1, 'new', 123.56, 124.42),  # webs across the ceiling
    (1, 'final', 127.86, 129.55),  # the Hand
    (1, 'new', 119.72, 120.66),  # the fight
    (1, 'final', 114.38, 115.03),  # the hit
    (1, 't1', 129.90, 130.63),   # over the water
    (1, 'final', 91.20, 97.51),  # the mask, the city
    (1, 't1', 93.94, 94.60),     # it hurts
    (2, 't1', 51.82, 53.08),     # crouched on the car
    (3, 't1', 140.20, 142.88),   # SPIDER-MAN: BRAND NEW DAY
]
END = BEAT(sum(n for n, *_ in AFTER))
SFX = [(5, 0.10), (6, 0.05)]     # (AFTER index, offset into the shot of its hit) - the crash and the blast, their own sound
# his words, source (t1) times; a new line starts at '|'
WORDS = [(26.62, 'HI,'), (27.52, 'MY'), (27.64, 'NAME'), (27.86, 'IS'), (28.08, 'PETER'), (28.36, 'PARKER.'),
         (31.00, '|YOU'), (31.10, "DON'T"), (31.32, 'REMEMBER'), (31.60, 'ME,'), (31.94, '|BUT'), (32.22, 'WE'), (32.54, 'USED'),
         (32.72, 'TO'), (32.84, 'KNOW'), (32.94, 'EACH'), (33.14, 'OTHER.'),
         (34.42, '|SOMETHING'), (34.64, 'BAD'), (34.90, 'WAS'), (35.08, 'GOING'), (35.18, 'TO'), (35.40, 'HAPPEN,'),
         (35.80, '|AND'), (35.86, 'THE'), (36.02, 'ONLY'), (36.16, 'WAY'), (36.30, 'TO'), (36.58, 'STOP'), (36.80, 'IT'),
         (37.30, '|WAS'), (37.84, 'TO'), (38.08, 'MAKE'), (38.26, 'EVERYONE'), (38.78, 'FORGET'), (39.16, 'ABOUT'), (39.40, 'ME.'),
         (42.28, '|BECAUSE'), (42.64, "I'M"), (42.82, 'NOT'), (43.02, 'JUST'), (43.32, 'PETER'), (43.64, 'PARKER...'),
         (46.10, "|I'M")]


def edit_t(src_t):
    e = 0.0
    for a, b in TALK:
        if a <= src_t <= b: return e + src_t - a
        e += b - a
    raise ValueError(src_t)


def glow_png(text, out, size=74, cy=0.6):
    """Spoken words: white caps with a soft glow, see-through, just below the middle."""
    f = ImageFont.truetype(wmtext.FONT, size)
    try: f.set_variation_by_axes([800, 112])
    except Exception: pass
    while f.getlength(text) > W * 0.8 and size > 30:                       # long lines shrink to fit, never off-screen
        size -= 4; f = ImageFont.truetype(wmtext.FONT, size)
        try: f.set_variation_by_axes([800, 112])
        except Exception: pass
    box = f.getbbox(text); tw = box[2] - box[0]; th = box[3] - box[1]
    x, y = (W - tw) // 2 - box[0], int(H * cy - th / 2) - box[1]
    txt = Image.new('L', (W, H), 0); ImageDraw.Draw(txt).text((x, y), text, font=f, fill=235)
    glow = txt.filter(ImageFilter.GaussianBlur(9)).point(lambda v: min(255, v * 2) * 0.7)
    a = Image.fromarray(__import__('numpy').maximum(__import__('numpy').array(txt), __import__('numpy').array(glow)).astype('uint8'))
    img = Image.new('RGBA', (W, H), (255, 255, 255, 0)); img.putalpha(a.point(lambda v: int(v * 0.88)))
    img.save(out); return out


def captions():
    """Word-by-word build: one state per spoken word, held until the next word (or 0.35 s after the line ends)."""
    states, line = [], []
    ends = {26.62: 28.95, 31.00: 31.94, 31.94: 33.52, 34.42: 35.80, 35.80: 37.30, 37.30: 40.10, 42.28: 44.70, 46.10: 46.92}
    starts = [t for t, w in WORDS if w.startswith('|')] + [WORDS[0][0]]
    for i, (t, w) in enumerate(WORDS):
        if w.startswith('|'): line = []; w = w[1:]
        line.append(w)
        nxt = WORDS[i + 1][0] if i + 1 < len(WORDS) else 46.92
        if i + 1 < len(WORDS) and WORDS[i + 1][1].startswith('|'):
            ls = max(s for s in starts if s <= t); nxt = min(nxt, ends.get(ls, nxt))
        states.append((edit_t(t), edit_t(min(nxt, 46.91)) if nxt < 46.92 else DROP - 0.001, ' '.join(line)))
    return states


def render(out):
    tmp = os.path.join(S, 'tmp_bf'); os.makedirs(tmp, exist_ok=True)
    parts, t = [], 0.0
    def clip(k, s, d, name):
        n = round((t + d) * FPS) - round(t * FPS); p = os.path.join(tmp, name)
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{s:.3f}', '-i', F[k], '-frames:v', str(n), '-an', '-vf',
                        f'fps={FPS},scale={W}:{H},{GRADE},setsar=1', '-c:v', 'libx264', '-crf', '12', '-preset', 'fast',
                        '-pix_fmt', 'yuv420p', p], check=True)
        parts.append(p)
    for i, (a, b) in enumerate(TALK):
        clip('t1', a + PIC_LEAD.get(i, 0), b - a, f'a{i}.mp4'); t += b - a
    for i, (n, k, s, e) in enumerate(AFTER):
        d = BEAT(sum(x for x, *_ in AFTER[:i + 1])) - t
        assert s + d <= e + 0.03, f'after #{i} runs past its take ({s + d:.2f} > {e})'
        clip(k, s, d, f'b{i:02d}.mp4'); t += d
    lst = os.path.join(tmp, 'list.txt'); open(lst, 'w').write(''.join(f"file '{x}'\n" for x in parts))
    vid = os.path.join(tmp, 'video.mp4')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', lst, '-c', 'copy', vid], check=True)

    words = captions()
    pngs = [glow_png(w, os.path.join(tmp, f'c{i:02d}.png')) for i, (_, _, w) in enumerate(words)]
    big = (DROP, BEAT(2) - 0.02, 'SPIDER-MAN')
    pngs.append(wmtext.word_png('SPIDER-MAN', W, H, os.path.join(tmp, 'big.png'), size=int(H * 0.15)))
    cmd = ['ffmpeg', '-v', 'error', '-y', '-i', vid, '-ss', f'{OFF:.3f}', '-i', SONG]
    for p in pngs: cmd += ['-loop', '1', '-framerate', str(FPS), '-t', f'{END:.3f}', '-i', p]
    chain, last = wmtext.overlay_filter([(a, b, w) for a, b, w in words] + [big], 2, '[0:v]')
    n0 = 2 + len(pngs); fx, labels = '', []
    # his voice: the trailer's own sound under each talk span, in sync; the last span runs on through "-MAN"
    e = 0.0
    for i, (a, b) in enumerate(TALK):
        tail = 0.30 if i == len(TALK) - 1 else 0.0
        cmd += ['-ss', f'{a:.3f}', '-t', f'{b - a + tail:.3f}', '-i', F['t1']]
        fx += (f"[{n0 + i}:a]aformat=channel_layouts=stereo,highpass=f=90,afade=t=in:d=0.03,"
               f"afade=t=out:st={b - a + tail - 0.06:.3f}:d=0.06,volume=2.0,adelay={int(e * 1000)}|{int(e * 1000)}[v{i}];")
        labels.append(f'[v{i}]'); e += b - a
    n1 = n0 + len(TALK)
    for j, (idx, off) in enumerate(SFX):
        _, k, s, _ = AFTER[idx]; at = BEAT(sum(x for x, *_ in AFTER[:idx]))
        cmd += ['-ss', f'{s:.3f}', '-t', '0.6', '-i', F[k]]
        fx += (f"[{n1 + j}:a]aformat=channel_layouts=stereo,afade=t=out:st=0.3:d=0.3,volume=1.6,"
               f"adelay={int(at * 1000)}|{int(at * 1000)}[x{j}];")
        labels.append(f'[x{j}]')
    duck = '+'.join(f'between(t,{BEAT(sum(x for x, *_ in AFTER[:i])) - 0.02:.2f},{BEAT(sum(x for x, *_ in AFTER[:i])) + 0.25:.2f})' for i, _ in SFX)
    fx += (f"[1:a]atrim=0:{END:.3f},asetpts=PTS-STARTPTS,volume='if(lt(t,{DROP - 0.04:.3f}),0.28,1.0)*(1-0.4*min(1,{duck}))':eval=frame,"
           f"afade=t=out:st={END - 0.5:.3f}:d=0.5[song];[song]{''.join(labels)}amix=inputs={len(labels) + 1}:normalize=0,alimiter=limit=0.85[a]")
    subprocess.run(cmd + ['-filter_complex', chain + fx, '-map', last, '-map', '[a]', '-t', f'{END:.3f}', '-r', str(FPS),
                          '-c:v', 'libx264', '-crf', '12', '-preset', 'slow', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '256k', out], check=True)
    print(out, f'drop at {DROP:.2f}, end {END:.2f}')


if __name__ == '__main__':
    render(os.path.join(S, 'out', 'bf_spiderman_funk.mp4'))
