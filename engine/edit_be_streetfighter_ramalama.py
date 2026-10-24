"""BE - MOVIE: STREET FIGHTER (in cinemas Oct 16 2026) x "Ramalama (Bang Bang)" - Roisin Murphy (#114).
Built like ref K1 (@kam_cuts) + Desmond Oct 24: the LYRIC picks the picture and the MOVIE'S OWN SOUND is laid on the song.
Lyric map (measured, three whisper passes + drum hits):
  0-4.4 "ramalama" x3 -> the faces (fist bump, Ken, Guile, Balrog, Chun-Li, Blanka, Ryu), a cut every beat
  4.40 "the bing" = wind-up (Ken leaps)  4.90 BANG = Balrog's glove hits the lens
  5.66 CRASH = explosion   5.92 BANG = Ken's flame kick   6.64 bing / 7.04 BANG = Ken's punch lands
  7.56 bing / 8.04 BANG = the red punch   9.00 CRASH = Blanka's lightning   9.30 BANG = body hits the canvas
  10.92 / 11.98 "whoa" = Chun-Li screams in the fire / the Hadouken charges
  13.8-18.4 the bing-bong chops = an exchange on every beat
  18.4-23 "and if I need a rhythm, it'll be to my heart I listen" = Ryu alone, Ryu and Ken, the title on "listen".
Every BANG/CRASH: the contact frame sits on the word and the trailer's own hit sound plays on top of the song.
Footage: official trailers + clip (IMDb, 1920x1080 23.976, letterboxed), pixels 1:1."""
import os, sys, subprocess
sys.path.insert(0, os.path.dirname(__file__))
import wmtext

S = os.environ.get('SCRATCH', '/tmp')
SRC = os.environ.get('DEX_SF', os.path.join(S, 'sf'))
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SONG = os.path.join(os.path.dirname(ROOT), 'dex-edits-assets', 'songs', '114_ramalama_bang_bang_r_is_n_murphy.mp3')
FPS = 30
W, H = 1920, 1080
GRADE = 'eq=contrast=1.06:saturation=1.08'
F = {k: os.path.join(SRC, k + '.mp4') for k in ('t1', 't2', 'blanka')}
END = 24.0

# (edit time, source, source in-point, take end) - the in-point puts the contact frame on the word
SHOTS = [
    (0.00, 't2', 143.72, 144.27),   # Ryu and Ken, fists touch
    (0.55, 't2', 135.00, 135.68),   # Ken screams
    (1.18, 't1', 12.95, 13.96),     # Guile
    (1.74, 't2', 52.00, 52.76),     # Balrog in the ring
    (2.32, 't2', 108.16, 108.68),   # Chun-Li
    (2.85, 't2', 112.60, 113.52),   # Blanka
    (3.44, 't2', 151.90, 153.94),   # Ryu in the blue
    (3.99, 't2', 40.95, 41.64),     # "the bing" - Ken leaps
    (4.65, 't2', 50.15, 50.76),     # BANG 4.90 - the glove hits the lens (contact 50.40)
    (5.28, 't2', 116.12, 116.95),   # kick
    (5.66, 't2', 122.95, 123.67),   # CRASH - explosion
    (5.92, 't1', 138.06, 138.76),   # BANG - flash, Ken's flame kick
    (6.62, 't2', 37.55, 38.28),     # bing 6.64 / BANG 7.04 - Ken's punch lands (contact 37.97)
    (7.30, 't2', 146.10, 146.88),   # flying kick
    (7.84, 't1', 40.60, 42.36),     # bing / BANG 8.04 - red punch (contact 40.80)
    (8.48, 't1', 134.30, 135.12),   # neon flip
    (9.00, 'blanka', 25.96, 28.08), # CRASH - Blanka's lightning bursts out of the dark
    (9.30, 't1', 20.54, 21.06),     # BANG - body hits the canvas (impact 20.55)
    (9.83, 't1', 136.30, 138.06),   # purple energy
    (10.40, 't1', 107.50, 109.28),  # neon fighter
    (10.92, 't2', 123.67, 124.32),  # "whoa" - Chun-Li screams in the fire
    (11.53, 't2', 126.20, 127.96),  # dodge in the field
    (11.98, 't1', 156.30, 157.52),  # "whoa" - Hadouken charging
    (12.65, 't1', 159.16, 160.00),  # the fireball
    (12.99, 'blanka', 53.70, 54.52),  # electric blast
    (13.50, 't2', 136.69, 137.26),  # flying kick lands 13.80 (136.99)
    (14.06, 'blanka', 36.32, 36.96),  # Blanka lunges (36.48)
    (14.61, 't2', 140.75, 141.32),  # ground fight (141.07)
    (15.18, 't1', 85.95, 86.76),    # Cammy's kick
    (15.73, 't2', 141.90, 142.64),  # jump kick
    (16.29, 'blanka', 41.95, 43.96),  # Blanka swings (42.12)
    (16.87, 't2', 117.95, 118.83),  # punch
    (17.42, 't1', 117.00, 118.12),  # fight in the light
    (17.99, 't1', 118.12, 118.83),  # thrown to the floor
    (18.40, 't2', 2.96, 3.84),      # "and if I need a rhythm" - Ryu in the rain
    (19.13, 't2', 150.00, 151.80),  # Ryu, blue
    (19.67, 't1', 152.60, 156.24),  # "need a rhythm"
    (20.80, 't2', 131.80, 133.18),  # Ryu and Ken, the crowd
    (21.91, 't1', 141.25, 142.39),  # "my heart" - Ryu and Ken laughing
    (22.48, 't2', 154.07, 157.12),  # "I listen" - STREET FIGHTER
]
# the movie's own hit sounds: (edit time of the hit) -> its shot's sound, in sync, laid on the song
SFX = [4.90, 5.66, 5.92, 7.04, 8.04, 9.00, 9.30, 13.80, 14.22, 14.93, 16.46, 18.17]
WORDS = [(0.05, 1.70, 'RAMALAMA'), (4.90, 5.27, 'BANG'), (5.66, 5.90, 'CRASH'), (5.92, 6.55, 'BANG'), (7.04, 7.50, 'BANG'),
         (8.04, 8.46, 'BANG'), (9.00, 9.28, 'CRASH'), (9.30, 9.80, 'BANG'), (11.98, 12.60, 'WHOA'),
         (21.80, 22.46, 'TO MY HEART')]


