"""DS - F1 VEGAS FALLOUT (Fri 27 Nov 18:00): after the Ferraris collided, Leclerc: 'I was considered to be at fault... I'm not going to argue that... not to blame Lewis, I think he didn't see me'. Hamilton: 'I don't want to get into the stuff with Charles, that's for the team to deal with.' Sources: F1 'Drivers React After The Race | 2026 Las Vegas GP' (GwwlbV_hG7c) + race highlights (Vyk_6bNm7lo).
NOV 17 rules: 15-20 s, short commentary runs, beat outro + card."""
import os, sys, glob
sys.path.insert(0, os.path.dirname(__file__))
import master

S = os.environ.get('SCRATCH', '/tmp')
SRC = os.environ['SRC']
ASSETS = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'dex-edits-assets')
src = lambda vid: glob.glob(os.path.join(SRC, '**', f'*{vid}*.mp4'), recursive=True)[0]
FILES = {'r': (src('GwwlbV_hG7c'), 'crop=1080:1080:420:0'), 'v': (src('Vyk_6bNm7lo'), 'crop=1080:1080:420:0')}
NAME = 'ds_leclerc_hamilton_react.py'.replace('.py', '')
CFG = dict(name=NAME, files=FILES, song=os.path.join(ASSETS, 'songs', 'trend', 'deathmetal_panchiko.mp3'), song_in=2.14, title="LECLERC: 'I WAS AT FAULT'|HAMILTON: 'FOR THE TEAM TO DEAL WITH'", banner_in=0.2,
           segments=[dict(type='voice', k='r', a=370.5, b=376.05, pic=('r', 377.0), words=[(370.57, 'TODAY I WAS CONSIDERED'), (371.69, 'TO BE AT FAULT'), (372.15, 'AND I TOOK A 10-SECOND PENALTY,'), (373.79, "AND I'M NOT GOING TO ARGUE THAT.")]),
                     dict(type='voice', k='r', a=401.7, b=404.25, words=[(401.77, 'NOT TO BLAME LEWIS.'), (403.05, "I THINK HE DIDN'T SEE ME.")]),
                     dict(type='voice', k='r', a=246.65, b=254.5, words=[(246.72, "I DEFINITELY DON'T WANT"), (247.86, 'TO GET INTO THE STUFF'), (248.68, 'WITH CHARLES.'), (249.52, "THAT'S FOR THE TEAM"), (253.56, 'TO DEAL WITH.')]),
                     dict(type='outro', shots=[('r', 380.0), ('v', 352.0), ('r', 383.5), ('v', 356.5), ('r', 386.0, 0.6)])])

if __name__ == '__main__':
    fps = int(os.environ.get('DEX_FPS', 25))
    out, total = master.render(dict(CFG, fps=fps), S, os.path.join(S, 'out', f'{NAME}_{fps}.mp4'))
    print(out, f'total {total:.1f}s', flush=True)
    import look; look.yt1440(out, out.replace('.mp4', '_yt1440.mp4'))
