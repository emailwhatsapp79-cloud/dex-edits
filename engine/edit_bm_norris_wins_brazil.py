"""BM - F1: NORRIS WINS IN BRAZIL, back to back (Sao Paulo GP, Nov 8 2026). Line -> drop on #162 Funk Loading - the same
trending sound as his pole edit the day before (pole -> win, one story). Ref Y1: the call, then the drop.
  commentary "And Lando Norris will go back to back in Brazil (over his McLaren in the spray) / in the wet, in the dry. He's"
  (over him crossing the line) -> drop "P1." -> the McLaren crew hugging, onboard, the podium. F1's own orange radio captions
  (finish clip > 10.5 s) are never on screen. Footage: formula1.com official (race highlights + "Norris crosses the line")."""
import os, sys, glob
sys.path.insert(0, os.path.dirname(__file__))
import linedrop

S = os.environ.get('SCRATCH', '/tmp')
B = os.path.join(S, 'bra')
SONGS = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'dex-edits-assets', 'songs')
CFG = dict(name='norriswin', song=glob.glob(os.path.join(SONGS, '162_*.mp3'))[0], drop=8.0, beat=60 / 123, shake=True,
    size=(1280, 720), cap=(46, 0.6),
    files={'fin': os.path.join(B, 'finish.mp4'), 'r': os.path.join(B, 'race.mp4'), 'ni': os.path.join(B, 'norint.mp4')},
    talk=[('fin', 0.00, 3.45, 0, 'r', 427.70), ('fin', 3.45, 6.20, 0, 'fin', 1.60)],
    words=[('fin', 0.02, '|LANDO NORRIS'), ('fin', 1.36, '|WILL GO BACK TO BACK'), ('fin', 2.92, 'IN BRAZIL.'),
           ('fin', 4.42, '|IN THE WET,'), ('fin', 5.28, 'IN THE DRY.'), ('fin', 6.20, "|HE'S")],
    big=('P1.', 2), big_size=0.2,
    after=[(2, 'r', 2.00, 6.84), (2, 'r', 18.00, 22.24), (2, 'r', 228.60, 230.04), (2, 'r', 149.00, 164.00),
           (2, 'r', 438.10, 442.96), (2, 'r', 410.00, 413.36), (2, 'fin', 4.45, 6.40), (2, 'fin', 6.50, 10.45),
           (2, 'fin', 8.40, 10.45), (2, 'r', 461.05, 463.62)],
    # v2 (Desmond: "missing passion... where's the celebration... why remove the Red Bull footage"): the whole race on the
    # beat - start, Lawson's lap-1 move, Kimi spinning out of the lead, Max's charge, Hadjar's Red Bull - then Lando
    # crossing the line, the crew going crazy, the podium, and his own words to close.
    outro=('ni', 49.82, 51.58, [('ni', 49.86, '|PROBABLY ONE OF THE BEST WINS'), ('ni', 50.98, "|I'VE HAD.")]))

if __name__ == '__main__':
    fps = int(os.environ.get('DEX_FPS', 30))
    out, drop, end = linedrop.render(dict(CFG, fps=fps), S, os.path.join(S, 'out', f'bm_norriswin_{fps}.mp4'))
    print(out, f'drop {drop:.2f} end {end:.2f}')
