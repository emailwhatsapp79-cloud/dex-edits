"""Edit AA - FOOTBALL, star of the day: RONALDO, SOFT style. No text, no flashes: only his faces and celebrations,
Real Madrid (white / grey) -> Al Nassr (yellow), smiling at 41, the jump on the biggest hit. Instrumental sound
played twice (songloop 0-10.39 + 0.06-10.4, 1.2 s fade - 20.7 s, it ENDS) (#51, Desmond: "this song can be used, follow the beat"). Official @realmadrid / @alnassr TikTok clips, 1080p vertical."""
import os, sys
import numpy as np
from PIL import Image, ImageFilter
sys.path.insert(0, os.path.dirname(__file__))
import cardedit
from cardedit import ROOT

RMA, RMB = 'realmadrid_7696530374939151638', 'realmadrid_7608867196927773974'
N1, N2, N3 = 'alnassr_7427249589536738568', 'alnassr_7481429251779054864', 'alnassr_7694912506078170386'
sh = lambda t, f, src, mode='real', cx=0.5: dict(t=t, file=f + '.mp4', src=src, cx=cx, mode=mode)
PLAN = [
    sh(0.00, RMA, 11.95, 'slow'),   # the scream, Madrid
    sh(1.16, RMB, 12.5, 'slow'),   # the hug, Madrid
    sh(2.07, N1, 25.8),            # Al Nassr, pointing, smiling
    sh(2.87, N3, 21.3, 'slow'),    # the smile
    sh(3.78, N3, 24.6),
    sh(4.93, N2, 19.85),           # close
    sh(5.59, N2, 26.3, 'slow'),    # the face
    sh(6.29, N3, 12.6),
    sh(7.51, N3, 64.3),            # the 7
    sh(8.34, N3, 16.0),            # GOAL
    sh(9.01, N1, 3.6, 'slow'),     # the jump, biggest hit
    # second pass of the sound (joined on the hit at 10.39 = song 0.06): the goals, then the end
    sh(10.39, RMA, 9.5),           # Roma - in the net
    sh(11.49, RMA, 15.0),          # the knee slide
    sh(12.40, RMB, 10.3),          # Osasuna - the strike
    sh(13.20, RMB, 18.2),          # in the net
    sh(14.11, N3, 49.5),           # Al Nassr
    sh(15.26, N3, 42.5),
    sh(15.92, N2, 14.2),           # Al Nassr attack
    sh(17.84, RMA, 1.0),           # Madrid, Roma
    sh(18.67, N2, 12.5),
    sh(19.34, RMB, 15.0, 'slow'),  # the hug - the end (sound fades out)
]
END = 20.7


def pre_fx(fr, i, t, lt):
    h, w = fr.shape[:2]
    small = Image.fromarray((np.clip(fr, 0, 1) * 255).astype(np.uint8)).resize((w // 8, h // 8), Image.BILINEAR)
    glow = np.asarray(small.filter(ImageFilter.GaussianBlur(6)).resize((w, h), Image.BILINEAR)).astype(np.float32) / 255
    return np.clip(fr + np.clip(glow - 0.62, 0, 1) * 0.4, 0, 1)


CFG = dict(
    name='AA', layout='full', srcdir=os.path.join(ROOT, 'src_cr7'), tmp=os.path.join(ROOT, 'tmp_aa'),
    song=os.path.join(ROOT, 'songs', 'cr7_loop.mp3'), song_offset=0.0,
    out=os.path.join(ROOT, 'out', 'edit_AA_ronaldo_soft.mp4'), end=END, plan=PLAN,
    swing=set(), drop=set(), punch=set(), cut_flash=False, warm=0.005, sat=1.03, grain=0.0, vig=0.3,
    fx={}, pre_fx=pre_fx, text=[],
)

if __name__ == '__main__':
    cardedit.run(CFG, sys.argv)
