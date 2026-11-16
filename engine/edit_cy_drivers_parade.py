"""CY - F1: THE MOST CHAOTIC DRIVERS' PARADE (Fri 20 Nov 08:00, replaces the Vegas 2023 turn one). Interlagos 2026: a
driver begging to leave ("I really need to go now, I'm sorry!"), hot rods and a remote-control car on the track, drivers
piled into tiny cars, and "I lived to tell the tale, that's amazing." Fun, light Friday post. The voices stay (song
ducked under them), our captions on every spoken line; nobody is named (the speakers are not identified in the source).
Song: Housewife (Tate McRae) from its loud part. ~28 s, 25 fps, end card.
Source: F1 Short 'A Chaotic Drivers' Parade Is Exactly What We Need' (L2-Z-AH41Rw), vertical - square crop y=300.
Usage: SRC=<sources folder> SCRATCH=<dir> python3 edit_cy_drivers_parade.py"""
import os, sys, glob
sys.path.insert(0, os.path.dirname(__file__))
import master

S = os.environ.get('SCRATCH', '/tmp')
SRC = os.environ['SRC']
ASSETS = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'dex-edits-assets')
src = lambda vid: glob.glob(os.path.join(SRC, '**', f'*{vid}*.mp4'), recursive=True)[0]
FILES = {'p': (src('L2-Z-AH41Rw'), 'crop=1080:1080:0:300')}
CFG = dict(name='drivers_parade', files=FILES, song=os.path.join(ASSETS, 'songs', 'trend', 'housewife_tate_mcrae.mp3'),
           song_in=37.0, title="DRIVERS' PARADE|PURE CHAOS", banner_in=0.4,
           segments=[dict(type='voice', k='p', a=0.0, b=8.2, words=[(4.7, 'I REALLY NEED TO GO NOW,'), (6.36, "I'M SORRY!")]),
                     dict(type='voice', k='p', a=9.0, b=14.5),
                     dict(type='voice', k='p', a=14.6, b=16.0),   # the RC car - the empty grass after it is cut
                     dict(type='voice', k='p', a=21.5, b=28.7, words=[(26.5, 'I LIVED TO TELL THE TALE,'), (27.66, "THAT'S AMAZING.")]),
                     dict(type='outro', shots=[])])

if __name__ == '__main__':
    fps = int(os.environ.get('DEX_FPS', 25))
    out, total = master.render(dict(CFG, fps=fps), S, os.path.join(S, 'out', f'cy_drivers_parade_{fps}.mp4'))
    print(out, f'total {total:.1f}s', flush=True)
    import look; look.yt1440(out, out.replace('.mp4', '_yt1440.mp4'))
