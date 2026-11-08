"""BL - F1: HAMILTON STARTS LAST IN HIS 400th RACE (Sao Paulo GP race day, Nov 8 2026, posted 18:00 Lagos = lights out).
Line -> drop on #163 "Look at me now" (trending, clean): Friday's radio "I've got smoke in the cockpit. / Box, box, box. /
That power unit is not healthy." over the Ferrari in the pits -> drop "FROM LAST." (new power unit = back of the grid) ->
his face, out in Q2 in the rain -> outro, song dipped: "I definitely didn't anticipate I'd ever get to 400."
F1's own red radio captions (smoke clip 0-2.6 s) are avoided: the voice plays over later, clean pit shots.
Footage: formula1.com official (FP3 smoke clip, Sao Paulo preview interview, qualifying highlights). DEX_FPS=50 for YouTube."""
import os, sys, glob
sys.path.insert(0, os.path.dirname(__file__))
import linedrop

S = os.environ.get('SCRATCH', '/tmp')
B = os.path.join(S, 'bra')
SONGS = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'dex-edits-assets', 'songs')
CFG = dict(name='hamlast', song=glob.glob(os.path.join(SONGS, '163_*.mp3'))[0], drop=15.0, beat=60 / 108, shake=True,
    size=(1280, 720), cap=(46, 0.6),
    files={'sm': os.path.join(B, 'smoke.mp4'), 'ham': os.path.join(B, 'hamint.mp4'), 'q': os.path.join(B, 'quali.mp4')},
    talk=[('sm', 1.10, 2.05, 0, 'sm', 3.55), ('sm', 2.40, 3.12, 0, 'sm', 6.10), ('sm', 3.80, 5.90, 0, 'sm', 6.85)],
    words=[('sm', 1.16, '|I\'VE GOT SMOKE'), ('sm', 1.60, 'IN THE COCKPIT.'), ('sm', 2.42, '|BOX, BOX, BOX.'),
           ('sm', 3.82, '|THAT POWER UNIT'), ('sm', 4.58, 'IS NOT HEALTHY.')],
    big=('FROM LAST.', 2),
    after=[(2, 'ham', 101.60, 106.00), (2, 'q', 235.40, 237.72), (2, 'q', 21.20, 23.80), (2, 'ham', 118.30, 125.00)],
    outro=('ham', 84.66, 87.40, [('ham', 84.68, '|I DEFINITELY DIDN\'T ANTICIPATE'), ('ham', 86.12, '|I\'D EVER GET TO'),
                                 ('ham', 86.86, '400.')]))

if __name__ == '__main__':
    fps = int(os.environ.get('DEX_FPS', 30))
    out, drop, end = linedrop.render(dict(CFG, fps=fps), S, os.path.join(S, 'out', f'bl_hamlast_{fps}.mp4'))
    print(out, f'drop {drop:.2f} end {end:.2f}')
