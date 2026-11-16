"""CT - F1: KIMI LOSES THE LEAD (Tue 17 Nov 08:00, replaces Norris Purple Rain). Brazil 2026 through the radio and the
commentary of F1's 'Radio Rewind' (LwU_TNRBjk8): the gap comes down, "Kimi needs some purple sectors", he spins from
the lead, the double yellows on the radio, then Hadjar dives past at turn 1 - and Kimi still fights back to second.
Every run is under ~8 s (F1 Content ID blocks long unbroken commentary, Nov 15 finding).
Song: Housewife (Tate McRae) from 28.5 s so the loud part comes in at "He loses it!". ~28 s, 25 fps, no grade.
Usage: SRC=<sources folder> SCRATCH=<dir> python3 edit_ct_antonelli_loses_lead.py"""
import os, sys, glob
sys.path.insert(0, os.path.dirname(__file__))
import master

S = os.environ.get('SCRATCH', '/tmp')
SRC = os.environ['SRC']
ASSETS = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'dex-edits-assets')
src = lambda vid: glob.glob(os.path.join(SRC, '**', f'*{vid}*.mp4'), recursive=True)[0]
FILES = {'r': (src('LwU_TNRBjk8'), 'crop=1080:1080:420:0')}
W1 = [(457.64, 'WELL, THE GAP HAS COME'), (458.64, 'DOWN DRAMATICALLY.'), (459.34, "THERE'S KIMI ANTONELLI"),
      (460.52, 'STILL WITH THE RACE LEAD.'), (461.54, 'BUT NORRIS HAS THE TYRES UP'), (462.96, 'AND THE GAP HAS COME DOWN.')]
W2 = [(489.56, 'KIMI NEEDS SOME'), (490.28, 'PURPLE SECTORS.')]
W3 = [(498.58, 'HE LOSES IT!'), (499.98, 'KIMI ANTONELLI'), (500.82, 'FROM THE LEAD OF THE GRAND PRIX!')]
W4 = [(503.54, 'YELLOW HERE, YELLOW HERE,'), (504.36, 'DOUBLE YELLOW HERE.')]
W5 = [(523.76, 'AGAIN INTO TURN ONE.'), (525.1, 'ANTONELLI IS DEEP'), (525.84, 'AND ISACK HADJAR IS THROUGH.'),
      (528.02, 'FIGHTING THE CAR.'), (529.22, "BUT HE'S FOUGHT HIS WAY"), (530.16, 'TO SECOND PLACE.')]
CFG = dict(name='antonelli_loses_lead', files=FILES,
           song=os.path.join(ASSETS, 'songs', 'trend', 'housewife_tate_mcrae.mp3'), song_in=28.5,
           title='KIMI ANTONELLI|LOSES THE LEAD', banner_in=0.4,
           segments=[dict(type='voice', k='r', a=457.55, b=464.4, words=W1),
                     dict(type='voice', k='r', a=489.5, b=490.95, words=W2),
                     dict(type='voice', k='r', a=498.5, b=502.4, words=W3),
                     dict(type='voice', k='r', a=503.5, b=505.9, words=W4),
                     dict(type='voice', k='r', a=523.7, b=531.2, words=W5),
                     dict(type='outro', shots=[('r', 210.0), ('r', 255.0), ('r', 615.0), ('r', 630.0), ('r', 990.0),
                                               ('r', 165.0), ('r', 1005.0), ('r', 1008.5, 0.6)])])

if __name__ == '__main__':
    fps = int(os.environ.get('DEX_FPS', 25))
    out, total = master.render(dict(CFG, fps=fps), S, os.path.join(S, 'out', f'ct_antonelli_loses_lead_{fps}.mp4'))
    print(out, f'total {total:.1f}s', flush=True)
    import look; look.yt1440(out, out.replace('.mp4', '_yt1440.mp4'))
