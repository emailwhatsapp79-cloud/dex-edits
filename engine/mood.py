"""MOOD EDIT renderer (Desmond, Nov 21 - refs AE1-AE5): full-screen 9:16, a few slow-motion shots, one cut per musical bar,
no captions/commentary/banner, a calm song, film grade, a small DEX EDITS mark, then the end card.
Rendered at 720x1280: a 608x1080 slice of a 1080p source only needs 1.18x (sharp; TikTok serves our posts at 540-576p anyway).
cfg: name, fps, song, song_in, shots [(path, t0, cx)] (cx = crop centre x in source pixels), every (beats per cut),
     slow (0.5 = half speed via RIFE in-betweens), grade (True), card (s)"""
import os, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import fx, hype, lyric

W, H = 720, 1280
ANTON = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'fonts', 'Anton.ttf')


def frames(path, t0, cx, dur, fps):
    """Source frames from t0 (dur s): 9:16 slice of the full height around cx, scaled to WxH."""
    sw = 608
    x = int(min(max(cx - sw // 2, 0), 1920 - sw))
    vf = f'fps={fps},crop={sw}:1080:{x}:0,scale={W}:{H}:flags=lanczos'
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{t0:.3f}', '-t', f'{dur + 0.2:.3f}', '-i', path, '-vf', vf,
                          '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True, check=True, stdin=subprocess.DEVNULL).stdout
    n = len(raw) // (W * H * 3)
    return np.frombuffer(raw[:n * W * H * 3], np.uint8).reshape(n, H, W, 3)


def mark(img):
    d = ImageDraw.Draw(img); f = ImageFont.truetype(ANTON, 34); t = 'DEX EDITS'
    b = f.getbbox(t); d.text(((W - (b[2] - b[0])) // 2, 60), t, font=f, fill=(255, 255, 255, 150))
    return img


def card(u):
    c = Image.fromarray(hype.endcard(u)).resize((W, W), Image.LANCZOS)
    img = Image.new('RGB', (W, H), (0, 0, 0)); img.paste(c, (0, (H - W) // 2)); return np.asarray(img)


def render(cfg, scratch, out):
    fps, slow = cfg.get('fps', 25), cfg.get('slow', 0.5)
    beats = [b - cfg['song_in'] for b in hype.song_beats(cfg['song'], cfg['song_in'], 40.0, cfg.get('every', 4))]
    cuts = [0.0] + [b for b in beats if b > 0.8][:len(cfg['shots'])]
    tmp = os.path.join(scratch, 'tmp_' + cfg['name']); os.makedirs(tmp, exist_ok=True); body = os.path.join(tmp, 'body.mp4')
    enc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(fps),
                            '-i', '-', '-c:v', 'libx264', '-crf', '14', '-preset', 'fast', '-pix_fmt', 'yuv420p', body], stdin=subprocess.PIPE)
    for i, (path, t0, cx) in enumerate(cfg['shots']):
        n = round(cuts[i + 1] * fps) - round(cuts[i] * fps); src = frames(path, t0, cx, n / fps * slow + 0.2, fps)
        for j in range(n):
            x = j * slow; i0 = min(int(x), len(src) - 2); fr = x - int(x)
            f = src[i0] if fr < 0.05 else fx.tween(src[i0], src[i0 + 1], fr)
            if cfg.get('grade', True): f = lyric.film(f)
            if j < 6: f = hype.flash(f, 0.25 * (1 - j / 6)) if i else f                     # soft dip on each cut
            enc.stdin.write(np.asarray(mark(Image.fromarray(f))).tobytes())
    nc = round(cfg.get('card', 1.6) * fps)
    for j in range(nc): enc.stdin.write(card(j / fps).tobytes())
    enc.stdin.close(); enc.wait()
    total = round(cuts[len(cfg['shots'])] * fps) / fps + nc / fps
    si = cfg['song_in']
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', body, '-i', cfg['song'], '-filter_complex',
                    f"[1:a]atrim={si:.3f}:{si + total:.3f},asetpts=PTS-STARTPTS,afade=t=in:d=0.3,afade=t=out:st={total - 1.2:.3f}:d=1.2[a]",
                    '-map', '0:v', '-map', '[a]', '-t', f'{total:.3f}', '-c:v', 'libx264', '-crf', '16', '-preset', 'slow',
                    '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '256k', '-movflags', '+faststart', out], check=True)
    return out, total
