"""DEX template "COUNTDOWN" (Top 5): each item plays with its OWN audio (commentary / crowd), so the sound always
matches the picture. Header "<NAME> / TOP 5" with five rank chips (current lit, done ticked), the rank pops big at
the start of each item with its caption, a white flash on every hard cut. Sources of any aspect are fitted to the
width over a blurred, darkened copy of themselves. Burned-in captions of the source can be blurred per piece.

A piece = dict(file, a, b, rank, cap, blur=[(y0_frac, y1_frac), ...], teaser=False)."""
import os, sys, math, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
sys.path.insert(0, os.path.dirname(__file__))
from cardedit import ROOT, ANTON, ORB, ease

W, H, FPS = 1080, 1920, 30
GOLD = (255, 200, 40)


def _font(path, size, var=None, _c={}):
    k = (path, size)
    if k not in _c:
        f = ImageFont.truetype(path, size)
        if var:
            try: f.set_variation_by_axes(var)
            except Exception: pass
        _c[k] = f
    return _c[k]


def probe(path):
    o = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v', '-show_entries', 'stream=width,height',
                        '-of', 'csv=p=0', path], capture_output=True, text=True).stdout.strip().split(',')
    return int(o[0]), int(o[1])


def frames(path, a, b, blur):
    """Yield the piece's frames composed to W x H (fit width, blurred fill), source captions blurred."""
    sw, sh = probe(path); fh = int(round(sh * W / sw / 2)) * 2
    n = int(round((b - a) * FPS))
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-ss', f'{a:.3f}', '-i', path, '-t', f'{b - a + 0.5:.3f}',
                          '-vf', f'fps={FPS},scale={W}:{fh}:flags=lanczos,unsharp=5:5:0.6',
                          '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
    last = None
    for _ in range(n):
        buf = p.stdout.read(W * fh * 3)
        if len(buf) < W * fh * 3:
            fr = last
        else:
            fr = np.frombuffer(buf, np.uint8).reshape(fh, W, 3); last = fr
        im = Image.fromarray(fr)
        for y0, y1 in blur:
            box = (0, int(y0 * fh), W, int(y1 * fh))
            c = im.crop(box).filter(ImageFilter.GaussianBlur(26)); g = c.convert('L').convert('RGB')
            im.paste(Image.blend(c, g, 0.7), box[:2])
        if fh >= H:
            out = im.crop((0, (fh - H) // 2, W, (fh - H) // 2 + H))
        else:
            sc = H / fh; bw = int(W * sc)
            bg = im.resize((bw, H)).crop(((bw - W) // 2, 0, (bw - W) // 2 + W, H)).filter(ImageFilter.GaussianBlur(40))
            bg = Image.eval(bg, lambda v: int(v * 0.45)); bg.paste(im, (0, (H - fh) // 2)); out = bg
        yield np.asarray(out).astype(np.float32) / 255
    p.stdout.close(); p.wait()


def overlay(a, piece, lt, name, ranks_done):
    im = Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8)).convert('RGBA')
    top = Image.new('RGBA', im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(top)
    for y in range(0, 470):                                                    # dark gradient behind the header
        d.line([(0, y), (W, y)], fill=(0, 0, 0, int(170 * (1 - y / 470) ** 1.4)))
    im = Image.alpha_composite(im, top); d = ImageDraw.Draw(im)
    title = f'{name} / TOP 5'; ft = _font(ANTON, 92)
    d.text(((W - d.textlength(title, font=ft)) / 2, 205), title, font=ft, fill=(255, 255, 255))
    r = piece['rank']; cw = 112; x0 = W / 2 - 2.5 * cw + 8
    for j, k in enumerate([5, 4, 3, 2, 1]):
        x = x0 + j * cw; cur = (k == r and not piece.get('teaser')); done = k in ranks_done
        fill = GOLD if cur else ((60, 60, 60) if not done else (235, 235, 235))
        d.rounded_rectangle([x, 330, x + cw - 16, 410], 14, fill=fill)
        fn = _font(ANTON, 56); s = f'{k}'
        d.text((x + (cw - 16 - d.textlength(s, font=fn)) / 2, 334), s, font=fn,
               fill=(10, 10, 10) if (cur or done) else (150, 150, 150))
    out = np.asarray(im.convert('RGB')).astype(np.float32) / 255
    # caption bar at the bottom (stays), the rank pops big at the start
    cap = piece['cap']; cs = 40; fc = _font(ORB, cs, [800])
    bar = Image.new('RGBA', (W, H), (0, 0, 0, 0)); bd = ImageDraw.Draw(bar)
    while bd.textlength(cap, font=fc) > 900: cs -= 2; fc = _font(ORB, cs, [800])
    tw = bd.textlength(cap, font=fc); k = ease(lt / 0.25)
    bd.rounded_rectangle([(W - tw) / 2 - 30, 1560, (W + tw) / 2 + 30, 1640], 16, fill=(0, 0, 0, int(190 * k)))
    bd.text(((W - tw) / 2, 1578), cap, font=fc, fill=(255, 255, 255, int(255 * k)))
    if not piece.get('teaser'):
        bd.rounded_rectangle([(W - tw) / 2 - 30, 1552, (W - tw) / 2 + 60, 1560], 3, fill=GOLD + (int(255 * k),))
    o = Image.alpha_composite(Image.fromarray((out * 255).astype(np.uint8)).convert('RGBA'), bar)
    out = np.asarray(o.convert('RGB')).astype(np.float32) / 255
    big = 'WAIT FOR|#1.' if piece.get('teaser') else f'#{r}'
    if piece.get('teaser') or (lt < 1.1 and not piece.get('cont')):
        k = ease(lt / 0.12) * (1 if piece.get('teaser') else 1 - ease((lt - 0.85) / 0.25))
        size = 170 if piece.get('teaser') else int(330 * (1 + 0.35 * (1 - ease(lt / 0.15))))
        import cardedit
        out = cardedit.put(out, big, k, size=size, cy=960)
    if lt < 2 / FPS: out = out + (1 - out) * (0.7 if lt < 1 / FPS else 0.3)   # flash on the cut
    return np.clip(out, 0, 1)


def render(pieces, name, out, tmp):
    os.makedirs(tmp, exist_ok=True); parts = []
    for n, pc in enumerate(pieces):
        path = pc['file']; a, b = pc['a'], pc['b']
        vtmp = os.path.join(tmp, f'v{n}.mp4'); ptmp = os.path.join(tmp, f'p{n}.mp4')
        done = {q['rank'] for q in pieces[:n] if not q.get('teaser')} - {pc['rank']}
        if os.environ.get('REUSE') and os.path.exists(ptmp): parts.append(ptmp); continue
        enc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}',
                                '-r', str(FPS), '-i', '-', '-c:v', 'libx264', '-crf', '14', '-preset', 'medium',
                                '-pix_fmt', 'yuv420p', vtmp], stdin=subprocess.PIPE)
        for f, fr in enumerate(frames(path, a, b, pc.get('blur', []))):
            enc.stdin.write((overlay(fr, pc, f / FPS, name, done) * 255).astype(np.uint8).tobytes())
        enc.stdin.close(); enc.wait()
        d = b - a
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', vtmp, '-ss', f'{a:.3f}', '-t', f'{d:.3f}', '-i', path,
                        '-map', '0:v', '-map', '1:a', '-c:v', 'copy',
                        '-af', f'loudnorm=I=-14:TP=-1.5,afade=t=in:d=0.03,afade=t=out:st={d - 0.05:.3f}:d=0.05,'
                               f'aresample=44100,apad=whole_dur={d:.3f}',
                        '-c:a', 'aac', '-b:a', '192k', '-shortest', ptmp], check=True)
        parts.append(ptmp); print('piece', n, 'done', flush=True)
    lst = os.path.join(tmp, 'list.txt')
    open(lst, 'w').write(''.join(f"file '{p}'\n" for p in parts))
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', lst, '-c:v', 'libx264',
                    '-crf', '15', '-preset', 'medium', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k', out],
                   check=True)
    print('done', out)


def still(pieces, name, n, lt, path):
    pc = pieces[n]; done = {q['rank'] for q in pieces[:n] if not q.get('teaser')} - {pc['rank']}
    for f, fr in enumerate(frames(pc['file'], pc['a'] + lt, pc['a'] + lt + 0.05, pc.get('blur', []))):
        Image.fromarray((overlay(fr, pc, lt, name, done) * 255).astype(np.uint8)).save(path); break