def check():
    for i, (t, k, s, e) in enumerate(SHOTS):
        d = (SHOTS[i + 1][0] if i + 1 < len(SHOTS) else END) - t
        assert s + d <= e + 0.02, f'shot {t} runs past its take ({s + d:.2f} > {e})'


def render(out):
    check()
    tmp = os.path.join(S, 'tmp_be'); os.makedirs(tmp, exist_ok=True)
    fr = [round(t * FPS) for t, *_ in SHOTS] + [round(END * FPS)]
    parts = []
    for i, (t, k, s, e) in enumerate(SHOTS):
        part = os.path.join(tmp, f's{i:02d}.mp4'); parts.append(part)
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{s:.3f}', '-i', F[k], '-frames:v', str(fr[i + 1] - fr[i]), '-an',
                        '-vf', f'fps={FPS},scale={W}:{H},{GRADE},setsar=1', '-c:v', 'libx264', '-crf', '12', '-preset', 'fast',
                        '-pix_fmt', 'yuv420p', part], check=True)
    lst = os.path.join(tmp, 'list.txt'); open(lst, 'w').write(''.join(f"file '{x}'\n" for x in parts))
    vid = os.path.join(tmp, 'video.mp4')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', lst, '-c', 'copy', vid], check=True)
    # movie hit sounds, each from the shot it belongs to so sound and picture are the same instant
    cmd = ['ffmpeg', '-v', 'error', '-y', '-i', vid, '-i', SONG]
    pngs = [wmtext.word_png(w, W, H, os.path.join(tmp, f'w{i}.png'), size=int(H * 0.16)) for i, (_, _, w) in enumerate(WORDS)]
    for p in pngs: cmd += ['-loop', '1', '-framerate', str(FPS), '-t', f'{END:.3f}', '-i', p]
    chain, last = wmtext.overlay_filter(WORDS, 2, '[0:v]')
    n0 = 2 + len(pngs); fx, labels = '', []
    for j, w in enumerate(SFX):
        t, k, s, _ = [x for x in SHOTS if x[0] <= w][-1]
        a = s + (w - t) - 0.05
        cmd += ['-ss', f'{a:.3f}', '-t', '0.6', '-i', F[k]]
        fx += (f"[{n0 + j}:a]aformat=channel_layouts=stereo,afade=t=in:d=0.01,afade=t=out:st=0.25:d=0.35,volume=2.0,"
               f"adelay={int((w - 0.05) * 1000)}|{int((w - 0.05) * 1000)}[x{j}];")
        labels.append(f'[x{j}]')
    duck = '+'.join(f'between(t,{w - 0.03:.2f},{w + 0.22:.2f})' for w in SFX)   # the song dips under each movie hit
    fx += (f"[1:a]atrim=0:{END:.3f},volume='0.85*(1-0.45*min(1,{duck}))':eval=frame,afade=t=out:st={END - 0.4:.3f}:d=0.4[song];"
           f"[song]{''.join(labels)}amix=inputs={len(labels) + 1}:normalize=0,alimiter=limit=0.85[a]")
    subprocess.run(cmd + ['-filter_complex', chain + fx, '-map', last, '-map', '[a]', '-t', f'{END:.3f}', '-r', str(FPS),
                          '-c:v', 'libx264', '-crf', '12', '-preset', 'slow', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '256k', out], check=True)
    print(out)


if __name__ == '__main__':
    render(os.path.join(S, 'out', 'be_streetfighter_ramalama.mp4'))
