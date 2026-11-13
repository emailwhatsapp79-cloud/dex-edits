"""Master edit renderer (Desmond, Nov 12): STORY + HYPE in one - continuous voice parts (never chopped, our captions) between
beat parts where every hit gets its own move (hype.entry), a position counter, AI slow motion (fx.tween / RIFE) on chosen
shots, a cold open with the subject cut out + text behind + a 3D camera push (fx.depth / fx.parallax), and a black-and-white
ending. Square 1080x1080 frames through Python (one segment at a time - low memory); the final ffmpeg pass pads to 1080x1920,
mixes song + voices (song ducked under voices) and adds the in-picture branding.
cfg: name, fps, files {key: (path, crop_vf)}, song, song_in, segments [...]:
  dict(type='voice', k, a, b, words=[(t, 'LINE')], hero=dict(at, text, dur), count=None|int, count_to=(t, int))
  dict(type='beats', cuts=[song s], end=song s, shots=[dict(k, t, fx, count, slow=1.0, bw)])
  dict(type='end', k, at, text, dur)"""
import os, subprocess
import numpy as np
from PIL import Image, ImageOps
import fx, look, hype

S = 1080


def read(path, vf, t0, dur, fps):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{max(0, t0):.3f}', '-t', f'{dur + 0.1:.3f}', '-i', path, '-vf',
                          f'fps={fps},{vf}', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True, check=True,
                         stdin=subprocess.DEVNULL).stdout
    n = len(raw) // (S * S * 3)
    return np.frombuffer(raw[:n * S * S * 3], np.uint8).reshape(n, S, S, 3)


def stream(path, vf, t0, dur, fps):
    """Frames one at a time (long voice parts would need GBs if read at once)."""
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-ss', f'{max(0, t0):.3f}', '-t', f'{dur + 0.1:.3f}', '-i', path, '-vf',
                          f'fps={fps},{vf}', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE,
                         stdin=subprocess.DEVNULL)
    last = None
    while True:
        buf = p.stdout.read(S * S * 3)
        if len(buf) < S * S * 3: break
        last = np.frombuffer(buf, np.uint8).reshape(S, S, 3); yield last
    p.wait()
    while True: yield last                                   # hold the last frame if the source runs short


def caption_layer(text, cache={}):
    if text not in cache: cache[text] = Image.open(look.caption_png(text, S, S, f'/tmp/claude-1000/cap_{abs(hash(text))}.png', 64, 0.82))
    return cache[text]


