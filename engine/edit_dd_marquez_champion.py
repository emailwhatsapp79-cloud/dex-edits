"""DD - MOTOGP: MARC MARQUEZ, 2026 WORLD CHAMPION (Sun 22 Nov evening, fresh - he clinched it at Portimao today).
The stake: seven rounds in he was 102 points behind Bezzecchi, and he still took the title.
NOV 17 rules: ~20 s, cold open on the payoff (the champion call as he crosses the line), short commentary runs, beat outro + card.
  1 "because Marc Marquez is your 2026 MotoGP World Champion."          (Marc crossing the line)
  2 "Seven rounds into the season, he was 102 points behind Marco Bezzecchi,"   (picture: his crash + the comeback, YMumj0ReSGE)
  3 "but Marc Marquez is a once in a generation talent."               (Marc in the crowd)
Source: MotoGP 'Best MotoGP Moments | 2026 Portuguese GP' (NPiiMVtqaUg) + 'Marc Marquez is your 2026 MotoGP WORLD CHAMPION' (YMumj0ReSGE).
Song: Let The World Burn (TikTok guitar).
Usage: SRC=<sources folder> SCRATCH=<dir> python3 edit_dd_marquez_champion.py"""
import os, sys, glob
sys.path.insert(0, os.path.dirname(__file__))
import master

S = os.environ.get('SCRATCH', '/tmp')
SRC = os.environ['SRC']
ASSETS = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'dex-edits-assets')
src = lambda vid: glob.glob(os.path.join(SRC, '**', f'*{vid}*.mp4'), recursive=True)[0]
FILES = {'b': (src('NPiiMVtqaUg'), 'crop=1080:1080:420:0'), 'a': (src('YMumj0ReSGE'), 'crop=1080:1080:420:0')}
W1 = [(202.58, 'MARC MÁRQUEZ'), (203.96, 'IS YOUR'), (205.14, '2026 MOTOGP'), (208.04, 'WORLD CHAMPION.')]
W2 = [(219.56, 'SEVEN ROUNDS'), (220.58, 'INTO THE SEASON,'), (222.06, 'HE WAS 102 POINTS'), (223.88, 'BEHIND'),
      (224.54, 'MARCO BEZZECCHI,')]
W3 = [(226.86, 'BUT MARC MÁRQUEZ'), (227.86, 'IS A ONCE'), (228.94, 'IN A GENERATION'), (229.74, 'TALENT.')]
CFG = dict(name='marquez_champion', files=FILES, song=os.path.join(ASSETS, 'songs', 'trend', 'let_the_world_burn_tiktok_guitar.mp3'),
           song_in=0.0, title='MARC MÁRQUEZ|2026 MOTOGP WORLD CHAMPION', banner_in=0.2,
           segments=[dict(type='voice', k='b', a=202.5, b=209.75, words=W1),
                     dict(type='voice', k='b', a=219.45, b=226.6, words=W2, pic=('a', 14.0)),
                     dict(type='voice', k='b', a=226.8, b=230.35, words=W3),
                     dict(type='outro', shots=[('b', 214.0), ('b', 222.0), ('a', 27.0), ('b', 216.5), ('b', 232.0, 0.6)])])

if __name__ == '__main__':
    fps = int(os.environ.get('DEX_FPS', 25))
    out, total = master.render(dict(CFG, fps=fps), S, os.path.join(S, 'out', f'dd_marquez_champion_{fps}.mp4'))
    print(out, f'total {total:.1f}s', flush=True)
    import look; look.yt1440(out, out.replace('.mp4', '_yt1440.mp4'))
