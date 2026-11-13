"""Lyric edit (Desmond, Nov 13 - pro style of @moto.rho 357k / @n.y.z.r 720k): cuts on the sung words and beats, ONE big
elegant serif word per sung word (Noto Serif Display), a film grade (warm highlights, teal shadows, soft contrast), gentle
moves only (slow push, a soft zoom-in on the cut, a white flash on the drop) - emotion over effects. No counters, no cutouts.
Square 1080x1080 through Python, final pass pads to 1080x1920 with the in-picture branding, song only.
cfg: name, fps, files {key: (path, crop_vf)}, song, cuts [(t, key, src_in, speed=1.0)], end, words [(t, 'WORD', size)],
     flash [t...], title"""
import os, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import look, hype, master

S = 1080
SERIF = '/usr/share/fonts/truetype/noto/NotoSerifDisplay-Regular.ttf'
_f = {}


def font(sz):
    if sz not in _f: _f[sz] = ImageFont.truetype(SERIF, sz)
    return _f[sz]


def film(f):
    """Film grade: lifted blacks, teal shadows, warm highlights, slightly soft contrast."""
    x = f.astype(np.float32) / 255.0
    lum = x.mean(axis=2, keepdims=True)
    sh = np.clip(1 - lum * 2, 0, 1); hi = np.clip(lum * 2 - 1, 0, 1)
    x = x + sh * np.array([-0.035, 0.01, 0.035]) + hi * np.array([0.04, 0.015, -0.03])
    x = 0.04 + x * 0.94                                       # lifted blacks
    x = (x - 0.5) * 1.06 + 0.5
    return (np.clip(x, 0, 1) * 255).astype(np.uint8)


def word_layer(word, size, u):
    """Big serif word, centred; scales 1.12 -> 1.0 and fades in over the first 0.1 of its life (u in seconds)."""
    k = 1 + 0.12 * max(0, 1 - u / 0.12); sz = int(size * k)
    f = font(sz)
    while f.getlength(word) > S * 0.92 and sz > 60: sz -= 10; f = font(sz)
    lay = Image.new('RGBA', (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    b = f.getbbox(word); x = (S - (b[2] - b[0])) // 2 - b[0]; y = (S - (b[3] - b[1])) // 2 - b[1]
    sh = Image.new('RGBA', (S, S), (0, 0, 0, 0)); ImageDraw.Draw(sh).text((x + 4, y + 6), word, font=f, fill=(0, 0, 0, 120))
    lay.alpha_composite(sh.filter(ImageFilter.GaussianBlur(8)))
    a = int(255 * min(1, u / 0.08))
    d.text((x, y), word, font=f, fill=(255, 255, 255, a))
    return lay


def render(cfg, scratch, out):
    fps, F = cfg.get('fps', 25), cfg['files']
    tmp = os.path.join(scratch, 'tmp_' + cfg['name']); os.makedirs(tmp, exist_ok=True)
    body = os.path.join(tmp, 'body.mp4')
    enc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{S}x{S}', '-r', str(fps),
                            '-i', '-', '-c:v', 'libx264', '-crf', '14', '-preset', 'fast', '-pix_fmt', 'yuv420p', body],
                           stdin=subprocess.PIPE)
    cuts, end, words, flashes = cfg['cuts'], cfg['end'], cfg['words'], cfg.get('flash', [])
    for i, (a, k, si, *sp) in enumerate(cuts):
        speed = sp[0] if sp else 1.0
        b = cuts[i + 1][0] if i + 1 < len(cuts) else end
        n = round(b * fps) - round(a * fps); d = n / fps
        path, vf = F[k]; src = master.read(path, vf, si, d * speed + 0.2, fps)
        for j in range(n):
            t = j / fps; T = a + t
            f = src[min(int(j * speed), len(src) - 1)]
            f = hype.zoom(f, 1.03 + 0.05 * t / max(d, 0.1))            # slow push on every shot
            if t < 0.1: f = hype.zoom(f, 1 + 0.06 * (1 - t / 0.1))       # soft punch on the cut
            f = film(f)
            for fl in flashes:
                if 0 <= T - fl < 0.25: f = hype.flash(f, 0.85 * (1 - (T - fl) / 0.25))
            img = Image.fromarray(f).convert('RGBA')
            cur = [w for w in words if w[0] <= T]
            if cur:
                wt, word, size = cur[-1]; nxt = [w[0] for w in words if w[0] > wt]
                if T < (nxt[0] if nxt else wt + 1.2) and T < wt + 1.4: img.alpha_composite(word_layer(word, size, T - wt))
            enc.stdin.write(np.asarray(img.convert('RGB')).tobytes())
    enc.stdin.close(); enc.wait()
    total = end
    cmd = ['ffmpeg', '-v', 'error', '-y', '-i', body, '-i', cfg['song'], '-loop', '1', '-framerate', str(fps), '-t', f'{total:.3f}',
           '-i', look.banner_png(cfg['title'], os.path.join(tmp, 'banner.png'))]
    chain = '[0:v]pad=1080:1920:0:420:black[pd];'
    flt, cur = look.brand_filter('[pd]', 2, total, t_in=cfg.get('banner_in', 7.0), hold=2.6)
    chain += flt + f"{cur}fade=t=out:st={total - 0.8:.3f}:d=0.8[v];[1:a]atrim=0:{total:.3f},afade=t=out:st={total - 1.0:.3f}:d=1.0[a]"
    subprocess.run(cmd + ['-filter_complex', chain, '-map', '[v]', '-map', '[a]', '-t', f'{total:.3f}', '-r', str(fps)]
                   + look.encode_args(total, 14) + ['-c:a', 'aac', '-b:a', '256k', out], check=True)
    return out, total
