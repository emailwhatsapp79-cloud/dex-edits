"""CZ - F1 LAS VEGAS 2026 QUALIFYING (Sat 21 Nov 12:00, fresh). The twist: Antonelli is fastest but has a five-place grid
drop, so Max Verstappen takes his first Vegas pole - and his team radios him "take a P2" because they hadn't clocked it.
NOV 17 rules: ~20 s, cold open on the payoff (Kimi fastest, won't be pole), short commentary runs, beat outro + card.
  1 "Takes the fastest time in qualifying. He's got a five-place grid drop, so it won't be pole."  (Antonelli's car, Toto)
  2 "Max Verstappen, when it all shakes out, has taken pole position for the Las Vegas Grand Prix, his first one at the circuit."
  3 radio: "Yes, P2, Max. P2. Take a P2."
Song: Flashing Lights (Kanye) from 21 s. Source: F1 'Qualifying Highlights | 2026 Las Vegas Grand Prix' (jiBlTDJ-mFw).
Usage: SRC=<sources folder> SCRATCH=<dir> python3 edit_cz_vegas26_quali.py"""
import os, sys, glob
sys.path.insert(0, os.path.dirname(__file__))
import master

S = os.environ.get('SCRATCH', '/tmp')
SRC = os.environ['SRC']
ASSETS = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'dex-edits-assets')
src = lambda vid: glob.glob(os.path.join(SRC, '**', f'*{vid}*.mp4'), recursive=True)[0]
FILES = {'q': (src('jiBlTDJ-mFw'), 'crop=1080:1080:420:0')}
W1 = [(369.84, 'TAKES THE FASTEST TIME'), (371.66, 'IN QUALIFYING.'), (373.28, "HE'S GOT A FIVE-PLACE GRID DROP,"),
      (375.6, "SO IT WON'T BE POLE.")]
W2 = [(385.7, 'MAX VERSTAPPEN,'), (386.72, 'WHEN IT ALL SHAKES OUT,'), (388.5, 'HAS TAKEN POLE POSITION'),
      (389.64, 'FOR THE LAS VEGAS GRAND PRIX,'), (391.36, 'HIS FIRST ONE AT THE CIRCUIT.')]
W3 = [(393.42, 'YES, P2, MAX.'), (394.48, 'P2.'), (395.34, 'TAKE A P2.')]
CFG = dict(name='vegas26_quali', files=FILES, song=os.path.join(ASSETS, 'songs', 'trend', 'flashing_lights_kanye.mp3'),
           song_in=21.0, title='VEGAS QUALIFYING|KIMI FASTEST, MAX ON POLE', banner_in=0.2,
           segments=[dict(type='voice', k='q', a=369.75, b=376.95, words=W1),
                     dict(type='voice', k='q', a=385.65, b=392.6, words=W2),
                     dict(type='voice', k='q', a=393.35, b=396.3, words=W3),
                     dict(type='outro', shots=[('q', 140.0), ('q', 301.0), ('q', 266.0), ('q', 357.0), ('q', 413.0, 0.6)])])

if __name__ == '__main__':
    fps = int(os.environ.get('DEX_FPS', 25))
    out, total = master.render(dict(CFG, fps=fps), S, os.path.join(S, 'out', f'cz_vegas26_quali_{fps}.mp4'))
    print(out, f'total {total:.1f}s', flush=True)
    import look; look.yt1440(out, out.replace('.mp4', '_yt1440.mp4'))
