"""Hype edit renderer (Desmond, Nov 12: "every beat has animation... do something that would blow my mind"). Every frame goes
through Python, so each hit can get its own move: whip pans with motion blur, zoom-through, RGB split + shake, spin, glitch
slices, slides, white flash - plus speed ramps, freeze-frame cutouts (fx.hero: subject cut out, glowing outline, text behind
it) and a graphics layer (position counter that punches on every change, stamps). Square 1080x1080 picture; the final
ffmpeg pass pads to 1080x1920, adds the song and the in-picture branding (look.brand_filter).
Memory: one shot's frames at a time (~75 x 3.5 MB) - safe next to the Claude app on 8 GB.
cfg: name, fps, files, song, song_in, cuts, end, build (key, in), shots [dict(k, t, fx, ramp, freeze, count, stamp)],
     intro_text, end_text, title, crop"""
import os, subprocess, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageFilter
import fx, look

S = 1080
ANTON = fx.ANTON


def read_frames(path, t0, dur, fps, crop):
    cmd = ['ffmpeg', '-v', 'error', '-ss', f'{max(0, t0):.3f}', '-t', f'{dur + 0.1:.3f}', '-i', path,
           '-vf', f'fps={fps},crop=1080:1080:{crop}:0', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-']
    raw = subprocess.run(cmd, capture_output=True, check=True, stdin=subprocess.DEVNULL).stdout
    n = len(raw) // (S * S * 3)
    return np.frombuffer(raw[:n * S * S * 3], np.uint8).reshape(n, S, S, 3)


# ---------- per-frame moves (u = 0..1 progress through the entry window) ----------
def zoom(f, z, cx=0.5, cy=0.5):
    if z <= 1.001: return f
    w = int(S / z); x0 = int((S - w) * cx); y0 = int((S - w) * cy)
    return np.asarray(Image.fromarray(f[y0:y0 + w, x0:x0 + w]).resize((S, S), Image.BILINEAR))


def shift(f, dx, dy):
    return np.roll(np.roll(f, int(dy), 0), int(dx), 1)


def motion_blur(f, dx, dy, n=6):
    if abs(dx) + abs(dy) < 2: return f
    acc = np.zeros(f.shape, np.float32)
    for i in range(n): acc += shift(f, dx * i / (n - 1) - dx / 2, dy * i / (n - 1) - dy / 2)
    return (acc / n).astype(np.uint8)


def rgb_split(f, d):
    if abs(d) < 1: return f
    o = f.copy(); o[..., 0] = np.roll(f[..., 0], int(d), 1); o[..., 2] = np.roll(f[..., 2], -int(d), 1); return o


def rotate(f, deg):
    if abs(deg) < 0.2: return f
    return np.asarray(Image.fromarray(f).rotate(deg, Image.BILINEAR, expand=False).resize((S, S)))


def slices(f, amt, seed):
    rng = np.random.default_rng(seed); o = f.copy()
    for _ in range(7):
        y = rng.integers(0, S - 60); h = rng.integers(20, 90); o[y:y + h] = np.roll(f[y:y + h], int(rng.integers(-1, 2) * amt), 1)
    return rgb_split(o, amt * 0.4)


def flash(f, a):
    return (f.astype(np.float32) * (1 - a) + 255 * a).astype(np.uint8) if a > 0.01 else f


def entry(f, kind, u, i):
    """The move a shot makes as it lands on its hit; u = 0..1 over the first ~0.22 s."""
    e = 1 - u; e2 = e * e
    if kind == 'whip_l':   return motion_blur(shift(f, -S * 0.35 * e2, 0), -140 * e, 0)
    if kind == 'whip_r':   return motion_blur(shift(f, S * 0.35 * e2, 0), 140 * e, 0)
    if kind == 'whip_u':   return motion_blur(shift(f, 0, -S * 0.3 * e2), 0, -120 * e)
    if kind == 'zoom':     return motion_blur(zoom(f, 1 + 0.45 * e2), 0, 0) if e > 0 else f
    if kind == 'punch':    return rgb_split(zoom(f, 1 + 0.18 * e), 18 * e)
    if kind == 'spin':     return motion_blur(rotate(zoom(f, 1 + 0.3 * e), 25 * e2), 40 * e, 0)
    if kind == 'glitch':   return slices(f, 60 * e, i * 7 + int(u * 10)) if e > 0.15 else f
    if kind == 'shake':    return rgb_split(shift(zoom(f, 1.08), 26 * e * math.sin(u * 40), 18 * e * math.cos(u * 33)), 14 * e)
    if kind == 'flash':    return flash(zoom(f, 1 + 0.12 * e), 0.9 * e2)
    return f


# ---------- graphics layer ----------
_fonts = {}
def font(sz):
    if sz not in _fonts: _fonts[sz] = ImageFont.truetype(ANTON, sz)
    return _fonts[sz]


def counter(img, pos, pop):
    """Position counter, top-left of the picture: 'P' + number, punches (scale + white flash) when it changes."""
    sz = int(150 * (1 + 0.35 * pop)); f = font(sz); txt = f'P{pos}'
    layer = Image.new('RGBA', (600, 300), (0, 0, 0, 0)); d = ImageDraw.Draw(layer)
    d.text((14, 14), txt, font=f, fill=(0, 0, 0, 140))
    d.text((8, 8), txt, font=f, fill=(255, 255, 255, 235) if pop < 0.3 else (255, 220, 40, 255))
    img.alpha_composite(layer.transform(layer.size, Image.AFFINE, (1, 0.12, -18, 0, 1, 0), Image.BICUBIC), (36, 210))


def stamp(img, text, u):
    """Big word slammed onto the picture: scales down from 1.6x to 1x over the first 0.12 of its time."""
    k = 1 + 0.6 * max(0, 1 - u / 0.12) ** 2
    lay = fx.big_text((S, S), text, h_share=0.2 * k, cy=0.78)
    img.alpha_composite(lay)


def render(cfg, scratch, out):
    fps, F, crop = cfg.get('fps', 50), cfg['files'], cfg.get('crop', 420)
    cuts, s0, end = cfg['cuts'], cfg['song_in'], cfg['end']
    tmp = os.path.join(scratch, 'tmp_' + cfg['name']); os.makedirs(tmp, exist_ok=True)
    body = os.path.join(tmp, 'body.mp4')
    enc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{S}x{S}', '-r', str(fps),
                            '-i', '-', '-c:v', 'libx264', '-crf', '14', '-preset', 'fast', '-pix_fmt', 'yuv420p', body],
                           stdin=subprocess.PIPE)
    spans = [dict(cfg['build'], a=s0, b=cuts[0], build=True)] + [
        dict(sh, a=cuts[i], b=cuts[i + 1] if i + 1 < len(cuts) else end) for i, sh in enumerate(cfg['shots'])]
    pos_prev, frame_no = None, 0
    for i, sh in enumerate(spans):
        n = round((sh['b'] - s0) * fps) - round((sh['a'] - s0) * fps); d = n / fps
        ramp = sh.get('ramp', 1.0)                          # source seconds used per edit second on average (ramp >1 = speeds up)
        src = read_frames(F[sh['k']], sh['t'], d * max(1.0, ramp) * 1.2 + 0.2, fps, crop)
        hero = None
        if sh.get('freeze') or sh.get('build'):
            fz = src[min(len(src) - 1, int(sh.get('freeze_at', 0.4) * fps))]
            hero = np.asarray(fx.hero(Image.fromarray(fz), sh.get('freeze_text') or cfg.get('intro_text')))
        for j in range(n):
            t = j / fps; u = t / max(d, 1e-6)
            if sh.get('build'):                               # cold open: walk in B&W, then freeze into the cutout + P21
                if t < d * 0.55:
                    f = np.asarray(ImageOps.grayscale(Image.fromarray(src[min(j, len(src) - 1)])).convert('RGB'))
                    f = (f * min(1, t / 0.4) * 0.8).astype(np.uint8)
                else:
                    f = zoom(hero, 1 + 0.06 * (t - d * 0.55) / (d * 0.45)); f = flash(f, 0.8 * max(0, 1 - (t - d * 0.55) / 0.1))
            elif sh.get('freeze'):                            # freeze frame: play 0.2 s, then the cutout still with its word
                f = src[min(j, len(src) - 1)] if t < 0.2 else zoom(hero, 1 + 0.05 * u)
                if 0.2 <= t < 0.28: f = flash(f, 0.7)
            else:
                si = int(fps * (d * ramp) * (u ** 1.7 if ramp > 1 else u)) if ramp != 1.0 else j
                f = src[min(si, len(src) - 1)]
                if sh.get('bw'): f = np.asarray(ImageOps.autocontrast(ImageOps.grayscale(Image.fromarray(f)), cutoff=2).convert('RGB'))
            if not sh.get('build') and t < 0.22: f = entry(f, sh.get('fx', 'punch'), t / 0.22, i)
            img = Image.fromarray(np.ascontiguousarray(f)).convert('RGBA')
            pos = sh.get('count')
            if pos is not None and not sh.get('hide_count'):
                pop = max(0, 1 - t / 0.25) if pos != pos_prev else 0
                counter(img, pos, pop)
            if sh.get('stamp'): stamp(img, sh['stamp'], u)
            enc.stdin.write(np.asarray(img.convert('RGB')).tobytes()); frame_no += 1
        if sh.get('count') is not None: pos_prev = sh['count']
        del src
    enc.stdin.close(); enc.wait()
    total = end - s0
    cmd = ['ffmpeg', '-v', 'error', '-y', '-i', body, '-ss', f'{s0:.3f}', '-t', f'{total:.3f}', '-i', cfg['song'],
           '-loop', '1', '-framerate', str(fps), '-t', f'{total:.3f}', '-i',
           look.banner_png(cfg.get('title', 'DEX EDITS'), os.path.join(tmp, 'banner.png'))]
    chain = '[0:v]pad=1080:1920:0:420:black[pd];'
    flt, cur = look.brand_filter('[pd]', 2, total, t_in=cfg.get('banner_in', 2.6))
    chain += flt + f"{cur}fade=t=out:st={total - 0.6:.3f}:d=0.6[v];[1:a]afade=t=out:st={total - 1.2:.3f}:d=1.2,alimiter=limit=0.9[a]"
    subprocess.run(cmd + ['-filter_complex', chain, '-map', '[v]', '-map', '[a]', '-t', f'{total:.3f}', '-r', str(fps)]
                   + look.encode_args(total, 14) + ['-c:a', 'aac', '-b:a', '256k', out], check=True)
    return out, total
