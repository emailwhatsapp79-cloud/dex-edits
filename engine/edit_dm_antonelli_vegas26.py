"""DM - F1 LAS VEGAS 2026 (Wed 25 Nov 12:00): the world champion Antonelli is in the fight for the win on the last laps - then he falls away and finishes P4.
Source: F1 official highlights (Vyk_6bNm7lo). NOV 17 rules: 15-20 s, short commentary runs, beat outro + card."""
import os, sys, glob
sys.path.insert(0, os.path.dirname(__file__))
import master

S = os.environ.get('SCRATCH', '/tmp')
SRC = os.environ['SRC']
ASSETS = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'dex-edits-assets')
src = lambda vid: glob.glob(os.path.join(SRC, '**', f'*{vid}*.mp4'), recursive=True)[0]
FILES = {'v': (src('Vyk_6bNm7lo'), 'crop=1080:1080:420:0')}
NAME = 'dm_antonelli_vegas26.py'.replace('.py', '')
CFG = dict(name=NAME, files=FILES, song=os.path.join(ASSETS, 'songs', 'trend', 'flashing_lights_kanye.mp3'), song_in=21.0, title="THE WORLD CHAMPION|FALLS AWAY ON THE LAST LAP", banner_in=0.2,
           segments=[dict(type='voice', k='v', a=367.55, b=372.6, words=[(367.65, 'KIMI ANTONELLI,'), (369.09, 'THE WORLD CHAMPION,'), (370.43, 'AHEAD OF GEORGE RUSSELL.')]),
                     dict(type='voice', k='v', a=429.7, b=432.6, words=[(429.80, 'HAS ANTONELLI'), (430.42, 'GOT AN ISSUE HERE?'), (431.68, "ANTONELLI'S FALLING AWAY.")]),
                     dict(type='voice', k='v', a=438.0, b=440.6, words=[(438.10, 'ANTONELLI WILL NOT'), (439.70, 'CONTEND FOR THE WIN.')]),
                     dict(type='outro', shots=[('v', 369.0), ('v', 431.0), ('v', 371.5), ('v', 433.5), ('v', 439.0, 0.6)])])

if __name__ == '__main__':
    fps = int(os.environ.get('DEX_FPS', 25))
    out, total = master.render(dict(CFG, fps=fps), S, os.path.join(S, 'out', f'{NAME}_{fps}.mp4'))
    print(out, f'total {total:.1f}s', flush=True)
    import look; look.yt1440(out, out.replace('.mp4', '_yt1440.mp4'))
