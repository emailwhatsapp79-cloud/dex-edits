"""YouTube Shorts version of a horizontal edit. YouTube only treats vertical/square uploads as Shorts - a 16:9 upload
becomes a normal video (no Shorts feed). So the 16:9 picture goes in as a sharp band (downscaled, never cropped or
blurred) on black, with a title above, then the DEX EDITS mark.
usage: python3 ytshort.py <unbranded horizontal.mp4> <out.mp4> 'TITLE|LINE 2'"""
import os, sys, subprocess
sys.path.insert(0, os.path.dirname(__file__))
import brand

FONT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'fonts', 'Anton.ttf')


def make(src, out, title='', fps=30):
    vf = 'scale=1080:-2:flags=lanczos,pad=1080:1920:0:(oh-ih)/2:black'
    for i, line in enumerate(l for l in title.split('|') if l):
        line = line.replace("'", '’').replace(':', '\\:')
        vf += (f",drawtext=fontfile={FONT}:text='{line}':fontsize=84:fontcolor=white:"
               f"x=(w-text_w)/2:y=(h-608)/2-{60 + 100 * (len(title.split('|')) - 1 - i)}-text_h")
    tmp = out.replace('.mp4', '_pre.mp4')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', src, '-vf', vf, '-c:v', 'libx264', '-crf', '10', '-preset', 'slow',
                    '-pix_fmt', 'yuv420p', '-c:a', 'copy', tmp], check=True)
    brand.brand(tmp, out, fps=fps); os.remove(tmp)
    return out


if __name__ == '__main__':
    print(make(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else '', int(sys.argv[4]) if len(sys.argv) > 4 else 30))
