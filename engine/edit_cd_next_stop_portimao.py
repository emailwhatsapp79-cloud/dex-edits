"""CD - NEXT STOP: PORTIMÃO (MotoGP build-up, Mon 16 Nov 12:00; the race is 20-22 Nov). The rollercoaster track: blind
crests and drops, slowed over the top and sped up after, cut every 2 beats on "Can I Ride" (SIDEPIECE, 481.8K TikTok
videos - checked Nov 13), the 2025 crash, the winner's helmet-cam celebration. 31 s, square in 1080x1920, 25 fps,
Anton title cards, no grade. Song from 9.07 s: drop at 15.07 = edit 5.98, break at 29.2 = edit 20.1, back at edit 21.0.
Sources: MotoGP 'Best MotoGP Moments | 2025 Portuguese GP' (EbJMANarkcQ).
Usage: SRC=<sources folder> SCRATCH=<work dir> python3 edit_cd_next_stop_portimao.py"""
import os, sys, glob
sys.path.insert(0, os.path.dirname(__file__))
import lyric

S = os.environ.get('SCRATCH', '/tmp')
SRC = os.environ['SRC']
ASSETS = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'dex-edits-assets')
src = lambda vid: glob.glob(os.path.join(SRC, '**', f'*{vid}*.mp4'), recursive=True)[0]
FILES = {'b': (src('EbJMANarkcQ'), 'crop=1080:1080:420:0')}
CUTS = [  # intro: the crests, slowed
        (0.00, 'b', 15.0, 0.6), (2.00, 'b', 45.0, 0.6), (4.00, 'b', 78.0, 0.6),
        # drop: every 2 beats, speed ramps (fast down the hills, slow on the leans)
        (5.98, 'b', 9.0), (6.93, 'b', 30.0, 0.6), (7.83, 'b', 21.0), (8.74, 'b', 48.0, 1.5), (9.65, 'b', 63.0),
        (10.55, 'b', 18.0), (11.46, 'b', 87.0, 0.6), (12.39, 'b', 99.0), (13.29, 'b', 165.0, 0.7), (14.20, 'b', 171.0),
        (15.10, 'b', 201.0, 0.6), (16.01, 'b', 114.0), (16.94, 'b', 138.0, 0.7), (17.82, 'b', 120.0), (18.75, 'b', 186.0),
        (19.65, 'b', 195.0, 0.6),
        # second drop
        (21.00, 'b', 81.0, 0.7), (21.93, 'b', 66.0), (22.81, 'b', 159.0), (23.74, 'b', 204.0, 0.7), (24.65, 'b', 210.0),
        (25.55, 'b', 213.0, 1.4), (26.46, 'b', 222.0), (27.36, 'b', 243.0, 0.7)]
WORDS = [(4.00, 'NEXT STOP', 150, 1.98), (5.98, 'PORTIMÃO|MOTOGP · NOVEMBER 20-22', 210, 1.9),
         (27.36, 'PORTIMÃO|NOVEMBER 20-22', 190, 3.64)]
CFG = dict(name='next_stop_portimao', files=FILES, cuts=CUTS, end=31.0, words=WORDS, flash=[5.98, 21.0], font='anton',
           grade=False, song=os.path.join(ASSETS, 'songs', 'trend', 'can_i_ride_sidepiece.mp3'), song_in=9.07,
           title='NEXT STOP|PORTIMÃO', banner_in=0.6)

if __name__ == '__main__':
    fps = int(os.environ.get('DEX_FPS', 25))
    out, total = lyric.render(dict(CFG, fps=fps), S, os.path.join(S, 'out', f'cd_next_stop_portimao_{fps}.mp4'))
    print(out, f'total {total:.1f}s', flush=True)
