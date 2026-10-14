"""Edit P - NATURE (travel aesthetic) with lyrics. Direction: "I saw a piece of heaven."
Alpine / lake postcards, one per soft beat, each matching the sung line, and the lyrics on screen word by word
(small line as it is sung, the key word lands big): HEAVEN / ME / AWAY / SOMEDAY? / NOBODY KNOWS.
Lyrics (faster-whisper medium, word timings): "I saw a piece of heaven, waiting impatient for me. And I was running
far away, would I run off the world someday? Nobody knows, nobody knows."
4K look: 1080p sources where available (Coverr), clarity (local contrast), vibrance, fine sharpening.
Song: library #29. Footage: Coverr + Mixkit (free licences)."""
import os, sys, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
sys.path.insert(0, os.path.dirname(__file__))
import cardedit
from cardedit import ROOT, W, H, ANTON, ease

FONT_ARCHIVO = os.path.join(ROOT, 'fonts', 'Archivo.ttf')
sh = lambda t, f, src, cx=0.5, mode='real': dict(t=t, file=f if f.endswith('.mp4') else f'{f}.mp4', src=src, cx=cx, mode=mode)
PLAN = [
    sh(0.000, '48483', 3.0, 0.50),                                         # i saw a piece of... (clouds in the valley)
    sh(1.207, 'cv_mountains-in-lake-tekapo-new-zealand-5006', 4.0, 0.55),  # HEAVEN - the turquoise lake
    sh(2.389, 'cv_mountain-valley-landscape-9973', 8.0, 0.60),
    sh(3.678, '25234', 1.0, 0.45),                                         # waiting impatient - the empty bench
    sh(4.614, 'cv_lake-in-queenstown-new-zealand-7432', 5.0, 0.50),        # the mirror lake
    sh(5.865, 'cv_lush-green-mountain-pathway', 4.0, 0.55),                # for ME - the path that invites you
    sh(7.027, '100200', 10.0, 0.50),                                       # waterfall between green hills
    sh(8.316, '35528', 5.0, 0.50),                                         # mountain village in the sun
    sh(9.614, '31939', 3.0, 0.50),                                         # snowy Alps, the railway
    sh(10.502, 'cv_walking-down-a-road-in-the-mountains-4740', 4.0, 0.45), # and I was running...
    sh(11.668, 'cv_curvy-mountain-road-9336', 6.0, 0.55),                  # far AWAY - the road above the clouds
    sh(12.628, 'cv_edge-of-a-rocky-mountain-7100', 5.0, 0.55),             # would I run off the world
    sh(13.981, 'cv_overlooking-the-mountains-8002', 6.0, 0.45),            # SOMEDAY?
    sh(15.141, '3308', 2.0, 0.50),                                         # NOBODY KNOWS - mist
    sh(16.301, 'cv_mountain-tops-734', 4.0, 0.50),
    sh(17.271, '4396', 4.0, 0.50),                                         # nobody knows - fog
    sh(18.062, 'cv_sunrise-in-queenstown-new-zealand-9001', 8.0, 0.55),    # pink sunrise
]
END = 18.8

# (line start, line end, [(t, word), ...], (t, KEY) or None)
LYRICS = [
    (0.00, 3.80, [(0.00, 'i'), (0.68, 'saw'), (1.14, 'a'), (1.56, 'piece'), (1.68, 'of')], (2.12, 'HEAVEN')),
    (3.90, 7.20, [(3.90, 'waiting'), (4.40, 'impatient'), (5.48, 'for')], (6.38, 'ME')),
    (10.00, 12.85, [(10.00, 'and'), (10.56, 'i'), (10.90, 'was'), (11.18, 'running'), (11.60, 'far')], (12.20, 'AWAY')),
    (12.90, 15.25, [(12.90, 'would'), (13.00, 'i'), (13.68, 'run'), (13.88, 'off'), (14.05, 'the'), (14.20, 'world')], (14.42, 'SOMEDAY?')),
    (15.32, 17.30, [], (15.32, 'NOBODY|KNOWS')),
    (17.42, END, [(17.42, 'nobody'), (17.96, 'knows')], None),
]

