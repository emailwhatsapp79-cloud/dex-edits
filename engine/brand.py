"""DEX EDITS branding pass: small semi-transparent wordmark in TikTok's safe zone (top centre, below the
status bar, clear of the right-side buttons and the bottom caption). Re-encodes to a file under 30 MB."""
import os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONT = os.path.join(ROOT, 'fonts', 'Anton.ttf')


def brand(src, dst, target_mb=27):
    d = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', src],
                             capture_output=True, text=True).stdout)
    target_mb = max(target_mb, d * 1.0)                    # long edits keep ~8 Mbps (a 58 s trailer must not drop to 3.5)
    br = int(target_mb * 8 * 1024 / d - 260)
    mark = (f"drawtext=fontfile={FONT}:text='DEX EDITS':fontsize=46:fontcolor=white@0.55:"
            f"shadowcolor=black@0.35:shadowx=2:shadowy=2:x=(w-text_w)/2:y=h*0.075")
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', src, '-vf', 'fps=30,' + mark,   # 30 fps: TikTok gives a fixed bitrate, so 30 fps = 2x bits per frame
                    '-c:v', 'libx264', '-preset', 'slow',
                    '-b:v', f'{br}k', '-maxrate', f'{int(br * 1.2)}k', '-bufsize', f'{br * 2}k', '-pix_fmt', 'yuv420p',
                    '-c:a', 'copy', '-movflags', '+faststart', dst], check=True)
    return dst


if __name__ == '__main__':
    for src in sys.argv[1:]:
        print(brand(src, src.replace('.mp4', '_DEX.mp4')))
