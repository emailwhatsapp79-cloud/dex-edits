"""CO - MotoGP Portimão 2025: Pecco's Sunday heartbreak, and the question for this weekend (Fri 20 Nov 12:00, Portimão
practice day). Moody serif-word edit with the film grade: slow shots on the crests every 4 beats, then the crash, the
onboard replays, the Ducati garage, Pecco walking back and sitting in the box - PORTIMÃO. / PECCO. / HEARTBREAK. (the
world feed's own caption: "another Sunday heartbreak for Pecco") / REDEMPTION? - PORTIMÃO · THIS WEEKEND.
24.5 s, square in 1080x1920, 25 fps. Song: D>E>A>T>H>M>E>T>A>L - Panchiko (Trend 48 worldwide top 15, Nov 13), 117 BPM.
Sources: MotoGP 'Best MotoGP Moments | 2025 Portuguese GP' (EbJMANarkcQ).
Usage: SRC=<sources folder> SCRATCH=<work dir> python3 edit_co_pecco_portimao.py"""
import os, sys, glob
sys.path.insert(0, os.path.dirname(__file__))
import lyric

S = os.environ.get('SCRATCH', '/tmp')
SRC = os.environ['SRC']
ASSETS = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'dex-edits-assets')
src = lambda vid: glob.glob(os.path.join(SRC, '**', f'*{vid}*.mp4'), recursive=True)[0]
FILES = {'b': (src('EbJMANarkcQ'), 'crop=1080:1080:420:0')}
CUTS = [(0.00, 'b', 15.0, 0.6), (2.04, 'b', 108.0, 0.6), (4.08, 'b', 111.0, 0.6), (6.13, 'b', 135.0, 0.6),
        (8.15, 'b', 116.0, 0.6), (10.19, 'b', 123.0, 0.7),
        (11.21, 'b', 126.0), (12.19, 'b', 120.0), (13.16, 'b', 138.0), (14.18, 'b', 141.0), (15.21, 'b', 144.0),
        (16.25, 'b', 129.0), (17.27, 'b', 147.0), (18.29, 'b', 150.0, 0.7), (20.41, 'b', 152.6, 0.4)]
WORDS = [(0.0, 'PORTIMÃO.', 230, 2.0), (8.15, 'PECCO.', 250, 2.0), (18.29, 'HEARTBREAK.', 190, 2.1),
         (20.41, 'REDEMPTION?|PORTIMÃO · THIS WEEKEND', 200, 4.1)]
CFG = dict(name='pecco_portimao', files=FILES, cuts=CUTS, end=24.52, words=WORDS, flash=[6.13], font='serif', grade=True,
           song=os.path.join(ASSETS, 'songs', 'trend', 'deathmetal_panchiko.mp3'), song_in=2.14,
           title='PECCO BAGNAIA|PORTIMÃO REDEMPTION?', banner_in=0.6)

if __name__ == '__main__':
    fps = int(os.environ.get('DEX_FPS', 25))
    out, total = lyric.render(dict(CFG, fps=fps), S, os.path.join(S, 'out', f'co_pecco_portimao_{fps}.mp4'))
    print(out, f'total {total:.1f}s', flush=True)
