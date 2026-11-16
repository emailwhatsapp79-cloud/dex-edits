"""CX - F1 x FOOTBALL: NEYMAR IN THE PADDOCK (Thu 19 Nov 08:00, replaces 'Vegas: 3 years, 3 winners'; the planned Toto
celebration short was dropped - same story as the posted 'Mercedes won it all' of Nov 10). Neymar arrives at Interlagos
and works the paddock - a crossover post for football fans. Music edit, 0.8x speed so the 11.7 s clip runs ~15 s,
Anton cards. Song: Funk Unico (Brazilian funk, super slowed) from its loud part.
Source: F1 Short 'Neymar Is Here In Sao Paulo!' (BjACzSJ5uVg), vertical - square crop from y=300 (his face, the F1
caption above our cards).
Usage: SRC=<sources folder> SCRATCH=<dir> python3 edit_cx_neymar_paddock.py"""
import os, sys, glob
sys.path.insert(0, os.path.dirname(__file__))
import lyric

S = os.environ.get('SCRATCH', '/tmp')
SRC = os.environ['SRC']
ASSETS = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'dex-edits-assets')
src = lambda vid: glob.glob(os.path.join(SRC, '**', f'*{vid}*.mp4'), recursive=True)[0]
FILES = {'y': (src('BjACzSJ5uVg'), 'crop=1080:1080:0:300')}
CUTS = [(0.0, 'y', 0.0, 0.8), (3.1, 'y', 2.5, 0.8), (7.25, 'y', 5.8, 0.8)]
END = 14.5
WORDS = [(0.0, 'NEYMAR|HAS ARRIVED', 190, 2.9), (3.1, 'INTERLAGOS|SÃO PAULO GRAND PRIX', 160, 2.6),
         (7.25, 'THE PADDOCK|JUST GOT BIGGER', 160, 2.6), (11.2, 'NEYMAR|x FORMULA 1', 190, 3.3)]
CFG = dict(name='neymar_paddock', files=FILES, cuts=CUTS, end=END, words=WORDS, flash=[3.1, 7.25], font='anton', grade=False,
           song=os.path.join(ASSETS, 'songs', 'full', '13_funk_unico_super_slowed.mp3'), song_in=54.0,
           title='NEYMAR|IN THE F1 PADDOCK', banner_in=0.6)

if __name__ == '__main__':
    fps = int(os.environ.get('DEX_FPS', 25))
    out, total = lyric.render(dict(CFG, fps=fps), S, os.path.join(S, 'out', f'cx_neymar_paddock_{fps}.mp4'))
    print(out, f'total {total:.1f}s', flush=True)
    import look; look.yt1440(out, out.replace('.mp4', '_yt1440.mp4'))
