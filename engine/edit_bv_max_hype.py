"""BV - F1: MAX VERSTAPPEN, P21 > P2 - the creative hype edit (Desmond, Nov 12: "every beat has animation... blow my mind").
Song #162 Funk Loading (cuts on its hits, as BU). Cold open: Max walks in black-and-white, freezes, is cut out with a glowing
outline and a huge P21 BEHIND him. Drop: white flash + GO. Every cut lands with a different move (whip L/R/up, zoom-through,
RGB punch, spin, glitch slices, shake, flash). A position counter ticks P21 -> P2 and punches on every change. Freeze-frame
cutout on the pass: INSTANT. Speed ramps on the long shots. Black-and-white ending: his face, the podium, P21 > P2.
No grade (Desmond's Nov 12 test: the footage as it is). Square in 1080x1920, branding inside the picture.
Sources: race highlights lkb5kqDJYXk ('r'), Max's 9-minute video q16mDWoytf0 ('m').
Usage: SRC=<folder with the mp4s> SCRATCH=<dir> python3 edit_bv_max_hype.py"""
import os, sys, glob
sys.path.insert(0, os.path.dirname(__file__))
import hype

S = os.environ.get('SCRATCH', '/tmp')
SRC = os.environ['SRC']
ASSETS = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'dex-edits-assets')
src = lambda vid: glob.glob(os.path.join(SRC, f'*{vid}*.mp4'))[0]
CUTS = [8.38, 9.13, 9.61, 10.33, 11.08, 11.56, 12.31, 13.03, 13.51, 14.58, 15.46, 15.95, 16.95, 17.44, 17.93, 18.9, 19.39,
        20.85, 21.57, 22.41, 23.31, 24.75, 25.26, 25.75, 26.61, 27.45]
sh = lambda k, t, count, fx, **kw: dict(k=k, t=t, count=count, fx=fx, **kw)
SHOTS = [sh('r', 2.4, 21, 'flash', stamp='GO.'), sh('r', 7.5, 20, 'whip_l'), sh('m', 95.0, 19, 'punch'),
         sh('r', 82.1, 18, 'zoom'), sh('m', 208.6, 17, 'whip_r'), sh('m', 212.0, 16, 'glitch'), sh('r', 89.1, 15, 'spin'),
         sh('m', 233.2, 14, 'shake'), sh('r', 74.0, 13, 'flash', freeze=True, freeze_at=0.15, freeze_text='INSTANT.'),
         sh('r', 103.5, 12, 'whip_u'), sh('r', 105.0, 11, 'punch'), sh('r', 84.0, 10, 'zoom', ramp=1.6),
         sh('m', 250.0, 9, 'glitch'), sh('m', 275.8, 8, 'whip_l'), sh('m', 289.0, 7, 'spin'), sh('m', 357.9, 6, 'shake'),
         sh('m', 358.6, 5, 'zoom', ramp=1.7), sh('m', 376.0, 4, 'whip_r'), sh('m', 300.0, 4, 'punch'),
         sh('m', 180.7, 3, 'glitch'), sh('m', 140.0, 3, 'spin', ramp=1.6),
         sh('m', 517.5, 2, 'flash', bw=True), sh('m', 519.2, 2, 'whip_u', bw=True), sh('m', 10.6, 2, 'zoom', bw=True),
         sh('m', 522.0, 2, 'punch', bw=True), sh('m', 522.6, 2, 'flash', bw=True, hide_count=True, stamp='P21 > P2.')]
CFG = dict(name='max_hype', files={'r': src('lkb5kqDJYXk'), 'm': src('q16mDWoytf0')}, crop=420,
           song=os.path.join(ASSETS, 'songs', '162_funk_loading_slowed.mp3'), song_in=6.0, cuts=CUTS, end=29.6,
           build=dict(k='m', t=13.3, freeze_at=1.3), shots=SHOTS, intro_text='P21', banner_in=2.6,
           title='MAX VERSTAPPEN|P21 TO THE PODIUM')

if __name__ == '__main__':
    fps = int(os.environ.get('DEX_FPS', 50))
    out, total = hype.render(dict(CFG, fps=fps), S, os.path.join(S, 'out', f'bv_max_hype_{fps}.mp4'))
    print(out, f'total {total:.1f}s', flush=True)
