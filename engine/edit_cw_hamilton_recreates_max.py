"""CW - F1: TWO SPINS, ONE DECADE APART (Wed 18 Nov 12:00, replaces 'Last time at Portimao'). Interlagos in the rain:
Max Verstappen's 2016 moment and Lewis Hamilton's 2026 one at the same place, cut between the two years on the beat -
"SAME TRACK. SAME RAIN. SAME MOMENT. 10 YEARS APART." Music edit (no commentary in the source), Anton cards, ~19 s.
Source: F1 Short 'Hamilton Recreates Verstappen Moment 10 Years Later!' (b57h8iRF4ys) - a vertical split screen:
2026 on top (y 0-955), 2016 below (y 965-1920); each half is cropped square and scaled 1.15x.
Song: Just Keep Watching (F1 cover); cuts snapped to its beats.
Usage: SRC=<sources folder> SCRATCH=<dir> python3 edit_cw_hamilton_recreates_max.py"""
import os, sys, glob
sys.path.insert(0, os.path.dirname(__file__))
import lyric, hype

S = os.environ.get('SCRATCH', '/tmp')
SRC = os.environ['SRC']
ASSETS = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'dex-edits-assets')
src = lambda vid: glob.glob(os.path.join(SRC, '**', f'*{vid}*.mp4'), recursive=True)[0]
SONG = os.path.join(ASSETS, 'songs', 'full', '22_just_keep_watching_f1_cover.mp3')
SONG_IN = 51.5
FILES = {'n': (src('b57h8iRF4ys'), 'crop=940:940:70:0,scale=1080:1080:flags=lanczos'),        # 2026 Hamilton
         'o': (src('b57h8iRF4ys'), 'crop=940:940:70:972,scale=1080:1080:flags=lanczos')}      # 2016 Verstappen
PLAN = [(0.0, 'o', 0.6), (3.0, 'n', 0.6), (6.0, 'o', 8.0, 0.6), (8.5, 'n', 8.0, 0.6), (11.0, 'o', 11.5),
        (12.5, 'n', 12.0), (14.0, 'o', 14.5), (15.5, 'n', 15.0)]
END = 17.0
beats = [b - SONG_IN for b in hype.song_beats(SONG, SONG_IN, 20.0, 1)]
snap = lambda t: t if t == 0 else min([b for b in beats if abs(b - t) < 0.5] or [t], key=lambda b: abs(b - t))   # only nearby beats
CUTS = [(snap(t), k, si, *sp) for t, k, si, *sp in PLAN]
WORDS = [(CUTS[0][0], '2016|MAX VERSTAPPEN · INTERLAGOS', 170, 2.6), (CUTS[1][0], '2026|LEWIS HAMILTON · INTERLAGOS', 170, 2.6),
         (CUTS[2][0], 'SAME TRACK.', 150, 1.6), (CUTS[3][0], 'SAME RAIN.', 150, 1.6), (CUTS[4][0], 'SAME MOMENT.', 150, 1.4),
         (CUTS[6][0], '10 YEARS|APART', 190, 3.0)]
CFG = dict(name='hamilton_recreates_max', files=FILES, cuts=CUTS, end=END, words=WORDS, flash=[CUTS[1][0], CUTS[4][0]],
           font='anton', grade=False, song=SONG, song_in=SONG_IN, title='TWO SPINS|10 YEARS APART', banner_in=0.6)

if __name__ == '__main__':
    fps = int(os.environ.get('DEX_FPS', 25))
    out, total = lyric.render(dict(CFG, fps=fps), S, os.path.join(S, 'out', f'cw_hamilton_recreates_max_{fps}.mp4'))
    print(out, f'total {total:.1f}s', flush=True)
    import look; look.yt1440(out, out.replace('.mp4', '_yt1440.mp4'))
