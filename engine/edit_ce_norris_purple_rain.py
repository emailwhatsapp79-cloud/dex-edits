"""CE - Las Vegas 2025 qualifying: Norris on pole in the rain, on "Purple Rain" (Prince - Trend 48 worldwide top 20 on
Nov 13). Tue 17 Nov 08:00. Cinematic: slowed shots (0.6x), the film grade, one big serif word per chorus line - rain on
neon, spray, sparks, the pink Alpine halo, Norris's onboard, the McLaren garage, Norris's arms up. 36.5 s, square in
1080x1920, 25 fps. Song from 38.0 s ('...laughing in the purple rain' 46.34 = edit 8.34; 'Purple rain' 48.58/56.62/64.52
= edit 10.58/18.62/26.52).
Sources: F1 'Qualifying Highlights | 2025 Las Vegas Grand Prix' (gC88zq9Y4gQ).
Usage: SRC=<sources folder> SCRATCH=<work dir> python3 edit_ce_norris_purple_rain.py"""
import os, sys, glob
sys.path.insert(0, os.path.dirname(__file__))
import lyric

S = os.environ.get('SCRATCH', '/tmp')
SRC = os.environ['SRC']
ASSETS = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'dex-edits-assets')
src = lambda vid: glob.glob(os.path.join(SRC, '**', f'*{vid}*.mp4'), recursive=True)[0]
FILES = {'q': (src('gC88zq9Y4gQ'), 'crop=1080:1080:420:0')}
CUTS = [(0.00, 'q', 58.0, 0.6), (2.80, 'q', 150.0, 0.6), (5.60, 'q', 195.0, 0.6), (8.34, 'q', 26.0, 0.6),
        (10.58, 'q', 201.0, 0.6), (12.32, 'q', 46.0, 0.5), (14.40, 'q', 336.0, 0.6), (16.50, 'q', 414.0, 0.6),
        (18.62, 'q', 30.0, 0.6), (20.70, 'q', 417.0, 0.6), (22.70, 'q', 228.0, 0.8), (24.60, 'q', 375.0, 0.6),
        (26.52, 'q', 405.0, 0.6), (29.10, 'q', 408.0, 0.6), (31.00, 'q', 399.0, 0.8), (32.80, 'q', 444.0, 0.6)]
WORDS = [(8.34, 'RAIN.', 240, 2.0), (10.58, 'PURPLE RAIN.', 170, 1.6), (18.62, 'LAS VEGAS.', 190, 1.8),
         (26.52, 'NORRIS.', 220, 2.0), (32.80, 'POLE.', 260, 3.7)]
CFG = dict(name='norris_purple_rain', files=FILES, cuts=CUTS, end=36.5, words=WORDS, flash=[26.52], font='serif',
           grade=True, song=os.path.join(ASSETS, 'songs', 'trend', 'purple_rain_prince.mp3'), song_in=38.0,
           title='LANDO NORRIS|POLE IN THE PURPLE RAIN', banner_in=0.6)

if __name__ == '__main__':
    fps = int(os.environ.get('DEX_FPS', 25))
    out, total = lyric.render(dict(CFG, fps=fps), S, os.path.join(S, 'out', f'ce_norris_purple_rain_{fps}.mp4'))
    print(out, f'total {total:.1f}s', flush=True)