def render(cfg, scratch, out):
    fps, F, s0 = cfg.get('fps', 50), cfg['files'], cfg['song_in']
    tmp = os.path.join(scratch, 'tmp_' + cfg['name']); os.makedirs(tmp, exist_ok=True)
    body = os.path.join(tmp, 'body.mp4')
    enc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{S}x{S}', '-r', str(fps),
                            '-i', '-', '-c:v', 'libx264', '-crf', '14', '-preset', 'fast', '-pix_fmt', 'yuv420p', body],
                           stdin=subprocess.PIPE)
    put = lambda img: enc.stdin.write(np.asarray(img.convert('RGB')).tobytes())
    t_edit, voices, duck = 0.0, [], []                    # voices: (k, a, b, at); duck: (from, to) edit seconds
    pos_prev = None
    for seg in cfg['segments']:
        if seg['type'] == 'voice':
            k, a, b = seg['k'], seg['a'], seg['b']; d = b - a; n = round(d * fps)
            path, vf = F[k]; src = stream(path, vf, a, d, fps)
            hero = seg.get('hero'); hv = None
            if hero:
                hi = Image.fromarray(read(path, vf, hero['at'], 0.05, fps)[0])
                hv = fx.hero(hi, hero['text']); hd = fx.depth(hv)
            ws = seg.get('words', [])
            for j in range(n):
                t = j / fps; ts = a + t; fr_j = next(src)
                if hv is not None and t < hero['dur']:
                    f = fx.parallax(hv, hd, t / hero['dur'], amount=70, zoom_k=0.14)
                    if t < 0.12: f = hype.flash(f, 0.8 * (1 - t / 0.12))
                else:
                    f = fr_j
                    if hv is not None and t < hero['dur'] + 0.1: f = hype.flash(f, 0.6)
                img = Image.fromarray(np.ascontiguousarray(f)).convert('RGBA')
                line = [x for x in ws if x[0] <= ts]
                if line and ts < line[-1][0] + 2.4 and ts < b - 0.05: img.alpha_composite(caption_layer(line[-1][1]))
                c = seg.get('count')
                if c is not None:
                    ct = seg.get('count_to')
                    cur = ct[1] if ct and ts >= ct[0] else c
                    hype.counter(img, cur, max(0, 1 - (ts - ct[0]) / 0.3) if ct and ts >= ct[0] else 0); pos_prev = cur
                put(img)
            voices.append((k, a, b, t_edit)); duck.append((t_edit, t_edit + d)); t_edit += d
        elif seg['type'] == 'beats':
            cuts, end = seg['cuts'], seg['end']
            for i, sh in enumerate(seg['shots']):
                a = cuts[i]; b = cuts[i + 1] if i + 1 < len(cuts) else end
                n = round((b - s0) * fps) - round((a - s0) * fps); d = n / fps; slow = sh.get('slow', 1.0)
                path, vf = F[sh['k']]; src = read(path, vf, sh['t'], d * slow + 0.2, fps)
                for j in range(n):
                    t = j / fps
                    if slow < 1.0:                          # AI slow motion: in-between frames from RIFE
                        x = j * slow; i0 = min(int(x), len(src) - 2); fr = x - int(x)
                        f = src[i0] if fr < 0.05 else fx.tween(src[i0], src[i0 + 1], fr)
                    else:
                        f = src[min(j, len(src) - 1)]
                    if sh.get('bw'): f = np.asarray(ImageOps.autocontrast(ImageOps.grayscale(Image.fromarray(f)), cutoff=2).convert('RGB'))
                    if t < 0.22: f = hype.entry(f, sh.get('fx', 'punch'), t / 0.22, i)
                    img = Image.fromarray(np.ascontiguousarray(f)).convert('RGBA')
                    if sh.get('count') is not None:
                        hype.counter(img, sh['count'], max(0, 1 - t / 0.25) if sh['count'] != pos_prev else 0)
                    if sh.get('stamp'): hype.stamp(img, sh['stamp'], t / d)
                    put(img)
                if sh.get('count') is not None: pos_prev = sh['count']
                t_edit += d
        elif seg['type'] == 'end':
            path, vf = F[seg['k']]; fr = read(path, vf, seg['at'], 0.1, fps)[0]
            hv = fx.hero(Image.fromarray(fr), None, dark=0.35)
            hv = ImageOps.autocontrast(ImageOps.grayscale(hv), cutoff=1).convert('RGB'); hd = fx.depth(hv)
            n = round(seg['dur'] * fps)
            for j in range(n):
                u = j / n; f = fx.parallax(hv, hd, u, amount=50, zoom_k=0.12)
                if j < 6: f = hype.flash(f, 0.9 * (1 - j / 6))
                img = Image.fromarray(f).convert('RGBA'); hype.stamp(img, seg['text'], u); put(img)
            t_edit += seg['dur']
    enc.stdin.close(); enc.wait()
    total = t_edit
    cmd = ['ffmpeg', '-v', 'error', '-y', '-i', body, '-ss', f'{s0:.3f}', '-t', f'{total:.3f}', '-i', cfg['song'],
           '-loop', '1', '-framerate', str(fps), '-t', f'{total:.3f}', '-i', look.banner_png(cfg['title'], os.path.join(tmp, 'banner.png'))]
    for k, a, b, at in voices: cmd += ['-ss', f'{a:.3f}', '-t', f'{b - a + 0.05:.3f}', '-i', F[k][0]]
    chain = '[0:v]pad=1080:1920:0:420:black[pd];'
    flt, cur = look.brand_filter('[pd]', 2, total, t_in=cfg.get('banner_in', 0.4))
    chain += flt + f"{cur}fade=t=out:st={total - 0.8:.3f}:d=0.8[v];"
    under = cfg.get('song_under', 0.22)
    vol = '1'
    for a, b in reversed(duck): vol = f"if(between(t,{a:.3f},{b - 0.1:.3f}),{under},{vol})"
    chain += f"[1:a]volume='{vol}':eval=frame,afade=t=out:st={total - 2.0:.3f}:d=2.0[song];"
    labels = ['[song]']
    for i, (k, a, b, at) in enumerate(voices):
        chain += (f"[{3 + i}:a]aformat=sample_rates=44100:channel_layouts=stereo,afade=t=in:d=0.03,"
                  f"afade=t=out:st={b - a - 0.08:.3f}:d=0.08,volume={cfg.get('voice_gain', 1.7)},adelay={int(at * 1000)}|{int(at * 1000)}[v{i}];")
        labels.append(f'[v{i}]')
    chain += f"{''.join(labels)}amix=inputs={len(labels)}:normalize=0,alimiter=limit=0.9[a]"
    subprocess.run(cmd + ['-filter_complex', chain, '-map', '[v]', '-map', '[a]', '-t', f'{total:.3f}', '-r', str(fps)]
                   + look.encode_args(total, min(14, 92 * 8 / total)) + ['-c:a', 'aac', '-b:a', '256k', out], check=True)
    return out, total
