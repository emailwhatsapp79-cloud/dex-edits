"""DE - MOTOGP: BEZZECCHI WON EVERYTHING AT PORTIMAO, MARC KEPT THE CROWN (Mon 23 Nov 08:00).
Pole + sprint win + Grand Prix win (his first MotoGP treble, Aprilia 1-2 with Martin) - and the title still went to Marc.
NOV 17 rules: ~18 s, short commentary runs, beat outro + card.
  1 "on course for his first ever MotoGP treble. Pole position, sprint win and Grand Prix win beckoning for Bez."
  2 "it's a factory Aprilia one-two once again. It's going to be Marc Marquez who will remain as the king in MotoGP."
Source: MotoGP 'Best MotoGP Moments | 2026 Portuguese GP' (NPiiMVtqaUg). Song: Deathmetal (Panchiko).
Usage: SRC=<sources folder> SCRATCH=<dir> python3 edit_de_bezzecchi_wins_loses_title.py"""
import os, sys, glob
sys.path.insert(0, os.path.dirname(__file__))
import master

S = os.environ.get('SCRATCH', '/tmp')
SRC = os.environ['SRC']
ASSETS = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'dex-edits-assets')
src = lambda vid: glob.glob(os.path.join(SRC, '**', f'*{vid}*.mp4'), recursive=True)[0]
FILES = {'b': (src('NPiiMVtqaUg'), 'crop=1080:1080:470:0')}
W1 = [(159.66, 'ON COURSE FOR HIS FIRST EVER'), (160.92, 'MOTOGP TREBLE.'), (162.38, 'POLE POSITION,'), (162.80, 'SPRINT WIN'),
      (163.48, 'AND GRAND PRIX WIN'), (164.82, 'BECKONING FOR BEZ.')]
W2 = [(186.38, 'A FACTORY APRILIA'), (187.58, 'ONE-TWO ONCE AGAIN,')]
W3 = [(188.88, "BUT IT'S MARC MÁRQUEZ"), (191.02, 'WHO WILL REMAIN'), (192.44, 'THE KING OF MOTOGP.')]
CFG = dict(name='bezzecchi_wins_loses_title', files=FILES, song=os.path.join(ASSETS, 'songs', 'trend', 'deathmetal_panchiko.mp3'),
           song_in=2.14, title='BEZZECCHI WON EVERYTHING|AND STILL LOST THE TITLE', banner_in=0.2,
           segments=[dict(type='voice', k='b', a=159.5, b=165.7, words=W1),
                     dict(type='voice', k='b', a=186.3, b=188.85, words=W2),
                     dict(type='voice', k='b', a=188.85, b=194.1, words=W3, pic=('b', 190.6)),   # Marc onboard, not the wide shot
                     dict(type='outro', shots=[('b', 132.0), ('b', 156.0), ('b', 172.0), ('b', 150.0), ('b', 186.0, 0.6)])])

if __name__ == '__main__':
    fps = int(os.environ.get('DEX_FPS', 25))
    out, total = master.render(dict(CFG, fps=fps), S, os.path.join(S, 'out', f'de_bezzecchi_wins_loses_title_{fps}.mp4'))
    print(out, f'total {total:.1f}s', flush=True)
    import look; look.yt1440(out, out.replace('.mp4', '_yt1440.mp4'))
