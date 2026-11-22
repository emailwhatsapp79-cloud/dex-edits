"""DH - F1 LAS VEGAS 2026: NORRIS GOES PAST BOTH OF THEM (Tue 24 Nov 08:00). Russell attacks Max around the outside
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
W1 = [(311.05, "HERE'S THE CHANCE"), (311.79, 'GEORGE RUSSELL'), (312.53, 'AROUND THE OUTSIDE'), (313.91, 'VERSTAPPEN'),
      (314.37, 'DESPERATE TO HANG ONTO IT'), (315.61, 'LAID ON THE BRAKES'), (317.77, 'NORRIS'),
      (318.19, 'TRYING TO GO PAST BOTH OF THEM'), (321.61, 'BUT NORRIS IS THROUGH'), (322.81, 'TO SECOND POSITION.')]
W2 = [(326.29, 'RUSSELL WAS LOOKING AT P1.'), (328.19, 'HE FINDS HIMSELF IN P3.')]
CFG = dict(name='norris_three_wide_vegas26', files=FILES, song=os.path.join(ASSETS, 'songs', 'trend', 'housewife_tate_mcrae.mp3'),
           song_in=30.0, title='NORRIS GOES PAST|BOTH OF THEM', banner_in=0.2,
           segments=[dict(type='voice', k='v', a=310.95, b=323.7, words=W1),
                     dict(type='voice', k='v', a=326.2, b=329.7, words=W2),
                     dict(type='outro', shots=[('v', 320.5), ('v', 313.0), ('v', 324.0), ('v', 302.0), ('v', 319.0, 0.6)])])

if __name__ == '__main__':
    fps = int(os.environ.get('DEX_FPS', 25))
    out, total = master.render(dict(CFG, fps=fps), S, os.path.join(S, 'out', f'dh_norris_three_wide_vegas26_{fps}.mp4'))
    print(out, f'total {total:.1f}s', flush=True)
    import look; look.yt1440(out, out.replace('.mp4', '_yt1440.mp4'))
