"""DU - F1 QATAR 2026 FP2 (F1 channel, Sat 28 Nov 12:00): Ferrari's Friday - Leclerc 360s through the gravel (red flag), Hamilton goes off and rides a scooter back. Source: F1 'FP2 Highlights | 2026 Qatar GP' (ZZ4ZgM25j1g).
NOV 17 rules: 15-20 s, short commentary runs (Content ID: each run < 8 s), beat outro + card."""
import os, sys, glob
sys.path.insert(0, os.path.dirname(__file__))
import master

S = os.environ.get('SCRATCH', '/tmp')
SRC = os.environ['SRC']
ASSETS = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'dex-edits-assets')
src = lambda vid: glob.glob(os.path.join(SRC, '**', f'*{vid}*.mp4'), recursive=True)[0]
FILES = {'q': (src('ZZ4ZgM25j1g'), 'crop=1080:1080:420:0')}
NAME = 'du_ferrari_friday_qatar.py'.replace('.py', '')
CFG = dict(name=NAME, files=FILES, song=os.path.join(ASSETS, 'songs', 'trend', 'housewife_tate_mcrae.mp3'), song_in=30.0, title="FERRARI'S FRIDAY IN QATAR|360 IN THE GRAVEL, THEN A SCOOTER", banner_in=0.2,
           segments=[dict(type='voice', k='q', a=156.3, b=161.8, words=[(156.37, 'I COULD HAVE BANKED ON HIM'), (157.87, 'FINDING SOME GRAVEL,'), (158.93, 'I WAS NOT EXPECTING HIM'), (160.05, 'TO 360 HIS WAY THROUGH IT.')]),
                     dict(type='voice', k='q', a=162.25, b=166.2, words=[(162.29, 'HIS ROTATION SCATTERED STONES'), (163.93, 'ACROSS THE TRACK,'), (165.09, 'WHICH CAUSED A RED FLAG.')]),
                     dict(type='voice', k='q', a=138.3, b=145.3, words=[(138.35, "IT DIDN'T END WELL FOR LEWIS."), (139.53, 'HE WENT OFF IN THE FINAL MINUTES'), (141.27, 'AND ABANDONED HIS SF26,'), (143.53, 'TAKING THE SCOOTER BACK TO THE PADDOCK.')]),
                     dict(type='outro', shots=[('q', 157.5), ('q', 148.0), ('q', 160.5), ('q', 143.5), ('q', 164.0, 0.6)])])

if __name__ == '__main__':
    fps = int(os.environ.get('DEX_FPS', 25))
    out, total = master.render(dict(CFG, fps=fps), S, os.path.join(S, 'out', f'{NAME}_{fps}.mp4'))
    print(out, f'total {total:.1f}s', flush=True)
    import look; look.yt1440(out, out.replace('.mp4', '_yt1440.mp4'))
