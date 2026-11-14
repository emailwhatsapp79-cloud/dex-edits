"""CK - Las Vegas: 3 years, 3 winners (Thu 19 Nov 08:00, race week). Countdown/title-card style: '3 YEARS. 3 WINNERS.' on
the quiet break, then three 10-cut sections on the chorus, each opening on a big year card (2023 MAX VERSTAPPEN, 2024
GEORGE RUSSELL, 2025 MAX VERSTAPPEN), ending on the Sphere: '2026 | WHO WINS?'. Anton, no grade. ~34.5 s, square in
1080x1920, 25 fps. Song: Housewife - Tate McRae (Trend 48, +15K UK/worldwide Nov 13), 136 BPM, from 33.0 s (break), chorus
on 37.41 = edit 4.41, cut every 2 beats (0.894 s).
Sources: F1 race highlights Las Vegas 2023 (Q9qSwDxF6YI), 2024 (sNd1-1GjMDY), 2025 (uQc-pW3QLuI) + 2025 quali (gC88zq9Y4gQ).
Usage: SRC=<sources folder> SCRATCH=<work dir> python3 edit_ck_vegas_three_winners.py"""
import os, sys, glob
sys.path.insert(0, os.path.dirname(__file__))
import lyric

S = os.environ.get('SCRATCH', '/tmp')
SRC = os.environ['SRC']
ASSETS = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'dex-edits-assets')
src = lambda vid: glob.glob(os.path.join(SRC, '**', f'*{vid}*.mp4'), recursive=True)[0]
SQ = 'crop=1080:1080:420:0'
FILES = {'a': (src('Q9qSwDxF6YI'), SQ), 'p': (src('sNd1-1GjMDY'), SQ), 'r': (src('uQc-pW3QLuI'), SQ), 'q': (src('gC88zq9Y4gQ'), SQ)}
STEP, T0 = 0.894, 4.41
SEC = {'a': [9.0, 21.0, 155.5, 186.0, 205.0, 274.0, 330.0, 361.0, 462.0, 468.3],      # 2023: Max
       'p': [12.0, 42.0, 87.0, 126.0, 186.0, 252.0, 282.0, 393.0, 405.0, 409.0],     # 2024: Russell
       'r': [6.0, 10.0, 62.0, 188.0, 200.0, 300.0, 404.0, 408.0, 420.0, 436.0]}      # 2025: Max
CUTS = [(0.00, 'q', 58.0, 0.6), (2.20, 'p', 144.0, 0.6)]
for n, k in enumerate(['a', 'p', 'r']):
    for m, t in enumerate(SEC[k]):
        CUTS.append((round(T0 + STEP * (10 * n + m), 2), k, t))
END_AT = round(T0 + STEP * 30, 2)                                                     # 31.23
CUTS.append((END_AT, 'p', 450.0, 0.6))
WORDS = [(0.20, '3 YEARS.', 210, 2.0), (2.20, '3 WINNERS.', 200, 2.2),
         (T0, '2023|MAX VERSTAPPEN', 260, 1.6), (round(T0 + STEP * 10, 2), '2024|GEORGE RUSSELL', 260, 1.6),
         (round(T0 + STEP * 20, 2), '2025|MAX VERSTAPPEN', 260, 1.6), (END_AT, '2026|WHO WINS?', 260, 3.3)]
CFG = dict(name='vegas_three_winners', files=FILES, cuts=CUTS, end=END_AT + 3.3, words=WORDS, flash=[T0, END_AT],
           font='anton', grade=False, song=os.path.join(ASSETS, 'songs', 'trend', 'housewife_tate_mcrae.mp3'), song_in=33.0,
           title='LAS VEGAS|3 YEARS, 3 WINNERS', banner_in=0.6)

if __name__ == '__main__':
    fps = int(os.environ.get('DEX_FPS', 25))
    out, total = lyric.render(dict(CFG, fps=fps), S, os.path.join(S, 'out', f'ck_vegas_three_winners_{fps}.mp4'))
    print(out, f'total {total:.1f}s', flush=True)
