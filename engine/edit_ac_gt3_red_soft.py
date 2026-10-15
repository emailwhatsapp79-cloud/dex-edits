"""Edit AC - CARS, SOFT style #2: a red 911 GT3 on a sunny race track. No text: close details (front wheel,
headlight, mirror, wing, brakes, the seat) between soft aerials of the car on the circuit, ending slow as it drives
away and the sound fades. Song: #44 (Desmond's purple GT3 RS 'my little baby' reference) played twice (songloop
0-10.81 + 0.88-11.7, joined on two hits, fade) = 21.6 s. Layout 'tall' (3:4). Porsche newsroom 4K footage 305257."""
import os, sys
import numpy as np
from PIL import Image, ImageFilter
sys.path.insert(0, os.path.dirname(__file__))
import cardedit
from cardedit import ROOT

sh = lambda t, f, src, mode='real', cx=0.5: dict(t=t, file=f'c_305257_{f}.mp4', src=src, cx=cx, mode=mode)
PLAN = [
    sh(0.00, 19, 0.5),            # the front wheel
    sh(0.88, 58, 0.5),            # low, on the track
    sh(2.21, 200, 0.5),           # from above
    sh(3.20, 278, 0.5),           # the headlight
    sh(4.07, 252, 1.0),           # the car (biggest hit)
    sh(5.03, 123, 0.5),
    sh(6.02, 213, 0.5),           # from above
    sh(7.84, 265, 1.15),          # the mirror
    sh(9.39, 304, 2.1),
    # second pass of the sound (joined on the hit at 10.81 = song 0.88)
    sh(10.81, 110, 0.5),          # the front
    sh(12.14, 226, 0.5),          # from above
    sh(13.13, 291, 0.2),          # the profile
    sh(14.00, 317, 2.0),          # three-quarter rear
    sh(14.96, 330, 0.3),          # exhausts
    sh(15.95, 291, 2.7),          # the brake
    sh(17.77, 369, 0.6),          # the seat
    sh(19.32, 239, 0.5, 'slow'),  # it drives away - the end
]
END = 21.6


def pre_fx(fr, i, t, lt):
    h, w = fr.shape[:2]
    small = Image.fromarray((np.clip(fr, 0, 1) * 255).astype(np.uint8)).resize((w // 8, h // 8), Image.BILINEAR)
    glow = np.asarray(small.filter(ImageFilter.GaussianBlur(6)).resize((w, h), Image.BILINEAR)).astype(np.float32) / 255
    a = fr + np.clip(glow - 0.6, 0, 1) * 0.45
    a = 0.03 + a * 0.97
    a[..., 0] *= 1.02; a[..., 2] *= 0.98
    return np.clip(a, 0, 1)


CFG = dict(
    name='AC', layout='tall', srcdir=os.path.join(ROOT, 'src_gt3'), tmp=os.path.join(ROOT, 'tmp_ac'),
    song=os.path.join(ROOT, 'songs', 'red_loop.mp3'), song_offset=0.0,
    out=os.path.join(ROOT, 'out', 'edit_AC_gt3_red_soft.mp4'), end=END, plan=PLAN,
    swing=set(), drop=set(), punch=set(), cut_flash=False, warm=0.0, sat=1.0, grain=0.0, vig=0.25,
    fx={}, pre_fx=pre_fx, text=[],
)

if __name__ == '__main__':
    cardedit.run(CFG, sys.argv)
