"""BN - F1: VERSTAPPEN, FROM THE BACK TO THE PODIUM - UP 19 PLACES (Sao Paulo GP, Nov 8 2026). Line -> drop on #11 Funk Mada
(Max's sound from 'capitalize'). Frame 1 = the move: "Is there a gap? There is a gap, and he's through." -> "Max Verstappen
with a superlative drive (onboard) / once again, from the back to the podium" -> drop "UP 19 PLACES." -> his passes on every
beat -> the podium. Footage: formula1.com official race highlights."""
import os, sys, glob
sys.path.insert(0, os.path.dirname(__file__))
import linedrop

S = os.environ.get('SCRATCH', '/tmp')
SONGS = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'dex-edits-assets', 'songs')
CFG = dict(name='maxup19', song=glob.glob(os.path.join(SONGS, '11_*.mp3'))[0], drop=13.0, beat=0.7895, shake=True,
    size=(1280, 720), cap=(46, 0.6), files={'r': os.path.join(S, 'bra', 'race.mp4'), 'mi': os.path.join(S, 'bra', 'maxint.mp4')},
    talk=[('r', 273.85, 275.95, 0), ('r', 432.45, 435.85, 0, 'r', 144.0), ('r', 435.85, 438.70, 0, 'r', 290.0)],
    words=[('r', 273.88, '|IS THERE A GAP?'), ('r', 274.48, '|THERE IS A GAP,'), ('r', 275.28, "|AND HE'S THROUGH."),
           ('r', 432.50, '|MAX VERSTAPPEN'), ('r', 433.78, '|WITH A SUPERLATIVE DRIVE.'), ('r', 435.92, '|ONCE AGAIN,'),
           ('r', 436.98, '|FROM THE BACK'), ('r', 437.88, 'TO THE PODIUM.')],
    big=('UP 19 PLACES.', 2),
    after=[(1, 'r', 302.50, 305.68), (1, 'r', 149.00, 164.00), (1, 'r', 105.00, 108.08), (1, 'r', 75.50, 80.66),
           (1, 'r', 279.00, 288.98), (3, 'r', 461.00, 463.62)], fade=1.0,
    outro=('mi', 6.55, 15.10, [('mi', 6.62, '|CRAZY RACE, I GUESS.'), ('mi', 8.10, '|STARTING P21'), ('mi', 9.38, '|AND FINISHING SECOND,'),
                               ('mi', 10.56, '|SO OF COURSE, FROM THAT SIDE,'), ('mi', 12.84, '|VERY HAPPY'), ('mi', 13.72, '|TO BE ON THE PODIUM HERE.')],
           [('r', 156.00, 1.2), ('mi', 7.75, 99)]))

if __name__ == '__main__':
    fps = int(os.environ.get('DEX_FPS', 30))
    out, drop, end = linedrop.render(dict(CFG, fps=fps), S, os.path.join(S, 'out', f'bn_maxup19_{fps}.mp4'))
    print(out, f'drop {drop:.2f} end {end:.2f}')
