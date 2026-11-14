"""CN - VEGAS WEEK: practice starts tonight (Thu 19 Nov 18:00; FP1 is 01:30 Lagos that night). Hype schedule-card edit:
cut every 2 beats on "Bow Bow Bow" (Zeddy Will - Trend 48, moving on TikTok + YouTube Shorts), angles not used in the
week's other edits (rain onboards, aerials over the Strip, the Ferrari garage, the crowd), Anton cards with the weekend in
Vegas time: VEGAS WEEK. / PRACTICE - THURSDAY NIGHT / QUALIFYING - FRIDAY NIGHT / LIGHTS OUT - SATURDAY NIGHT.
~29.8 s, square in 1080x1920, 25 fps, no grade.
Sources: F1 race highlights Las Vegas 2023 (Q9qSwDxF6YI), 2024 (sNd1-1GjMDY), 2025 (uQc-pW3QLuI) + 2025 quali (gC88zq9Y4gQ).
Usage: SRC=<sources folder> SCRATCH=<work dir> python3 edit_cn_vegas_week_hype.py"""
import os, sys, glob
sys.path.insert(0, os.path.dirname(__file__))
import lyric

S = os.environ.get('SCRATCH', '/tmp')
SRC = os.environ['SRC']
ASSETS = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'dex-edits-assets')
src = lambda vid: glob.glob(os.path.join(SRC, '**', f'*{vid}*.mp4'), recursive=True)[0]
SQ = 'crop=1080:1080:420:0'
FILES = {'a': (src('Q9qSwDxF6YI'), SQ), 'p': (src('sNd1-1GjMDY'), SQ), 'r': (src('uQc-pW3QLuI'), SQ), 'q': (src('gC88zq9Y4gQ'), SQ)}
BEATS = [2.86, 3.76, 4.67, 5.6, 6.52, 7.45, 8.36, 9.29, 10.22, 11.15, 12.05, 13.0, 13.91, 14.84, 15.74, 16.7, 17.6, 18.53,
         19.44, 20.34, 21.29, 22.22, 23.15, 24.06, 24.98, 25.89, 26.82, 27.75, 28.68, 29.61, 30.51, 31.42]
SONG_IN = BEATS[0]
SHOTS = [('a', 144.0), ('q', 66.0), ('p', 84.0), ('a', 168.0), ('q', 104.0), ('p', 135.0), ('a', 126.0), ('q', 110.0),
         ('p', 288.0), ('r', 40.0), ('a', 51.0), ('q', 285.0), ('p', 162.0), ('a', 141.0), ('q', 72.0), ('p', 252.0),
         ('a', 186.0), ('r', 46.0), ('p', 291.0), ('q', 120.0), ('a', 132.0), ('p', 444.0), ('q', 375.0), ('r', 404.0),
         ('a', 459.0), ('p', 450.0), ('r', 440.0, 0.7)]
CUTS = [(round(BEATS[i] - SONG_IN, 2), k, t, *sp) for i, (k, t, *sp) in enumerate(SHOTS)]
END = round(BEATS[len(SHOTS) + 3] - SONG_IN, 2)                                       # last shot holds 4 beats
WORDS = [(0.0, 'VEGAS WEEK.', 230, 1.8), (CUTS[8][0], 'PRACTICE|THURSDAY NIGHT', 230, 2.7),
         (CUTS[16][0], 'QUALIFYING|FRIDAY NIGHT', 230, 2.7), (CUTS[24][0], 'LIGHTS OUT|SATURDAY NIGHT', 220, END - CUTS[24][0])]
CFG = dict(name='vegas_week_hype', files=FILES, cuts=CUTS, end=END, words=WORDS, flash=[CUTS[8][0], CUTS[16][0], CUTS[24][0]],
           font='anton', grade=False, song=os.path.join(ASSETS, 'songs', 'trend', 'bow_bow_bow_zeddy_will.mp3'), song_in=SONG_IN,
           title='VEGAS WEEK|PRACTICE STARTS TONIGHT', banner_in=0.6)

if __name__ == '__main__':
    fps = int(os.environ.get('DEX_FPS', 25))
    out, total = lyric.render(dict(CFG, fps=fps), S, os.path.join(S, 'out', f'cn_vegas_week_hype_{fps}.mp4'))
    print(out, f'total {total:.1f}s', flush=True)