_fc = {}
def archivo(size):
    if size not in _fc:
        f = ImageFont.truetype(FONT_ARCHIVO, size)
        try: f.set_variation_by_axes([600, 100])
        except Exception: pass
        _fc[size] = f
    return _fc[size]


def anton(size):
    k = ('anton', size)
    if k not in _fc: _fc[k] = ImageFont.truetype(ANTON, size)
    return _fc[k]


LEAD = 0.35            # lyrics lead the voice: a word starts appearing 0.35 s early and is fully on screen ~0.2 s
                       # before it is sung (Desmond: "it should show some ms before the music")


def overlay(a, f, t, i, lt):
    t = t + LEAD
    for s0, s1, words, key in LYRICS:
        if not (s0 <= t < s1): continue
        out = 1 - ease((t - (s1 - 0.25)) / 0.25)                                   # whole line fades out
        txt = Image.new('L', (W, H), 0); d = ImageDraw.Draw(txt)
        if words:                                                                  # small line, words appear as sung
            fs = archivo(60); full = ' '.join(w for _, w in words)
            x = (W - d.textlength(full, font=fs)) / 2; y = 1150
            for tw, w in words:
                k = ease((t - tw) / 0.15)
                if k > 0: d.text((x, y + 14 * (1 - k)), w, font=fs, fill=int(235 * k))
                x += d.textlength(w + ' ', font=fs)
        if key and t >= key[0]:                                                    # the key word lands big
            k = ease((t - key[0]) / 0.18); lines = key[1].split('|'); size = 170 if len(lines) == 1 else 150
            fk = anton(size)
            while max(d.textlength(l, font=fk) for l in lines) > 960: size -= 8; fk = anton(size)
            y0 = 1240 if words else 1050
            for n, l in enumerate(lines):
                d.text(((W - d.textlength(l, font=fk)) / 2, y0 + n * int(size * 1.05) + 30 * (1 - k)), l, font=fk, fill=int(255 * k))
        m = np.asarray(txt).astype(np.float32)[..., None] / 255 * out
        shadow = np.asarray(txt.filter(ImageFilter.GaussianBlur(14))).astype(np.float32)[..., None] / 255 * out
        a = a * (1 - np.clip(shadow * 1.3, 0, 0.6))
        a = a * (1 - m) + m
    return a


def pre_fx(fr, i, t, lt):
    """4K look: clarity (local contrast), vibrance, gentle highlight bloom."""
    h, w = fr.shape[:2]
    small = Image.fromarray((np.clip(fr, 0, 1) * 255).astype(np.uint8)).resize((w // 6, h // 6), Image.BILINEAR)
    base = np.asarray(small.filter(ImageFilter.GaussianBlur(4)).resize((w, h), Image.BILINEAR)).astype(np.float32) / 255
    a = np.clip(fr + 0.55 * (fr - base), 0, 1)                                     # clarity
    lum = a @ np.array([0.299, 0.587, 0.114], np.float32)
    sat = a.max(2) - a.min(2)
    a = lum[..., None] + (a - lum[..., None]) * (1 + 0.35 * (1 - sat))[..., None]  # vibrance: dull colours boosted most
    bloom = np.clip(base - 0.72, 0, 1) * 0.6                                        # soft glow on highlights
    return np.clip(a + bloom, 0, 1)


CFG = dict(
    name='P', layout='full', srcdir=os.path.join(ROOT, 'src_swiss'), tmp=os.path.join(ROOT, 'tmp_p'),
    song=os.path.join(ROOT, 'songs', 'named', '29_swiss_song_lyrics.mp3'), song_offset=0.0,
    out=os.path.join(ROOT, 'out', 'edit_P_heaven.mp4'), end=END, plan=PLAN,
    swing=set(), drop=set(), punch=set(), cut_flash=False, grain=0.08, vig=0.3, warm=0.012, sat=1.15,
    pre_fx=pre_fx, overlay=overlay, text=[], text_cy=960,
)

if __name__ == '__main__':
    cardedit.run(CFG, sys.argv)
