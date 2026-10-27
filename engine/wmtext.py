"""Watermark-style lyrics (Desmond, Oct 23 - refs X9/X17 jet edits): the word sits INSIDE the picture - Archivo Expanded
Black (width 125, weight 900), letters filled with a sky texture, ~85% opacity, no outline, no shadow, centred.
word_png(text, w, h, out, size)  -> transparent PNG the size of the frame, ready for ffmpeg overlay.
overlay_filter(words, pngs)      -> filter_complex chain overlaying each PNG between its t0 and t1."""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONT = os.path.join(ROOT, 'fonts', 'Archivo.ttf')


def _font(size):
    f = ImageFont.truetype(FONT, size)
    try: f.set_variation_by_axes([900, 125])
    except Exception: pass
    return f


def _sky(w, h, seed=7):
    """A bright sky/cloud texture: blue at the top of the letters fading to white, soft cloud noise."""
    rng = np.random.default_rng(seed)
    y = np.linspace(0, 1, h)[:, None]
    base = np.dstack([95 + 150 * y, 160 + 95 * y, 235 + 20 * y]).repeat(w, axis=1)
    n = rng.random((h // 16 + 2, w // 16 + 2))
    n = np.array(Image.fromarray((n * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC).filter(ImageFilter.GaussianBlur(10)), np.float32) / 255
    img = base * (0.78 + 0.45 * n[..., None])
    return Image.fromarray(np.clip(img, 0, 255).astype(np.uint8))


def word_png(text, w, h, out, size=None, opacity=0.9, cy=0.6):
    size = size or int(h * 0.17)
    f = _font(size)
    while f.getlength(text) > w * 0.86 and size > 20:
        size -= 4; f = _font(size)
    box = f.getbbox(text)
    tw, th = box[2] - box[0], box[3] - box[1]
    x, y = (w - tw) // 2 - box[0], int(h * cy - th / 2) - box[1]
    mask = Image.new('L', (w, h), 0)
    ImageDraw.Draw(mask).text((x, y), text, font=f, fill=int(255 * opacity))
    tex = _sky(w, h)
    rgba = tex.convert('RGBA'); rgba.putalpha(mask)
    rgba.save(out)
    return out


def overlay_filter(words, first_png_input, src='[v0]'):
    """words: [(t0, t1, text)], PNG inputs start at index first_png_input. Returns (filter, last_label)."""
    chain, cur = '', src
    for i, (t0, t1, _) in enumerate(words):
        nxt = f'[w{i}]'
        chain += f"{cur}[{first_png_input + i}:v]overlay=0:0:enable='between(t,{t0:.3f},{t1:.3f})'{nxt};"
        cur = nxt
    return chain, cur
