"""CQ - SUPER SATURDAY (Sat 21 Nov 08:00, the last pre-made post of the week): MotoGP sprint at Portimão in the afternoon,
F1 race in Las Vegas on Saturday night. Two-series alternating cut on the hits of Montagem Kali: five MotoGP cuts under
'MOTOGP SPRINT | PORTIMÃO', five F1 cuts under 'F1 RACE | LAS VEGAS · SATURDAY NIGHT', then bike/car alternating on every
hit, ending on the Bellagio. Anton cards, no grade. ~28.2 s, square in 1080x1920, 25 fps.
Sources: MotoGP 'Best MotoGP Moments | 2025 Portuguese GP' (EbJMANarkcQ); F1 race highlights Las Vegas 2023 (Q9qSwDxF6YI),
2024 (sNd1-1GjMDY), 2025 (uQc-pW3QLuI) + 2025 quali (gC88zq9Y4gQ).
Usage: SRC=<sources folder> SCRATCH=<work dir> python3 edit_cq_super_saturday.py"""
import os, sys, glob
sys.path.insert(0, os.path.dirname(__file__))
import lyric

S = os.environ.get('SCRATCH', '/tmp')
SRC = os.environ['SRC']
ASSETS = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'dex-edits-assets')
src = lambda vid: glob.glob(os.path.join(SRC, '**', f'*{vid}*.mp4'), recursive=True)[0]
SQ = 'crop=1080:1080:420:0'
FILES = {'b': (src('EbJMANarkcQ'), SQ), 'a': (src('Q9qSwDxF6YI'), SQ), 'p': (src('sNd1-1GjMDY'), SQ),
         'r': (src('uQc-pW3QLuI'), SQ), 'q': (src('gC88zq9Y4gQ'), SQ)}
SONG_IN = 72.79
HITS = [76.32, 77.48, 78.67, 79.83, 81.01, 82.18, 83.36, 84.54, 85.7, 86.89, 88.05, 89.23, 90.39, 91.58, 92.74, 93.9, 95.09,
        96.25, 97.43, 98.59]                                                     # every 2nd beat from the drop (103 BPM)
SHOTS = [('b', 9.0), ('b', 30.0), ('b', 87.0), ('b', 165.0), ('b', 201.0),                     # MotoGP
         ('p', 12.0), ('r', 62.0), ('a', 27.0), ('p', 252.0), ('r', 200.0),                    # F1
         ('b', 63.0), ('q', 64.0), ('b', 99.0), ('a', 337.0), ('b', 186.0), ('p', 186.0),      # alternating
         ('b', 243.0), ('p', 459.0), ('b', 228.0), ('r', 440.0, 0.6)]
CUTS = [(0.0, 'b', 15.0, 0.6)] + [(round(h - SONG_IN, 2), *sh) for h, sh in zip(HITS, SHOTS)]
END = round(HITS[-1] - SONG_IN + 2.4, 2)
WORDS = [(0.2, 'SUPER SATURDAY.', 190, 3.3), (CUTS[1][0], 'MOTOGP SPRINT|PORTIMÃO', 210, 2.2),
         (CUTS[6][0], 'F1 RACE|LAS VEGAS · SATURDAY NIGHT', 230, 2.2), (CUTS[20][0], 'SUPER SATURDAY.|SPRINT + RACE', 190, 2.4)]
CFG = dict(name='super_saturday', files=FILES, cuts=CUTS, end=END, words=WORDS, flash=[CUTS[1][0], CUTS[6][0], CUTS[11][0]],
           font='anton', grade=False, song=os.path.join(ASSETS, 'songs', 'full', '05_montagem_kali_slowed.mp3'), song_in=SONG_IN,
           title='SUPER SATURDAY|MOTOGP + F1', banner_in=0.6)

if __name__ == '__main__':
    fps = int(os.environ.get('DEX_FPS', 25))
    out, total = lyric.render(dict(CFG, fps=fps), S, os.path.join(S, 'out', f'cq_super_saturday_{fps}.mp4'))
    print(out, f'total {total:.1f}s', flush=True)
