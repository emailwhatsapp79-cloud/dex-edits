"""DN - QATAR WEEK HYPE (Thu 26 Nov 08:00): last year at Lusail - three title contenders, 'if Lando wins tonight he's champion of the world', the lights and the run to turn 1.
Source: F1 official highlights (BeaVJggQ2dc). NOV 17 rules: 15-20 s, short commentary runs, beat outro + card."""
import os, sys, glob
sys.path.insert(0, os.path.dirname(__file__))
import master

S = os.environ.get('SCRATCH', '/tmp')
SRC = os.environ['SRC']
ASSETS = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'dex-edits-assets')
src = lambda vid: glob.glob(os.path.join(SRC, '**', f'*{vid}*.mp4'), recursive=True)[0]
FILES = {'v': (src('BeaVJggQ2dc'), 'crop=1080:1080:420:0')}
NAME = 'dn_qatar25_start_hype.py'.replace('.py', '')
CFG = dict(name=NAME, files=FILES, song=os.path.join(ASSETS, 'songs', 'trend', 'can_i_ride_sidepiece.mp3'), song_in=40.0, title="QATAR IS BACK THIS WEEKEND|LAST YEAR: 3 TITLE CONTENDERS", banner_in=0.2,
           segments=[dict(type='voice', k='v', a=0.25, b=9.95, words=[(0.30, 'THREE CONTENDERS FOR THE TITLE'), (2.46, 'AND AN EPIC RUN TO TURN ONE.'), (4.38, 'IF LANDO WINS TONIGHT'), (6.10, "HE'S CHAMPION OF THE WORLD."), (8.06, 'HERE COME THE LIGHTS IN QATAR.')]),
                     dict(type='voice', k='v', a=11.3, b=16.95, words=[(11.36, "WE'RE UNDERWAY"), (12.32, 'AND RACING TO TURN ONE.')]),
                     dict(type='outro', shots=[('v', 13.0), ('v', 18.0), ('v', 21.0), ('v', 26.0), ('v', 30.0, 0.6)])])

if __name__ == '__main__':
    fps = int(os.environ.get('DEX_FPS', 25))
    out, total = master.render(dict(CFG, fps=fps), S, os.path.join(S, 'out', f'{NAME}_{fps}.mp4'))
    print(out, f'total {total:.1f}s', flush=True)
    import look; look.yt1440(out, out.replace('.mp4', '_yt1440.mp4'))
