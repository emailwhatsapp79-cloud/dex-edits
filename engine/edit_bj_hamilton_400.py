"""BJ - F1: HAMILTON, RACE 400 (Sao Paulo GP, Nov 8 2026 - his 400th Grand Prix, at the track where he won the 2008 title).
Line -> drop (engine/linedrop.py) on #06 Oya-sa funk (the Lindblad "easily" sound, 10k views - reused on purpose):
  cold open: the Mexico start (Hamilton from pole) under his voice "everyone said that no one's won after 300"
  then his face: "I proved that wrong, so I'll have to do that after" -> "400." = the drop
  -> his Ferrari on the beat (onboard, the stop, out of the pits, the start) -> outro, song dipped: "Definitely, especially
  after winning the world championship here in 2008."
Footage: formula1.com official - Hamilton's Sao Paulo preview interview (bra/hamint) + Mexico race highlights (mex/race).
Usage: python3 edit_bj_hamilton_400.py  (DEX_FPS=50 for YouTube)."""
import os, sys, glob
sys.path.insert(0, os.path.dirname(__file__))
import linedrop

S = os.environ.get('SCRATCH', '/tmp')
SONGS = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'dex-edits-assets', 'songs')
CFG = dict(name='hamilton400', song=glob.glob(os.path.join(SONGS, '06_*.mp3'))[0], drop=13.5, beat=0.8333, size=(1280, 720),
    files={'ham': os.path.join(S, 'bra', 'hamint.mp4'), 'race': os.path.join(S, 'mex', 'race.mp4')}, cap=(46, 0.6),
    talk=[('ham', 94.78, 97.05, 0, 'race', 15.10), ('ham', 98.25, 99.95, 0), ('ham', 100.78, 101.54, 0)],
    words=[('ham', 94.80, '|EVERYONE SAID'), ('ham', 95.44, 'NO ONE\'S WON'), ('ham', 96.20, 'AFTER 300.'),
           ('ham', 98.30, '|I PROVED THAT WRONG.'), ('ham', 99.42, '|SO I\'LL'), ('ham', 100.80, 'HAVE TO DO THAT'),
           ('ham', 101.28, 'AFTER')],
    big=('400.', 2), big_size=0.30,
    after=[(2, 'race', 188.30, 193.76), (1, 'race', 112.60, 118.68), (1, 'race', 194.00, 199.14), (1, 'race', 237.00, 240.98),
           (1, 'race', 20.00, 23.88)],
    outro=('ham', 112.55, 117.45, [('ham', 112.62, '|DEFINITELY,'), ('ham', 113.52, '|ESPECIALLY AFTER WINNING'),
                                   ('ham', 114.38, '|THE WORLD CHAMPIONSHIP'), ('ham', 115.14, '|HERE IN 2008.')]))

if __name__ == '__main__':
    fps = int(os.environ.get('DEX_FPS', 30))
    out, drop, end = linedrop.render(dict(CFG, fps=fps), S, os.path.join(S, 'out', f'bj_hamilton400_{fps}.mp4'))
    print(out, f'drop {drop:.2f} end {end:.2f}')
