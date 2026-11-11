"""The "4K look" (Desmond, Nov 9 - refs AA1 @81l_l184 F1 Brazil, AA2/AA3 @agoftbl "France 4k" / "Lamine Yamal 4k").
Those edits are only 720p files, but they READ as 4K because of four things, all done here:
  1. sharp close-up sources at native size (no upscale anywhere in the chain - see EDITING_RULES "4K LOOK")
  2. a strong grade: deep blacks, real contrast, colour that pops (GRADES)
  3. sharpening AFTER every resize (CAS: adds edge contrast without halos)
  4. solid, bold captions that look designed (caption_png), not faded see-through text
Also: turned(src, dst) = the "turn your phone" 9:16 (16:9 picture rotated 90 deg, fills the screen at native size) for
the odd day - not the default.
usage: python3 look.py <in.mp4> <out.mp4> [bright|cine|pop|clean]     (grades a finished horizontal file, e.g. to test)"""
import os, subprocess, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONT = os.path.join(ROOT, 'fonts', 'Archivo.ttf')

GRADES = {
    # AA1 F1 look: crushed blacks, cool teal shadows, warm highlights, soft vignette (measured: avg luma ~75, sat ~13)
    'cine': ("curves=all='0/0 0.18/0.04 0.50/0.44 0.88/0.90 1/1',"
             "colorbalance=rs=-0.07:gs=0.01:bs=0.09:rh=0.05:bh=-0.05,"
             "eq=contrast=1.15:saturation=0.95,vignette=PI/4.5"),
    # AA2/AA3 "4k" look: bright, punchy, saturated, crisp (measured: avg luma ~108, sat ~29 - twice ours)
    'pop': ("curves=all='0/0 0.20/0.13 0.80/0.88 1/1',"
            "eq=contrast=1.14:saturation=1.50:gamma=1.03"),
    # AA5/AA6 "[4K]" look (Desmond, Nov 11: "this type and not dark" - clorix.kw Neymar 4.4M, agoftbl Yamal 12.6M): bright,
    # very saturated (ref sat ~39 = 3x ours), lifted mids, 'clarity' (large-radius unsharp = local contrast), no vignette.
    # THE DEFAULT. Grey rainy F1 footage needs the strong vibrance to get there.
    'bright': ("eq=contrast=1.12:brightness=0.02:saturation=1.45:gamma=1.06,vibrance=intensity=0.45,"
               "curves=all='0/0 0.25/0.22 0.75/0.82 1/1',unsharp=13:13:0.45:13:13:0"),
    # light touch for footage that is already graded (press films, trailers)
    'clean': "eq=contrast=1.06:saturation=1.12",
}
SHARPEN = 'cas=0.7'           # run after the LAST resize; 0.4-0.8 (higher = crunchier; the [4K] refs are very crisp)


def vf(grade='bright'):
    """Grade + sharpen, ready to append to a filter chain after scaling."""
    return f"{GRADES[grade]},{SHARPEN}"


def scale(W, H):
    """The only resize we use: lanczos, so a downscale stays crisp. Never call it to make a picture bigger than ~1.1x."""
    return f'scale={W}:{H}:flags=lanczos'


def caption_png(text, W, H, out, size=48, cy=0.78, italic=0.2, weight=900, width=88):
    """AA1 caption: solid white heavy italic capitals with a soft dark shadow, centred, lower part of the frame.
    Fully opaque - it must look designed and confident, not like a watermark."""
    while True:
        f = ImageFont.truetype(FONT, size)
        try: f.set_variation_by_axes([weight, width])
        except Exception: pass
        if f.getlength(text) <= W * 0.86 or size <= 24: break
        size -= 2
    box = f.getbbox(text); tw, th = box[2] - box[0], box[3] - box[1]
    pad = int(size * 0.6) + int(th * italic)
    tile = Image.new('L', (tw + 2 * pad, th + 2 * pad), 0)
    ImageDraw.Draw(tile).text((pad - box[0], pad - box[1]), text, font=f, fill=255)
    if italic:                                       # synthetic italic: shear the letters right
        tile = tile.transform(tile.size, Image.AFFINE, (1, italic, -italic * tile.size[1] * 0.5, 0, 1, 0), Image.BICUBIC)
    shadow = tile.filter(ImageFilter.GaussianBlur(max(3, size // 9))).point(lambda v: int(v * 0.75))
    x, y = (W - tile.size[0]) // 2, int(H * cy - tile.size[1] / 2)
    img = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    off = max(2, size // 18)
    img.paste(Image.new('RGBA', tile.size, (0, 0, 0, 255)), (x + off, y + off), shadow)
    img.paste(Image.new('RGBA', tile.size, (255, 255, 255, 255)), (x, y), tile)
    img.save(out); return out


def encode_args(seconds, mbps=None):
    """Final delivery encode: high bitrate so TikTok/YouTube re-encode from the cleanest possible copy."""
    br = int((mbps or 16) * 1000)
    return ['-c:v', 'libx264', '-preset', 'slow', '-profile:v', 'high', '-b:v', f'{br}k', '-maxrate', f'{int(br * 1.3)}k',
            '-bufsize', f'{br * 2}k', '-pix_fmt', 'yuv420p', '-movflags', '+faststart']


def grade_file(src, dst, grade='cine'):
    d = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', src],
                             capture_output=True, text=True).stdout)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', src, '-vf', vf(grade)] + encode_args(d) + ['-c:a', 'copy', dst], check=True)
    return dst


def turned(src, dst, fps=30):
    """'Turn your phone' 9:16: the 16:9 master rotated 90 deg clockwise, so the whole frame fills the phone at its native
    pixels (1920x1080 -> 1080x1920, 1280x720 -> 720x1280). No crop, no bars, no upscale. Use now and then, not every day.
    The DEX EDITS mark is drawn on the landscape picture first, so it reads upright when the viewer turns the phone."""
    mark = (f"drawtext=fontfile={os.path.join(ROOT, 'fonts', 'Anton.ttf')}:text='DEX EDITS':fontsize=h*0.04:"
            f"fontcolor=white@0.6:shadowcolor=black@0.35:shadowx=2:shadowy=2:x=(w-text_w)/2:y=h*0.05")
    d = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', src],
                             capture_output=True, text=True).stdout)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', src, '-vf', f'fps={fps},{mark},transpose=1'] + encode_args(d)
                   + ['-c:a', 'copy', dst], check=True)
    return dst


if __name__ == '__main__':
    print(grade_file(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else 'bright'))
