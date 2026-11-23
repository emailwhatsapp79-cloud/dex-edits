"""DQ - MOTOGP VALENCIA PREVIEW (Wed 25 Nov 08:00): last year's finale - Bez wins start to finish and the commentator calls it: 'Aprilia, Bezzecchi and a fully fit Martin - watch out, title contenders in 2026'. Source: MotoGP 'Best MotoGP Moments | 2025 Valencia GP' (_MNlGAK69AE).
NOV 17 rules: 15-20 s, short commentary runs, beat outro + card."""
import os, sys, glob
sys.path.insert(0, os.path.dirname(__file__))
import master

S = os.environ.get('SCRATCH', '/tmp')
SRC = os.environ['SRC']
ASSETS = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'dex-edits-assets')
src = lambda vid: glob.glob(os.path.join(SRC, '**', f'*{vid}*.mp4'), recursive=True)[0]
FILES = {'m': (src('_MNlGAK69AE'), 'crop=1080:1080:470:0')}
NAME = 'dq_valencia25_bez_prophecy.py'.replace('.py', '')
CFG = dict(name=NAME, files=FILES, song=os.path.join(ASSETS, 'songs', 'full', '05_montagem_kali_slowed.mp3'), song_in=13.0, title="VALENCIA LAST YEAR|'WATCH OUT IN 2026'", banner_in=0.2,
           segments=[dict(type='voice', k='m', a=203.3, b=210.3, words=[(203.35, 'IT FINISHES'), (204.07, 'WITH THE ICING ON THE CAKE'), (206.53, 'AS BEZ WINS'), (207.87, 'THE FINAL GRAND PRIX'), (209.17, 'OF THE SEASON.')]),
                     dict(type='voice', k='m', a=218.05, b=227.65, pic=('m', 212.5), words=[(218.11, 'BACK-TO-BACK'), (219.01, 'START TO FINISH VICTORIES.'), (220.57, 'APRILIA, BEZZECCHI'), (222.31, 'AND A FULLY FIT JORGE MARTIN.'), (224.29, 'WATCH OUT.'), (225.21, "THEY'RE GONNA BE"), (225.81, 'TITLE CONTENDERS IN 2026.')]),
                     dict(type='outro', shots=[('m', 196.0), ('m', 209.0), ('m', 198.5), ('m', 207.5), ('m', 214.0, 0.6)])])

if __name__ == '__main__':
    fps = int(os.environ.get('DEX_FPS', 25))
    out, total = master.render(dict(CFG, fps=fps), S, os.path.join(S, 'out', f'{NAME}_{fps}.mp4'))
    print(out, f'total {total:.1f}s', flush=True)
    import look; look.yt1440(out, out.replace('.mp4', '_yt1440.mp4'))
