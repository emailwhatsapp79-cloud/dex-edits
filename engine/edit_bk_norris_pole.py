"""BK - F1: NORRIS ON POLE IN THE RAIN (Sao Paulo GP qualifying, Nov 7 2026, rain-delayed). Line -> drop on #162 Funk Loading
(slowed) - the trending funk Desmond sent (a hit every 4 s). Ref Y1/X1: the moment first, the song low under it, the drop on the
payoff, then a cut every 2 beats with a shake on each cut.
  "the rain is falling, but it's not slowing down" (frame 1 = a car in the spray) -> "Right, the chequered flag is out.
  It's Lando Norris on pole position in Sao Paulo" -> drop: "3 IN A ROW." -> the McLaren in the rain, Lando celebrating.
Formats: DEX_VERT=1 -> TikTok FULL SCREEN 9:16 (centre crop 405x720 -> 540x960, 1.33x, no bars, no title - Desmond Nov 7);
default -> 1280x720 for the YouTube band Short (ytshort.py). Footage: formula1.com official qualifying highlights."""
import os, sys, glob
sys.path.insert(0, os.path.dirname(__file__))
import linedrop

S = os.environ.get('SCRATCH', '/tmp')
SONGS = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'dex-edits-assets', 'songs')
VERT = os.environ.get('DEX_VERT') == '1'
CFG = dict(name='norrispole', song=glob.glob(os.path.join(SONGS, '162_*.mp3'))[0], drop=8.0, beat=60 / 123, shake=True,
    files={'q': os.path.join(S, 'bra', 'quali.mp4')},
    talk=[('q', 321.45, 323.62, 0), ('q', 448.70, 453.40, 0)],
    words=[('q', 321.48, '|THE RAIN IS FALLING,'), ('q', 322.32, '|BUT IT\'S NOT'), ('q', 322.92, 'SLOWING DOWN.'),
           ('q', 448.76, '|THE CHEQUERED FLAG'), ('q', 449.72, 'IS OUT.'), ('q', 450.50, '|IT\'S LANDO NORRIS'),
           ('q', 451.52, '|ON POLE'), ('q', 452.62, 'IN SAO PAULO')],
    big=('3 IN A ROW.', 4), big_size=0.13,
    after=[(2, 'q', 209.50, 212.42), (2, 'q', 166.40, 170.36), (2, 'q', 317.00, 320.24), (2, 'q', 310.00, 316.92),
           (2, 'q', 345.80, 348.12), (2, 'q', 171.00, 174.32), (2, 'q', 264.00, 266.84), (2, 'q', 456.00, 459.60)])
if VERT:
    CFG.update(size=(540, 960), crop='crop=405:720:437:0', cap=(40, 0.6), big_size=0.075)
else:
    CFG.update(size=(1280, 720), cap=(46, 0.6))

if __name__ == '__main__':
    fps = int(os.environ.get('DEX_FPS', 30))
    out, drop, end = linedrop.render(dict(CFG, fps=fps), S, os.path.join(S, 'out', f"bk_norris_{'v' if VERT else 'h'}{fps}.mp4"))
    print(out, f'drop {drop:.2f} end {end:.2f}')
