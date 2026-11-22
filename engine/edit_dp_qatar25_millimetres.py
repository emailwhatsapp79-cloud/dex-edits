"""DP - QATAR 2025 FLASHBACK (Fri 27 Nov 12:00): both McLarens dance over the same kerb while chasing the title - 'millimetres between spinning and losing the chance to win the world championship'.
Source: F1 official highlights (BeaVJggQ2dc). NOV 17 rules: 15-20 s, short commentary runs, beat outro + card."""
import os, sys, glob
sys.path.insert(0, os.path.dirname(__file__))
import master

S = os.environ.get('SCRATCH', '/tmp')
SRC = os.environ['SRC']
ASSETS = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'dex-edits-assets')
src = lambda vid: glob.glob(os.path.join(SRC, '**', f'*{vid}*.mp4'), recursive=True)[0]
FILES = {'v': (src('BeaVJggQ2dc'), 'crop=1080:1080:420:0')}
NAME = 'dp_qatar25_millimetres.py'.replace('.py', '')
CFG = dict(name=NAME, files=FILES, song=os.path.join(ASSETS, 'songs', 'trend', 'ramalama_roisin_murphy.mp3'), song_in=113.0, title="QATAR 2025|MILLIMETRES FROM LOSING THE TITLE", banner_in=0.2,
           segments=[dict(type='voice', k='v', a=350.0, b=359.6, words=[(350.08, 'OH MY WORD!'), (351.60, 'THE SECOND McLAREN'), (352.92, 'TO DANCE OVER THAT KERB.'), (355.66, 'MILLIMETRES'), (356.02, 'BETWEEN SPINNING'), (357.38, 'AND LOSING THE CHANCE'), (358.46, 'TO WIN THE WORLD CHAMPIONSHIP.')]),
                     dict(type='outro', shots=[('v', 352.5), ('v', 345.0), ('v', 354.0), ('v', 347.0), ('v', 356.0, 0.6)])])

if __name__ == '__main__':
    fps = int(os.environ.get('DEX_FPS', 25))
    out, total = master.render(dict(CFG, fps=fps), S, os.path.join(S, 'out', f'{NAME}_{fps}.mp4'))
    print(out, f'total {total:.1f}s', flush=True)
    import look; look.yt1440(out, out.replace('.mp4', '_yt1440.mp4'))
