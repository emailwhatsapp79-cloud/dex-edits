"""Edit O - NATURE, cut like a car edit. Direction: "Nature's garage." A video-game car garage, but the models are
flowers: SELECT MODEL flips through flowers opening on a black showroom floor; SELECT PAINT re-sprays a rose on
the beat; then the drop is the drive - fields, droplets, blooms cut on every hit. Ends: BUILT BY NATURE.
The song agrees with the picture: "devagar, devagar" (slowly, slowly) = flowers opening slowly; "vai, vai, vai"
(go, go, go) = the menu flips a model on every "vai"; the drop (13.769 s) = the drive.
Song: 06 Oya Sa Funk from 3.0 s. Footage: Mixkit (free licence), 720p, shown as a 1080x1080 showroom square."""
import os, sys, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, os.path.dirname(__file__))
import cardedit
from cardedit import ROOT, W, H, SQ_Y, ANTON, ORB, ease, dec

OFF = 3.0
sh = lambda t, f, src, mode='real', name='': dict(t=round(t, 3), file=f, src=src, cx=0.5, mode=mode, name=name)
F = {k: v for k, v in (
    (17852, '17852_red-roses-opening-on-black-background.mp4'), (34515, '34515_white-rose-blooming-on-black-background.mp4'),
    (17845, '17845_yellow-orchid-opens-on-black-background.mp4'), (17853, '17853_a-purple-orchid-flower-opens-on-the-bran.mp4'),
    (17850, '17850_red-orchid-opens-on-black-background.mp4'), (38370, '38370_yellow-orchids-opening-on-a-black-backgr.mp4'),
    (17813, '17813_pink-orchid-on-a-black-background.mp4'), (17854, '17854_a-white-orchid-flower-opens-on-the-branc.mp4'),
    (17738, '17738_rose-flower-on-black-background.mp4'), (32302, '32302_flying-and-spinning-over-a-sunflower-fie.mp4'),
    (29344, '29344_gentle-water-drops-falling-on-a-rose.mp4'), (4881, '4881_gigantic-field-of-sunflowers-on-a-sunny-.mp4'),
    (28820, '28820_blooming-rose-flower-in-the-branch.mp4'), (16020, '16020_sunset-over-lavender-field.mp4'),
    (28833, '28833_blooming-yellow-and-violet-orchid-flower.mp4'), (40294, '40294_pink-rose-with-water-drops-on-the-petals.mp4'),
    (25154, '25154_flying-above-a-sunflower-field-in-the-su.mp4'), (28839, '28839_blooming-yellow-orchid.mp4'),
    (17848, '17848_lavender-field-in-an-orange-sunset.mp4'), (34627, '34627_purple-flower-blooming-slowly.mp4'),
    (17760, '17760_pink-flower-moving-and-opening.mp4'), (17816, '17816_white-rose-on-the-bush-opens.mp4'),
    (17819, '17819_orange-rose-flower-opens-on-the-bush.mp4'), (17820, '17820_red-orchid-on-the-branch-opens.mp4'),
    (4483, '4483_flowers-slowly-opening.mp4'), (29420, '29420_rose-falling-against-a-black-screen.mp4'))}
s = lambda song_t: song_t - OFF                     # song time -> edit time

PLAN = [
    # SELECT MODEL - "não fala nada, só olha pra trás"
    sh(0.0, F[17852], 3.0, 'real', 'RED ROSE'),
    sh(s(5.94), F[34515], 1.0, 'slow', 'WHITE ROSE'),        # "devagar" - slowly
    sh(s(7.64), F[17845], 2.0, 'slow', 'YELLOW ORCHID'),     # "devagar" - slowly
    sh(s(9.32), F[17853], 3.0, 'real', 'PURPLE ORCHID'),     # "a glória"
    sh(s(10.36), F[17850], 3.0, 'real', 'RED ORCHID'),       # vai
    sh(s(10.76), F[38370], 3.0, 'real', 'GOLD ORCHID'),      # vai
    sh(s(11.54), F[17813], 3.0, 'real', 'PINK ORCHID'),      # vai
    sh(s(11.98), F[17854], 3.0, 'real', 'WHITE ORCHID'),     # vai
    # SELECT PAINT - one rose, re-sprayed on the hits (no cut: the paint change is the accent)
    sh(s(12.488), F[17738], 1.0, 'real', 'paint'),
    # DROP - the drive
    sh(s(13.769), F[32302], 2.0),        # spinning over the sunflowers
    sh(s(14.634), F[29344], 1.0),        # detail: water on the petals
    sh(s(15.064), F[4881], 3.0),
    sh(s(15.490), F[28820], 2.0),
    sh(s(15.920), F[16020], 4.0),
    sh(s(17.198), F[28833], 4.0),
    sh(s(17.625), F[40294], 2.0),
    sh(s(18.491), F[25154], 1.0),
    sh(s(19.347), F[28839], 3.0),
    sh(s(19.769), F[17848], 4.0),
    sh(s(20.626), F[34627], 2.0),
    sh(s(21.914), F[17760], 6.0),
    sh(s(22.347), F[17816], 5.0),
    sh(s(22.770), F[17819], 5.0),
    dict(sh(s(23.204), F[17820], 10.0), cx=0.15),
    sh(s(24.056), F[4483], 8.0),
    dict(sh(s(24.918), F[29420], 5.0, 'real'), cx=0.92),  # the last rose falls - BUILT BY NATURE.
]
END = s(27.3)
PAINT_T = [s(12.488), s(12.942), s(13.340)]                     # re-spray on these hits
PAINTS = [('CRIMSON', 0, 1.0, (200, 20, 40)), ('ROSE GOLD', 22, 0.75, (232, 160, 120)),
          ('ELECTRIC BLUE', 165, 1.1, (40, 90, 255)), ('MIDNIGHT VIOLET', 200, 1.0, (130, 40, 200))]
