"""One thumbnail per source take (union of both cut detectors) -> tiled sheet, for picking shots."""
import os, sys, json, subprocess
sys.path.insert(0, os.path.dirname(__file__))
import velocity
from PIL import Image, ImageDraw

def union(path):
    cs = []
    for d in ('hist', 'scene'):
        velocity.DETECTOR = d; cs += velocity.source_cuts(path)
    cs = sorted(cs); return [c for i, c in enumerate(cs) if i == 0 or c - cs[i - 1] > 0.06]

def sheet(path, out, cols=10, tw=240, minlen=0.5):
    dur = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', path], capture_output=True, text=True).stdout)
    c = [0.0] + union(path) + [dur]
    takes = [(a, b) for a, b in zip(c, c[1:]) if b - a >= minlen]
    thumbs = []
    for a, b in takes:
        p = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{(a + b) / 2:.3f}', '-i', path, '-frames:v', '1', '-vf', f'scale={tw}:-2', '-f', 'image2pipe', '-vcodec', 'png', '-'], capture_output=True)
        import io; im = Image.open(io.BytesIO(p.stdout)).convert('RGB'); d = ImageDraw.Draw(im)
        d.rectangle((0, 0, 110, 14), fill=(0, 0, 0)); d.text((2, 1), f'{a:.2f}-{b:.2f}', fill=(255, 255, 0)); thumbs.append(im)
    th = thumbs[0].height; rows = (len(thumbs) + cols - 1) // cols
    S = Image.new('RGB', (cols * tw, rows * th))
    for i, im in enumerate(thumbs): S.paste(im, ((i % cols) * tw, (i // cols) * th))
    S.save(out, quality=85); json.dump(takes, open(out + '.json', 'w'))
    print(out, len(takes))

if __name__ == '__main__':
    for p in sys.argv[2:]: sheet(p, os.path.join(sys.argv[1], os.path.basename(p).replace('.mp4', '_takes.jpg')))
