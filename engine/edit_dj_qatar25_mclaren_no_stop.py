"""DJ - QATAR 2025 FLASHBACK (Tue 24 Nov 18:00): safety car, almost the whole field pits, McLaren keep both cars out, Max wins and takes the title fight to Abu Dhabi. 'whose fault? 👇'
Source: F1 official highlights (BeaVJggQ2dc). NOV 17 rules: 15-20 s, short commentary runs, beat outro + card."""
import os, sys, glob
sys.path.insert(0, os.path.dirname(__file__))
import master

S = os.environ.get('SCRATCH', '/tmp')
SRC = os.environ['SRC']
ASSETS = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'dex-edits-assets')
src = lambda vid: glob.glob(os.path.join(SRC, '**', f'*{vid}*.mp4'), recursive=True)[0]
FILES = {'v': (src('BeaVJggQ2dc'), 'crop=1080:1080:420:0')}
NAME = 'dj_qatar25_mclaren_no_stop.py'.replace('.py', '')
CFG = dict(name=NAME, files=FILES, song=os.path.join(ASSETS, 'songs', 'full', '13_funk_unico_super_slowed.mp3'), song_in=42.95, title="QATAR 2025|McLAREN DIDN'T PIT. MAX WON.", banner_in=0.2,
           segments=[dict(type='voice', k='v', a=177.55, b=182.45, pic=('v', 171.5), words=[(177.63, "McLAREN'S WHO REMAIN"), (178.99, 'ON THE RACETRACK.'), (179.57, 'A WHOLE BUNCH OF CARS'), (180.59, 'COMING IN,'), (181.29, 'IN FACT MOST OF THE FIELD.')]),
                     dict(type='voice', k='v', a=198.0, b=201.8, words=[(198.05, 'THEY HAVE LOST'), (199.21, 'ALL THEIR FLEXIBILITY'), (200.37, 'FOR THE REST OF THE RACE.')]),
                     dict(type='voice', k='v', a=426.9, b=434.95, words=[(426.97, 'MAX VERSTAPPEN'), (428.47, 'WILL NOT BE MOVED.'), (430.03, 'HE HEADS TO ABU DHABI'), (431.59, 'WITH A FIGHTING CHANCE'), (433.25, 'STILL TO WIN IT ALL.')]),
                     dict(type='outro', shots=[('v', 173.0), ('v', 200.5), ('v', 176.0), ('v', 203.0), ('v', 428.0, 0.6)])])

if __name__ == '__main__':
    fps = int(os.environ.get('DEX_FPS', 25))
    out, total = master.render(dict(CFG, fps=fps), S, os.path.join(S, 'out', f'{NAME}_{fps}.mp4'))
    print(out, f'total {total:.1f}s', flush=True)
    import look; look.yt1440(out, out.replace('.mp4', '_yt1440.mp4'))