I_PAINT = 8; I_DROP = 9


def paint_idx(t):
    return max(0, min(len(PAINTS) - 1, sum(1 for p in PAINT_T if t >= p) - 1))


def pre_fx(fr, i, t, lt):
    if i != I_PAINT: return fr
    k = paint_idx(t)
    _, hue, sat, _ = PAINTS[k]
    if hue == 0 and sat == 1.0: return fr
    im = Image.fromarray((np.clip(fr, 0, 1) * 255).astype(np.uint8)).convert('HSV')
    hsv = np.asarray(im).astype(np.int16).copy()
    hsv[..., 0] = (hsv[..., 0] + hue) % 256
    hsv[..., 1] = np.clip(hsv[..., 1] * sat, 0, 255)
    out = np.asarray(Image.fromarray(hsv.astype(np.uint8), 'HSV').convert('RGB')).astype(np.float32) / 255
    since = t - max(p for p in PAINT_T if t >= p)
    return out + (1 - out) * 0.35 * math.exp(-since / 0.06)              # spray flash on the hit


_f = {}
def font(path, size):
    if (path, size) not in _f: _f[(path, size)] = ImageFont.truetype(path, size)
    return _f[(path, size)]


def overlay(a, f, t, i, lt):
    """Garage menu: header, SELECT MODEL / SELECT PAINT with arrows and swatches (only before the drop)."""
    im = Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8)); d = ImageDraw.Draw(im)
    if t < PLAN[I_DROP]['t']:
        hdr = "NATURE'S GARAGE"; fh = font(ORB, 46); bb = d.textbbox((0, 0), hdr, font=fh)
        d.text(((W - bb[2]) / 2, 200), hdr, font=fh, fill=(255, 255, 255))
        d.line([(W / 2 - 240, 268), (W / 2 + 240, 268)], fill=(255, 255, 255), width=2)
        paint = i == I_PAINT
        cap = 'SELECT PAINT' if paint else 'SELECT MODEL'
        fc = font(ORB, 34); bb = d.textbbox((0, 0), cap, font=fc)
        d.text(((W - bb[2]) / 2, SQ_Y + W + 30), cap, font=fc, fill=(200, 200, 200))
        name = PAINTS[paint_idx(t)][0] if paint else PLAN[i]['name']
        fn = font(ANTON, 88); bb = d.textbbox((0, 0), name, font=fn)
        y = SQ_Y + W + 80; d.text(((W - bb[2]) / 2, y), name, font=fn, fill=(255, 255, 255))
        press = max(0.0, 1 - lt / 0.18) if not paint else 0.0                 # the > arrow 'clicks' on each change
        fa = font(ANTON, 110)
        d.text((70, y - 12), '‹', font=fa, fill=(170, 170, 170))
        d.text((W - 110 + int(14 * press), y - 12), '›', font=fa, fill=(255, 255, int(255 * (1 - press))))
        if paint:
            k = paint_idx(t); n = len(PAINTS); r = 34; x0 = W / 2 - (n - 1) * 52
            for j, (_, _, _, col) in enumerate(PAINTS):
                cx = x0 + j * 104; cy = y + 150
                d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col)
                if j == k: d.ellipse([cx - r - 9, cy - r - 9, cx + r + 9, cy + r + 9], outline=(255, 255, 255), width=5)
    return np.asarray(im).astype(np.float32) / 255


CFG = dict(
    name='O', layout='square', srcdir=os.path.join(ROOT, 'src_nat'), tmp=os.path.join(ROOT, 'tmp_o'),
    song=os.path.join(ROOT, 'songs', 'named', '06_oya_sa_funk_144bpm.mp3'), song_offset=OFF,
    out=os.path.join(ROOT, 'out', 'edit_O_nature.mp4'), end=END, plan=PLAN,
    swing=set(), drop={I_DROP}, punch=set(range(I_DROP, len(PLAN) - 1)), warm=0.01, sat=1.08,
    fx={I_DROP: ('radial',), 13: ('radial',), 17: ('radial',)},
    pre_fx=pre_fx, overlay=overlay,
    text=[(PLAN[I_DROP]['t'], PLAN[I_DROP + 2]['t'], 'FULL|BLOOM.'), (PLAN[-1]['t'] + 0.3, END, 'BUILT BY|NATURE.')],
    text_cy=SQ_Y + 230,
)

if __name__ == '__main__':
    cardedit.run(CFG, sys.argv)
