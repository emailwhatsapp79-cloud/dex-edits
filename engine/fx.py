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


# ---------- depth (Depth Anything V2 small, int8) - 2.5D camera moves on stills, depth blur ----------
_dsess = None
DEPTH_MODEL = os.path.join(os.path.dirname(MODEL), 'depth_v2_small_int8.onnx')


def depth(img):
    """0..1 depth map, 1 = nearest, same size as img."""
    global _dsess
    if _dsess is None:
        import onnxruntime as ort
        o = ort.SessionOptions(); o.enable_cpu_mem_arena = False; o.enable_mem_pattern = False
        _dsess = ort.InferenceSession(DEPTH_MODEL, o, providers=['CPUExecutionProvider'])
    x = np.asarray(img.convert('RGB').resize((518, 518), Image.BICUBIC), np.float32) / 255.0
    x = ((x - [0.485, 0.456, 0.406]) / [0.229, 0.224, 0.225]).transpose(2, 0, 1)[None].astype(np.float32)
    d = _dsess.run(None, {'pixel_values': x})[0][0]
    d = (d - d.min()) / (d.max() - d.min() + 1e-6)
    return np.asarray(Image.fromarray((d * 255).astype(np.uint8)).resize(img.size, Image.BILINEAR), np.float32) / 255.0


def parallax(img, d, u, amount=60, zoom_k=0.10, layers=4):
    """2.5D 'camera push' on a still: near layers move/zoom more than far ones (u = 0..1). Far gaps are filled by the
    blurred far layer. Returns RGB np."""
    a = np.asarray(img.convert('RGB')); H, W = a.shape[:2]
    out = np.asarray(Image.fromarray(a).filter(ImageFilter.GaussianBlur(8)))
    edges = np.linspace(0, 1, layers + 1)
    for li in range(layers):
        lo, hi = edges[li], edges[li + 1] + (1e-6 if li == layers - 1 else 0)
        m = ((d >= lo) & (d < hi)).astype(np.float32)
        if m.sum() < 50: continue
        k = (lo + hi) / 2
        z = 1 + zoom_k * u * (0.3 + k); dx = amount * u * (k - 0.5)
        lay = Image.fromarray(a).resize((int(W * z), int(H * z)), Image.BILINEAR)
        mk = Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(2)).resize(lay.size, Image.BILINEAR)
        x0 = int((lay.size[0] - W) / 2 - dx); y0 = int((lay.size[1] - H) / 2)
        lay = np.asarray(lay)[y0:y0 + H, x0:x0 + W]; mk = np.asarray(mk, np.float32)[y0:y0 + H, x0:x0 + W, None] / 255
        if lay.shape[:2] != (H, W): continue
        out = (out * (1 - mk) + lay * mk).astype(np.uint8)
    return out


def depth_blur(img, d, focus=0.8, strength=10):
    """Fake shallow depth of field: everything far from `focus` depth gets blurred."""
    a = np.asarray(img.convert('RGB'), np.float32); b = np.asarray(img.convert('RGB').filter(ImageFilter.GaussianBlur(strength)), np.float32)
    w = np.clip(np.abs(d - focus) * 2.2, 0, 1)[..., None]
    return (a * (1 - w) + b * w).astype(np.uint8)


# ---------- smooth slow motion (RIFE 4.7) ----------
_rsess = None
RIFE_MODEL = os.path.join(os.path.dirname(MODEL), 'rife47.onnx')


def tween(f0, f1, t):
    """AI in-between frame of two RGB np frames at time t (0..1). Pads to a multiple of 32."""
    global _rsess
    if _rsess is None:
        import onnxruntime as ort
        o = ort.SessionOptions(); o.enable_cpu_mem_arena = False; o.enable_mem_pattern = False   # keep RAM low on 8 GB
        _rsess = ort.InferenceSession(RIFE_MODEL, o, providers=['CPUExecutionProvider'])
    H, W = f0.shape[:2]; ph, pw = (32 - H % 32) % 32, (32 - W % 32) % 32
    prep = lambda f: np.pad(f, ((0, ph), (0, pw), (0, 0)), mode='edge').astype(np.float32).transpose(2, 0, 1)[None] / 255.0
    o = _rsess.run(None, {'img0': prep(f0), 'img1': prep(f1), 'timestep': np.array([t], np.float32)})[0][0]
    return (np.clip(o.transpose(1, 2, 0)[:H, :W], 0, 1) * 255).astype(np.uint8)
