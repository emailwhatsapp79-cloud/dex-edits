"""DR - MOTOGP VALENCIA FLASHBACK (Fri 27 Nov 08:00): Pecco Bagnaia's 2025 ends four corners into the finale, in the gravel - 'cannot wait to see the back of 2025'. Source: _MNlGAK69AE.
NOV 17 rules: 15-20 s, short commentary runs, beat outro + card."""
import os, sys, glob
sys.path.insert(0, os.path.dirname(__file__))
import master

S = os.environ.get('SCRATCH', '/tmp')
SRC = os.environ['SRC']
ASSETS = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'dex-edits-assets')
src = lambda vid: glob.glob(os.path.join(SRC, '**', f'*{vid}*.mp4'), recursive=True)[0]
FILES = {'m': (src('_MNlGAK69AE'), 'crop=1080:1080:470:0')}
NAME = 'dr_valencia25_pecco_gravel.py'.replace('.py', '')
CFG = dict(name=NAME, files=FILES, song=os.path.join(ASSETS, 'songs', 'trend', 'purple_rain_prince.mp3'), song_in=38.0, title="VALENCIA 2025|PECCO'S YEAR ENDS IN THE GRAVEL", banner_in=0.2,
           segments=[dict(type='voice', k='m', a=67.1, b=76.55, pic=('m', 62.4), words=[(67.21, 'FOUR CORNERS'), (68.81, 'INTO THIS FINAL GRAND PRIX'), (70.79, "AND HE'S IN THE GRAVEL."), (72.25, "HE'S IN THE DUST."), (73.43, "HE'S FRUSTRATED,"), (74.11, "HE'S DEJECTED"), (75.19, 'ONCE AGAIN.')]),
                     dict(type='voice', k='m', a=76.55, b=83.5, words=[(76.65, 'PECCO BAGNAIA'), (77.85, 'CANNOT WAIT'), (78.87, 'TO SEE THE BACK OF 2025.'), (80.39, 'IT HAS BEEN'), (81.29, 'NOTHING SHORT OF A DISASTER.')]),
                     dict(type='outro', shots=[('m', 64.0), ('m', 72.0), ('m', 65.5), ('m', 74.5), ('m', 63.0, 0.6)])])

if __name__ == '__main__':
    fps = int(os.environ.get('DEX_FPS', 25))
    out, total = master.render(dict(CFG, fps=fps), S, os.path.join(S, 'out', f'{NAME}_{fps}.mp4'))
    print(out, f'total {total:.1f}s', flush=True)
    import look; look.yt1440(out, out.replace('.mp4', '_yt1440.mp4'))
