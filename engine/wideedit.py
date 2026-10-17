"""Horizontal 16:9 edits at the source's NATIVE size (EDITING_RULES 'Pixels 1:1', ref M6): every source pixel is used
1:1 - no crop, no upscale. One word per shot (lyric style), cut on the word timings, light cinematic grade.

cfg = dict(song=path, off=song start s, end=edit length s, size=(1280, 720), font=path, fs=font size,
           shots=[(t, src, src_t, 'WORD' or '')], words=[(t0, t1, 'WORD')] optional extra text not tied to cuts)
Shots run from their t to the next shot's t. Modes: render (default) | stills (one frame per shot -> qc sheet)."""
import os, subprocess, sys, json
from PIL import Image

FPS = 30
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GRADE = 'eq=contrast=1.10:saturation=1.08:gamma=0.94,unsharp=3:3:0.25'   # crushed blacks, tiny edge lift (no halo)


def _esc(t):
    return t.replace('\\', '\\\\').replace("'", "’").replace(':', '\\:').replace(',', '\\,')


def _text(cfg, word, t0=None, t1=None):
    if not word:
        return ''
    en = f":enable='between(t,{t0:.3f},{t1:.3f})'" if t0 is not None else ''
    return (f",drawtext=fontfile={cfg['font']}:text='{_esc(word)}':fontsize={cfg['fs']}:fontcolor=white:"
            f"shadowcolor=black@0.55:shadowx=0:shadowy=4:x=(w-text_w)/2:y=(h-text_h)/2{en}")


def frames(cfg):
    ts = [s[0] for s in cfg['shots']] + [cfg['end']]
    fr = [round(t * FPS) for t in ts]
    return [b - a for a, b in zip(fr, fr[1:])]


def check(cfg):
    used = {}
    for (t, src, st, w), n in zip(cfg['shots'], frames(cfg)):
        d = n / FPS; dur = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', src], capture_output=True, text=True).stdout)
        assert st + d <= dur, f'{src} too short at {st}'
        for a, b in used.get(src, []):
            assert st + d <= a or st >= b, f'repeated footage {os.path.basename(src)} {st:.2f}'
        used.setdefault(src, []).append((st, st + d))
        print(f'{t:6.2f} {d:5.2f}s {os.path.basename(src)[:28]:28} @{st:7.2f} {w}')


def stills(cfg, out):
    W, H = cfg['size']; ims = []
    for (t, src, st, w), n in zip(cfg['shots'], frames(cfg)):
        p = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{st + n / FPS / 2:.3f}', '-i', src, '-frames:v', '1',
                            '-vf', f'scale={W}:{H}:flags=lanczos,{GRADE}' + _text(cfg, w), '-f', 'image2pipe', '-vcodec', 'png', '-'], capture_output=True)
        import io; ims.append(Image.open(io.BytesIO(p.stdout)).convert('RGB').resize((W // 3, H // 3)))
    cols = 4; rows = (len(ims) + cols - 1) // cols
    S = Image.new('RGB', (cols * W // 3, rows * H // 3))
    for i, im in enumerate(ims): S.paste(im, ((i % cols) * W // 3, (i // cols) * H // 3))
    S.save(out, quality=88); print(out)


def render(cfg, out, tmp):
    os.makedirs(tmp, exist_ok=True); W, H = cfg['size']; parts = []
    for i, ((t, src, st, w), n) in enumerate(zip(cfg['shots'], frames(cfg))):
        p = os.path.join(tmp, f's{i:02d}.mp4'); parts.append(p)
        vf = f'fps={FPS},scale={W}:{H}:flags=lanczos,{GRADE},setsar=1' + _text(cfg, w)
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{st:.3f}', '-i', src, '-frames:v', str(n), '-an', '-vf', vf,
                        '-c:v', 'libx264', '-crf', '10', '-preset', 'fast', '-pix_fmt', 'yuv420p', p], check=True)
    lst = os.path.join(tmp, 'list.txt'); open(lst, 'w').write(''.join(f"file '{p}'\n" for p in parts))
    vid = os.path.join(tmp, 'video.mp4')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', lst, '-c', 'copy', vid], check=True)
    extra = ''.join(_text(cfg, w, a, b) for a, b, w in cfg.get('words', []))
    end = cfg['end']
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', vid, '-ss', f"{cfg['off']:.3f}", '-i', cfg['song'],
                    '-filter_complex', f"[0:v]null{extra}[v];[1:a]atrim=0:{end:.3f},afade=t=out:st={end - 0.6:.3f}:d=0.6[a]",
                    '-map', '[v]', '-map', '[a]', '-t', f'{end:.3f}', '-c:v', 'libx264', '-crf', '10', '-preset', 'slow',
                    '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '256k', out], check=True)
    print(out)


def run(cfg, name, argv):
    S = os.environ.get('SCRATCH', '/tmp')
    mode = argv[1] if len(argv) > 1 else 'render'
    if mode == 'check':
        check(cfg)
    elif mode == 'stills':
        check(cfg); stills(cfg, os.path.join(S, 'qc', f'{name}_stills.jpg'))
    else:
        check(cfg); render(cfg, os.path.join(S, 'out', f'{name}.mp4'), os.path.join(S, f'tmp_{name}'))
