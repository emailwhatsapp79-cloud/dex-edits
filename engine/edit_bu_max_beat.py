"""BU - F1: MAX VERSTAPPEN, FROM THE BACK - beat edit (ref AE1 @aelclerc). Every cut on a hit of #162 Funk Loading
(123 BPM, drop 8.38 s): helmet walk over the build, then the start, the passes (Hamilton, Piastri, round the outside,
Albon), the spray battles, the pit stop, his face, the podium - "P21 > P2." Zoom punch + shake on every cut, white flash on
the drop and the big hits. Desmond's Nov 12 test: NO grade - the 1080p footage as it is. Square in 1080x1920.
Sources: race highlights lkb5kqDJYXk ('r'), Max's 9-minute video q16mDWoytf0 ('m').
Usage: SRC=<folder with the mp4s> SCRATCH=<dir> python3 edit_bu_max_beat.py"""
import os, sys, glob
sys.path.insert(0, os.path.dirname(__file__))
import beatedit

S = os.environ.get('SCRATCH', '/tmp')
SRC = os.environ['SRC']
ASSETS = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'dex-edits-assets')
src = lambda vid: glob.glob(os.path.join(SRC, f'*{vid}*.mp4'))[0]
# hits of #162 kept at least 0.42 s apart (librosa percussive onsets, strongest 40 %)
CUTS = [8.38, 9.13, 9.61, 10.33, 11.08, 11.56, 12.31, 13.03, 13.51, 14.58, 15.46, 15.95, 16.95, 17.44, 17.93, 18.9, 19.39,
        20.85, 21.57, 22.41, 23.31, 24.75, 25.26, 25.75, 26.61, 27.45]
SHOTS = [('r', 2.4), ('r', 7.5), ('m', 95.0), ('r', 74.1), ('m', 208.6), ('m', 212.0), ('r', 82.1), ('m', 233.2),
         ('m', 236.0), ('r', 89.1), ('r', 103.5), ('r', 105.0), ('r', 84.0), ('m', 250.0), ('m', 275.8), ('m', 289.0),
         ('m', 140.0), ('m', 357.9), ('m', 358.6), ('m', 376.0), ('m', 300.0), ('m', 517.5), ('m', 519.2), ('m', 10.6),
         ('m', 180.7), ('m', 522.6)]
CFG = dict(name='max_beat', files={'r': src('lkb5kqDJYXk'), 'm': src('q16mDWoytf0')}, grade=None, crop=420,
           song=os.path.join(ASSETS, 'songs', '162_funk_loading_slowed.mp3'), song_in=6.0, cuts=CUTS, end=29.6,
           build=('m', 13.3), shots=SHOTS, flash=[0, 8, 14, 17, 25], endcap='P21 > P2.',
           title='MAX VERSTAPPEN|FROM THE BACK')

if __name__ == '__main__':
    fps = int(os.environ.get('DEX_FPS', 50))
    out, total = beatedit.render(dict(CFG, fps=fps), S, os.path.join(S, 'out', f'bu_max_beat_{fps}.mp4'))
    print(out, f'total {total:.1f}s', flush=True)
