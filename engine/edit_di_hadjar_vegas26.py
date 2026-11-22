"""DI - F1 LAS VEGAS 2026: HADJAR, P2 IN A RED BULL 1-2... THEN THE FRONT WING (Tue 24 Nov 12:00).
into turn 1, Max brakes late - and Lando comes through on both for P2; Russell was looking at P1 and ends up P3.
NOV 17 rules: ~19 s, short commentary runs, beat outro + card.
Source: F1 'Race Highlights | 2026 Las Vegas Grand Prix' (Vyk_6bNm7lo). Song: Housewife (Tate McRae)."""
import os, sys, glob
sys.path.insert(0, os.path.dirname(__file__))
import master

S = os.environ.get('SCRATCH', '/tmp')
SRC = os.environ['SRC']
ASSETS = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'dex-edits-assets')
src = lambda vid: glob.glob(os.path.join(SRC, '**', f'*{vid}*.mp4'), recursive=True)[0]
FILES = {'v': (src('Vyk_6bNm7lo'), 'crop=1080:1080:420:0')}
W1 = [(67.45, "AND AT THE FRONT"), (68.57, "IT'S SIDE BY SIDE"), (69.53, 'BETWEEN THE RED BULLS.'),
      (70.49, "DIDN'T EXPECT TO SAY THAT"), (72.01, 'AT THE START OF THE DAY.')]
W2 = [(262.48, 'BUT HADJAR HAS GOT SPARKS'),
      (264.28, 'COMING FROM THE CAR'), (265.92, 'AND HIS CHANCES OF PODIUM'), (267.54, 'ARE DISAPPEARING.')]
CFG = dict(name='hadjar_vegas26', files=FILES, song=os.path.join(ASSETS, 'songs', 'trend', 'can_i_ride_sidepiece.mp3'),
           song_in=40.0, title='HADJAR P2 IN A RED BULL 1-2|THEN THE SPARKS', banner_in=0.2,
           segments=[dict(type='voice', k='v', a=67.35, b=73.0, words=W1),
                     dict(type='voice', k='v', a=262.4, b=268.7, words=W2),
                     dict(type='outro', shots=[('v', 69.5), ('v', 73.0), ('v', 77.0), ('v', 66.5), ('v', 75.5, 0.6)])])

if __name__ == '__main__':
    fps = int(os.environ.get('DEX_FPS', 25))
    out, total = master.render(dict(CFG, fps=fps), S, os.path.join(S, 'out', f'di_hadjar_vegas26_{fps}.mp4'))
    print(out, f'total {total:.1f}s', flush=True)
    import look; look.yt1440(out, out.replace('.mp4', '_yt1440.mp4'))
