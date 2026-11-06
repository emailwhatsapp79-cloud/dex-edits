"""BI - F1: "WHAT'S UP, BRAZIL" - the drivers arrive at Interlagos (Sao Paulo GP week, Nov 2026) on the trending sound #161
("What's up? / in a minute", ref X1). Every driver looks / waves / laughs into the lens; a cut every 2 beats; a short mild
camera SHAKE on every cut (ref X1). Frame 1 = Kimi waving at the camera. Footage: formula1.com "Driver arrivals" (official,
1280x720 50 fps); shake = a 0.95 crop moving on each hit, back to 1280x720 (1.05x, sharp).
Usage: python3 edit_bi_brazil_arrivals.py  (DEX_FPS=50 for YouTube) -> horizontal master; vertical via ytshort.py."""
import os, sys, glob, subprocess
sys.path.insert(0, os.path.dirname(__file__))
import wmtext

S = os.environ.get('SCRATCH', '/tmp')
SRC = os.path.join(S, 'bra', 'arrivals.mp4')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SONG = glob.glob(os.path.join(os.path.dirname(ROOT), 'dex-edits-assets', 'songs', '161_*.mp3'))[0]
FPS = int(os.environ.get('DEX_FPS', 30))
W, H = 1280, 720
GRADE = 'eq=contrast=1.06:saturation=1.10'
CUTS = [0, 0.95, 1.86, 2.74, 3.65, 4.55, 5.46, 6.34, 7.24, 8.13, 9.03, 9.91, 10.82, 11.73, 12.62]   # every 2 beats (136 bpm)
END = 14.0
SHOTS = [(9.20, 10.52), (10.55, 11.96), (12.00, 13.34), (13.36, 14.68), (23.10, 24.46), (21.75, 23.08), (18.40, 20.34),
         (25.20, 27.26), (27.30, 28.64), (30.40, 32.86), (38.50, 39.84), (40.00, 41.24), (44.05, 45.42), (49.65, 51.02),
         (15.20, 17.50)]                                          # (in, take end), each take once
WORDS = [(0.0, 0.93, "WHAT'S UP,"), (12.62, END, 'BRAZIL.')]


def shake_expr(hits, amp, f, phase):
    terms = [f"between(t,{h:.3f},{h + 0.28:.3f})*{amp}*sin(2*PI*{f}*(t-{h:.3f})+{phase})*(1-(t-{h:.3f})/0.28)" for h in hits]
    return '+'.join(terms)


def render(out):
    tmp = os.path.join(S, 'tmp_bi'); os.makedirs(tmp, exist_ok=True)
    bounds = CUTS + [END]; parts = []
    for i, (s, e) in enumerate(SHOTS):
        d = bounds[i + 1] - bounds[i]
        assert s + d <= e + 0.03, f'shot {i} runs past its take ({s + d:.2f} > {e})'
        n = round(bounds[i + 1] * FPS) - round(bounds[i] * FPS); p = os.path.join(tmp, f's{i:02d}.mp4'); parts.append(p)
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{s:.3f}', '-i', SRC, '-frames:v', str(n), '-an', '-vf',
                        f'fps={FPS},{GRADE},setsar=1', '-c:v', 'libx264', '-crf', '10', '-preset', 'fast', '-pix_fmt', 'yuv420p', p], check=True)
    lst = os.path.join(tmp, 'list.txt'); open(lst, 'w').write(''.join(f"file '{x}'\n" for x in parts))
    vid = os.path.join(tmp, 'video.mp4')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', lst, '-c', 'copy', vid], check=True)
    cw, ch = int(W * 0.95) // 2 * 2, int(H * 0.95) // 2 * 2
    mx, my = (W - cw) // 2, (H - ch) // 2
    xs = f"{mx}+{shake_expr(CUTS, 22, 18, 0)}"; ys = f"{my}+{shake_expr(CUTS, 14, 23, 1.3)}"
    shake = f"crop={cw}:{ch}:'{xs}':'{ys}',scale={W}:{H}:flags=lanczos,setsar=1"
    pngs = [wmtext.word_png(w, W, H, os.path.join(tmp, f'w{i}.png'), size=int(H * 0.13)) for i, (_, _, w) in enumerate(WORDS)]
    cmd = ['ffmpeg', '-v', 'error', '-y', '-i', vid, '-i', SONG]
    for p in pngs: cmd += ['-loop', '1', '-framerate', str(FPS), '-t', f'{END:.3f}', '-i', p]
    chain, last = wmtext.overlay_filter(WORDS, 2, '[sh]')
    fc = f"[0:v]{shake}[sh];" + chain + f"[1:a]atrim=0:{END:.3f},afade=t=out:st={END - 0.35:.3f}:d=0.35[a]"
    subprocess.run(cmd + ['-filter_complex', fc, '-map', last, '-map', '[a]', '-t', f'{END:.3f}', '-r', str(FPS),
                          '-c:v', 'libx264', '-crf', '10', '-preset', 'slow', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '256k', out], check=True)
    print(out)


if __name__ == '__main__':
    render(os.path.join(S, 'out', f'bi_arrivals_{FPS}.mp4'))
