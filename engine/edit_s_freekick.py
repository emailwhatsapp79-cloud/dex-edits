"""Edit S - FOOTBALL (many players, no single star). Direction: "One wall. One keeper. One shot." The free-kick:
hook = the faces of the takers staring at the ball (tension, slow), the wall, the keeper - then the drop rips the
nets: top-bin free-kicks from different players and teams cut on every hit, celebrations, the trophy. Ends: THE
BEAUTIFUL GAME. Song: library #20 (instrumental) from 4.6 s, so the first hit lands on frame 0 and the drop (9.59)
at 4.99. Footage: official @championsleague TikTok clips (vertical)."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import cardedit
from cardedit import ROOT

OFF = 4.6
FK, WAB, DEB = 'championsleague_7504683533684854038', 'championsleague_7683055908464643360', 'championsleague_7696163578860014881'
sh = lambda t, f, src, mode='real', cx=0.5: dict(t=round(t, 3), file=f + '.mp4', src=src, cx=cx, mode=mode)
s = lambda song_t: song_t - OFF
PLAN = [
    sh(0.0, FK, 0.22, 'hero'),          # the taker's face
    sh(s(5.90), FK, 18.45, 'slow'),     # another taker staring at the ball
    sh(s(7.12), FK, 23.40),             # the keeper behind the wall
    sh(s(8.05), FK, 4.20, 'slow'),      # the stare
    sh(s(9.12), FK, 33.90),             # the run-up and strike
    # DROP
    sh(s(9.59), FK, 44.62, 'slow'),     # TOP BINS - net ripples, keeper flying
    sh(s(10.20), FK, 37.60),            # strike
    sh(s(10.96), FK, 17.40),            # in the net
    sh(s(11.42), FK, 41.90),            # over the wall
    sh(s(12.04), FK, 51.20, 'slow'),            # in the net
    sh(s(13.10), FK, 31.90),            # goal
    sh(s(13.87), FK, 12.45),            # in the net
    sh(s(14.49), FK, 2.90, 'slow'),     # in the net
    sh(s(15.11), FK, 61.00, 'slow'),    # in the net
    sh(s(16.32), DEB, 27.62, 'slow'),   # the strike
    sh(s(16.93), FK, 57.50, 'slow'),          # in the net
    sh(s(17.58), 'laliga_7694755460309683478', 0.50),
    sh(s(18.77), FK, 21.80, 'slow'),    # the stadium, the wall: THE BEAUTIFUL GAME.
]
END = 16.2
I_DROP = 5
TEXT = [
    (0.03, s(5.90) - 0.02, '20 YARDS OUT.'),
    (s(5.90), s(7.12) - 0.02, 'ONE CHANCE.'),
    (s(7.12), s(8.05) - 0.02, 'ONE WALL.'),
    (s(8.05), s(9.12) - 0.02, 'NO PRESSURE.'),
    (s(9.59), s(10.20) - 0.02, 'TOP BINS.'),
    (s(18.77) + 0.15, END, 'THE BEAUTIFUL|GAME.'),
]

def pre_fx(fr, i, t, lt):
    """Hide the source clip's own caption on the first shot (soft blur band)."""
    if i != 0: return fr
    from PIL import Image, ImageFilter
    import numpy as np
    y0, y1 = 1440, 1660
    band = Image.fromarray((np.clip(fr[y0:y1], 0, 1) * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(18))
    fr = fr.copy(); fr[y0:y1] = np.asarray(band).astype(np.float32) / 255
    return fr


CFG = dict(
    name='S', layout='full', srcdir=os.path.join(ROOT, 'src_fb2'), tmp=os.path.join(ROOT, 'tmp_s'),
    song=os.path.join(ROOT, 'songs', 'named', '20_mbappe_malvini_sound.mp3'), song_offset=OFF,
    out=os.path.join(ROOT, 'out', 'edit_S_freekick.mp4'), end=END, plan=PLAN,
    swing=set(), drop={I_DROP, 13}, pre_fx=pre_fx, punch=set(range(I_DROP, len(PLAN) - 1)), warm=0.0, sat=1.1, grain=0.14, vig=0.55,
    fx={0: ('bw',), 1: ('bw',), 3: ('bw',), I_DROP: ('radial',), 8: ('xerox',), 12: ('radial',), 15: ('strobe',)},
    text=TEXT, text_cy=960,
)

if __name__ == '__main__':
    cardedit.run(CFG, sys.argv)
