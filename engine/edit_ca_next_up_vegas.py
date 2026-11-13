"""CA - NEXT RACE: LAS VEGAS (gap-week build-up, Sat 14 Nov 12:00). Format of the 7.4M-play "NEXT UP: LAS VEGAS" TikTok
(@simply_boah, Nov 11 2025, the same gap week): slow neon intro on the strings, title card, then every beat cut on the
"Flashing Lights" hook. Our own shots and text: Vegas 2025 race + rain qualifying, Vegas 2024 (Max crowned on the Strip).
36.6 s, square in 1080x1920, 25 fps, Anton titles, no grade (the neon is the look). Song: Kanye West - Flashing Lights
(from 5.8 s: strings, hook 'Flashin' lights' at 21.78 = edit 15.98, 89 BPM).
Usage: SRC=<sources folder> SCRATCH=<work dir> python3 edit_ca_next_up_vegas.py"""
import os, sys, glob
sys.path.insert(0, os.path.dirname(__file__))
import lyric

S = os.environ.get('SCRATCH', '/tmp')
SRC = os.environ['SRC']
ASSETS = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'dex-edits-assets')
src = lambda vid: glob.glob(os.path.join(SRC, '**', f'*{vid}*.mp4'), recursive=True)[0]
SQ = 'crop=1080:1080:420:0'
FILES = {'r': (src('uQc-pW3QLuI'), SQ), 'q': (src('gC88zq9Y4gQ'), SQ), 'p': (src('sNd1-1GjMDY'), SQ)}   # r/q = 2025, p = 2024
CUTS = [  # intro: one shot every 2 beats, slowed - the neon city
        (0.00, 'q', 58.0, 0.7), (2.00, 'p', 144.0, 0.7), (4.00, 'p', 450.0, 0.7), (6.00, 'q', 24.0, 0.7),
        (8.00, 'r', 188.0, 0.7), (10.00, 'p', 186.0, 0.7), (12.00, 'r', 440.0, 0.8),
        # drop on 'Flashin' lights': every beat
        (15.98, 'p', 12.0), (16.68, 'r', 6.0), (17.35, 'p', 24.0), (18.00, 'r', 62.0), (18.65, 'p', 44.0),
        (19.32, 'r', 10.0), (20.00, 'p', 76.0), (20.65, 'q', 32.0), (21.32, 'p', 292.0), (21.97, 'q', 46.0),
        (22.62, 'p', 364.0), (23.29, 'p', 417.0), (23.96, 'r', 436.0), (24.61, 'q', 64.0), (25.29, 'p', 340.0),
        (25.94, 'r', 420.0), (26.61, 'q', 120.0), (27.26, 'p', 236.0), (27.94, 'r', 200.0), (28.59, 'p', 423.0),
        (29.26, 'r', 176.0), (29.91, 'p', 438.0), (30.58, 'r', 456.0),
        # the payoff: Max crowned on the Strip, fireworks
        (31.23, 'p', 458.5, 0.6), (32.58, 'p', 461.5, 0.7), (33.90, 'p', 476.3, 0.8)]
WORDS = [(10.00, 'NEXT RACE', 150, 2.0), (12.00, 'LAS VEGAS|NOVEMBER 19-21', 210, 3.98),
         (33.90, 'LAS VEGAS|NOVEMBER 19-21', 190, 2.7)]
CFG = dict(name='next_up_vegas', files=FILES, cuts=CUTS, end=36.6, words=WORDS, flash=[15.98, 31.23], font='anton',
           grade=False, song=os.path.join(ASSETS, 'songs', 'trend', 'flashing_lights_kanye.mp3'), song_in=5.8,
           title='NEXT RACE|LAS VEGAS', banner_in=0.6)

if __name__ == '__main__':
    fps = int(os.environ.get('DEX_FPS', 25))
    out, total = lyric.render(dict(CFG, fps=fps), S, os.path.join(S, 'out', f'ca_next_up_vegas_{fps}.mp4'))
    print(out, f'total {total:.1f}s', flush=True)
