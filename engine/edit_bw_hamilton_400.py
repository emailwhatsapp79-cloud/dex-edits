"""BW - F1: LEWIS HAMILTON, RACE 400 - master edit (story + hype, Desmond Nov 12: "another master edit").
  A  Lewis, one continuous take (F1 Short Z17VXMBiFuk, interview half cropped - their subtitles cut out, ours added):
     "I definitely didn't anticipate I'd ever get to 400... no one's won after 300 Grands Prix. I proved that wrong.
     So... I'll have to do that after 400." Cold open: Lewis cut out, 400 behind him, 3D camera push (depth).
  B  drop: his lap-1 onboard (F1 Short rdypaolu6cM, zoomed half), every hit its own move, counter P20 -> P10, AI slow
     motion (RIFE) on the long shot.
  C  the commentator, in full: "Lewis Hamilton to the inside on camera. How can Hamilton be there? He's up 11 places. He
     cannot be up 11 places, but he is." - counter lands on P9.
  D  black-and-white Lewis, 3D push, RACE 400.
Song: Destroy It All / YUJI (slowed, full track), drop at 55.9 s on the end of A. No grade (Desmond's Nov 12 test).
Usage: SRC=<sources folder> SCRATCH=<dir> python3 edit_bw_hamilton_400.py"""
import os, sys, glob
sys.path.insert(0, os.path.dirname(__file__))
import master

S = os.environ.get('SCRATCH', '/tmp')
SRC = os.environ['SRC']
ASSETS = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'dex-edits-assets')
src = lambda vid: glob.glob(os.path.join(SRC, '**', f'*{vid}*.mp4'), recursive=True)[0]
FILES = {'z': (src('Z17VXMBiFuk'), 'crop=940:940:70:0,scale=1080:1080:flags=lanczos'),
         'y': (src('rdypaolu6cM'), 'crop=1080:1080:0:720'),
         'r': (src('lkb5kqDJYXk'), 'crop=1080:1080:420:0')}
A_WORDS = [(0.0, "I DEFINITELY DIDN'T"), (0.96, 'ANTICIPATE'), (1.54, "I'D EVER GET TO 400."), (2.88, 'I NEVER, EVER'),
           (3.58, 'THOUGHT ABOUT THAT.'), (5.28, 'I DO REMEMBER'), (6.24, 'I WAS APPROACHING 300'), (8.68, 'AND THE NARRATIVE'),
           (9.96, 'THAT EVERYONE SAID'), (10.86, "THAT NO ONE'S WON"), (11.64, 'AFTER 300 GRANDS PRIX,'), (13.54, 'I PROVED THAT WRONG.'),
           (14.52, 'SO...'), (15.04, "I'LL HAVE TO DO THAT"), (16.72, 'AFTER 400.')]
C_WORDS = [(44.57, 'LEWIS HAMILTON'), (45.4, 'TO THE INSIDE ON CAMERA.'), (46.53, 'HOW CAN HAMILTON BE THERE?'),
           (47.75, "HE'S UP 11 PLACES."), (49.03, 'HE CANNOT BE UP 11 PLACES,'), (50.75, 'BUT HE IS.')]
B_CUTS = [55.9, 56.59, 57.48, 58.15, 59.2, 59.87, 60.4, 60.91, 63.0, 63.65, 64.4, 65.39]
FXS = ['flash', 'whip_l', 'punch', 'zoom', 'whip_r', 'glitch', 'spin', 'shake', 'whip_u', 'punch', 'zoom', 'glitch']
B_SHOTS = [dict(k='y', t=t, fx=FXS[i], count=c, **({'slow': 0.5} if i == 7 else {}))
           for i, (t, c) in enumerate(zip([6.5, 8.0, 9.5, 11.0, 12.5, 14.0, 15.2, 16.0, 18.0, 19.5, 21.0, 22.5],
                                          [20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 10]))]
B_SHOTS[0]['stamp'] = 'RACE 400.'
CFG = dict(name='hamilton_400', files=FILES, song=os.path.join(ASSETS, 'songs', 'full', '19_destroy_it_all_yuji_slowed.mp3'),
           song_in=55.9 - 17.45, title='LEWIS HAMILTON|RACE 400', banner_in=3.0,
           segments=[dict(type='voice', k='z', a=0.0, b=17.45, words=A_WORDS, hero=dict(at=0.6, text='400', dur=2.6)),
                     dict(type='beats', cuts=B_CUTS, end=65.93, shots=B_SHOTS),
                     dict(type='voice', k='r', a=44.55, b=51.6, words=C_WORDS, count=10, count_to=(51.0, 9)),
                     dict(type='end', k='z', at=12.0, text='RACE 400.', dur=4.0)])

if __name__ == '__main__':
    fps = int(os.environ.get('DEX_FPS', 50))
    out, total = master.render(dict(CFG, fps=fps), S, os.path.join(S, 'out', f'bw_hamilton_400_{fps}.mp4'))
    print(out, f'total {total:.1f}s', flush=True)
