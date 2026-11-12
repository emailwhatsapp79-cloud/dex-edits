"""Frame effects for the creative edits (Desmond, Nov 12: "every beat has animation... think outside the box"):
person cutout (silueta / U2-Net, onnxruntime, model in work/models), glowing outline, text BEHIND the subject, black-and-white
background, and the hero still used for freeze frames and the cold open."""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

MODEL = os.environ.get('DEX_SEG_MODEL', os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
                                                     'models', 'silueta.onnx'))
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ANTON = os.path.join(ROOT, 'fonts', 'Anton.ttf')
_sess = None


def mask(img):
    """Soft 0..1 person/object mask (same size as img) from silueta."""
    global _sess
    if _sess is None:
        import onnxruntime as ort
        _sess = ort.InferenceSession(MODEL, providers=['CPUExecutionProvider'])
    x = np.asarray(img.convert('RGB').resize((320, 320), Image.BILINEAR), dtype=np.float32) / 255.0
    x = (x - [0.485, 0.456, 0.406]) / [0.229, 0.224, 0.225]
    out = _sess.run(None, {_sess.get_inputs()[0].name: x.transpose(2, 0, 1)[None].astype(np.float32)})[0][0, 0]
    out = (out - out.min()) / (out.max() - out.min() + 1e-6)
    return Image.fromarray((out * 255).astype(np.uint8)).resize(img.size, Image.BILINEAR)


def glow_outline(m, width=6, blur=10, color=(255, 255, 255)):
    """RGBA glowing outline around mask m (white line + soft glow)."""
    hard = m.point(lambda v: 255 if v > 128 else 0)
    ring = Image.fromarray(np.clip(np.asarray(hard.filter(ImageFilter.MaxFilter(width * 2 + 1)), np.int16)
                                   - np.asarray(hard, np.int16), 0, 255).astype(np.uint8))
    glow = ring.filter(ImageFilter.GaussianBlur(blur)).point(lambda v: min(255, v * 3))
    a = np.maximum(np.asarray(ring), np.asarray(glow))
    out = Image.new('RGBA', m.size, color + (0,)); out.putalpha(Image.fromarray(a)); return out


def big_text(size, text, h_share=0.55, cy=0.45, fill=(255, 255, 255, 235), italic=0.12):
    """Huge condensed text layer (RGBA) for 'text behind the subject'."""
    W, H = size; fs = int(H * h_share)
    while True:
        f = ImageFont.truetype(ANTON, fs)
        if f.getlength(text) <= W * 0.94 or fs < 40: break
        fs -= 8
    b = f.getbbox(text); tw, th = b[2] - b[0], b[3] - b[1]
    layer = Image.new('RGBA', (tw + 200, th + 200), (0, 0, 0, 0))
    ImageDraw.Draw(layer).text((100 - b[0], 100 - b[1]), text, font=f, fill=fill)
    if italic: layer = layer.transform(layer.size, Image.AFFINE, (1, italic, -italic * layer.size[1] * 0.5, 0, 1, 0), Image.BICUBIC)
    out = Image.new('RGBA', size, (0, 0, 0, 0))
    out.alpha_composite(layer, ((W - layer.size[0]) // 2, int(H * cy - layer.size[1] / 2)))
    return out


def hero(img, text=None, bw_bg=True, dark=0.55, outline=True, text_cy=0.42, m=None):
    """The cold-open / freeze-frame look: background black-and-white + darkened, TEXT behind the subject, subject in colour
    on top with a glowing white outline. Returns RGB."""
    img = img.convert('RGB'); m = m or mask(img)
    bg = ImageOps.grayscale(img).convert('RGB') if bw_bg else img
    bg = Image.blend(Image.new('RGB', img.size, (0, 0, 0)), bg, dark).convert('RGBA')
    if text: bg.alpha_composite(big_text(img.size, text, cy=text_cy))
    subj = img.convert('RGBA'); subj.putalpha(m)
    bg.alpha_composite(subj)
    if outline: bg.alpha_composite(glow_outline(m))
    return bg.convert('RGB')
