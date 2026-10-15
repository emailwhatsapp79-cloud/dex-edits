"""Edit Z - CARS, SOFT style (Desmond's 'soft' GT3 RS reference, batch H). No text, no flashes, no shake: one green
911 GT3 with Touring package on a sunny mountain road, 11 shots on the strong beats, warm glow on the highlights.
The sound is a love song ("let me show you how proud I am to be yours ... in my summer ... feel your grace"), the
picture follows it: proud = the headlight, yours (big hit) = the car head-on, summer = the sunlit valley,
grace = the car gliding past, the wing, the profile. Layout 'tall' (3:4, not over-zoomed), 4K footage downscaled.
Song: #48 (from @fonzicaars.edits), played twice (songloop: 0-14.08 + 0.07-11.0, joined on two hits, 1 s fade-out) so the edit runs 25 s and ENDS - Desmond: short edits felt unfinished. Footage: Porsche newsroom 4K footage reels 305321 / 305500 (911 GT3 Touring)."""
import os, sys
import numpy as np
from PIL import Image, ImageFilter
sys.path.insert(0, os.path.dirname(__file__))
import cardedit
from cardedit import ROOT

sh = lambda t, f, src, mode='real', cx=0.5: dict(t=t, file=f'c_{f}.mp4', src=src, cx=cx, mode=mode)
PLAN = [
    sh(0.00, '305321_42', 0.4),           # driving away into the sun
    sh(1.20, '305321_361', 0.3, cx=0.4),  # proud - the headlight
    sh(2.94, '305500_236', 0.2, cx=0.45), # the wheel, low sun
    sh(4.16, '305321_159', 0.5),          # yours - head-on
    sh(5.81, '305321_294', 0.2, cx=0.6),  # summer - the valley
    sh(7.46, '305321_243', 0.5, 'slow', cx=0.15),  # from above
    sh(8.29, '305500_322', 0.2, cx=0.45), # the mirror
    sh(9.53, '305321_126', 0.5),          # grace - gliding past
    sh(10.37, '305321_193', 0.5),         # the wing
    sh(11.29, '305500_222', 2.1),         # the wing in the sun
    sh(12.43, '305321_411', 0.3, cx=0.36),       # the rear, PORSCHE
    # second pass of the sound (joined on the hit at 14.08 = song 0.07): the drive, ending on the car leaving
    sh(14.08, '305500_351', 0.5),                # parked, the rear
    sh(15.21, '305321_226', 0.5, cx=0.3),        # the road from above
    sh(16.95, '305321_277', 0.3),                # the hairpin
    sh(18.17, '305500_121', 2.6),                # close, low sun
    sh(19.82, '305321_394', 1.0, cx=0.45),       # three-quarter rear
    sh(21.47, '305321_445', 0.3),                # inside
    sh(22.30, '305500_365', 0.15, 'slow'),       # GT3 Touring
    sh(23.54, '305321_142', 0.6, 'slow'),        # driving away - the end (sound fades out)
]
END = 25.0


def pre_fx(fr, i, t, lt):
    """Soft look: gentle highlight glow + a touch of warmth, shadows slightly lifted."""
    h, w = fr.shape[:2]
    small = Image.fromarray((np.clip(fr, 0, 1) * 255).astype(np.uint8)).resize((w // 8, h // 8), Image.BILINEAR)
    glow = np.asarray(small.filter(ImageFilter.GaussianBlur(6)).resize((w, h), Image.BILINEAR)).astype(np.float32) / 255
    a = fr + np.clip(glow - 0.6, 0, 1) * 0.45
    a = 0.03 + a * 0.97
    a[..., 0] *= 1.03; a[..., 2] *= 0.97
    return np.clip(a, 0, 1)


CFG = dict(
    name='Z', layout='tall', srcdir=os.path.join(ROOT, 'src_gt3'), tmp=os.path.join(ROOT, 'tmp_z'),
    song=os.path.join(ROOT, 'songs', 'gt3_loop.mp3'), song_offset=0.0,
    out=os.path.join(ROOT, 'out', 'edit_Z_gt3_soft.mp4'), end=END, plan=PLAN,
    swing=set(), drop=set(), punch=set(), cut_flash=False, warm=0.0, sat=1.0, grain=0.0, vig=0.25,
    fx={}, pre_fx=pre_fx, text=[],
)

if __name__ == '__main__':
    cardedit.run(CFG, sys.argv)
