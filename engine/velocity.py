"""Velocity-edit engine: per-shot speed ramps on motion-interpolated footage, cuts snapped to drum hits, 60 fps."""
import os, subprocess, math, json
from concurrent.futures import ThreadPoolExecutor
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

W, H, FPS, IFPS = 1080, 1920, 60, 100          # output size/fps, interpolated source fps


def speed_fn(mode):
    if mode == 'slow':
        return lambda u: 0.4
    if mode == 'hero':
        return lambda u: 0.28
    if mode == 'real':
        return lambda u: 1.0
    # velocity: lands slow right after the hit, whips up to fast into the next hit
    return lambda u: 0.28 + (2.7 - 0.28) * (u ** 2.2)


def src_needed(mode, dur):
    f = speed_fn(mode); n = 400
    return dur * sum(f((i + .5) / n) for i in range(n)) / n


def prep(shots, srcdir, tmpdir, src_w=1920, src_h=1080, prescale=False):
    """Cut each shot's source span, crop to vertical, motion-interpolate to IFPS. Returns paths."""
    os.makedirs(tmpdir, exist_ok=True)
    cw = int(round(src_h * 9 / 16)) // 2 * 2
    def job(i):
        sh = shots[i]
        need = src_needed(sh['mode'], sh['t1'] - sh['t0']) + 0.15
        new = clean_span(os.path.join(srcdir, sh['file']), sh['src'], need)
        if abs(new - sh['src']) > 1e-3:
            print(f"shot {i}: src {sh['src']:.2f} -> {new:.2f} (avoids a cut in the source)", flush=True)
            sh['src'] = new
        out = os.path.join(tmpdir, f"shot{i:02d}_{sh['src']:.2f}_{sh['mode']}.mp4")
        if os.path.exists(out): return out
        x = int((src_w - cw) * sh.get('cx', 0.5))
        pre = 'scale=1080:1920:flags=lanczos,' if prescale else ''
        vf = f"crop={cw}:{src_h}:{x}:0,{pre}minterpolate=fps={IFPS}:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1"
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(sh['src']), '-t', f'{need:.3f}', '-i',
                        os.path.join(srcdir, sh['file']), '-vf', vf, '-an', '-c:v', 'libx264', '-crf', '14',
                        '-preset', 'veryfast', out], check=True)
        return out
    with ThreadPoolExecutor(4) as ex:
        return list(ex.map(job, range(len(shots))))


class Seq:
    """Sequential frame access into an interpolated clip, scaled to W x H."""
    def __init__(self, path):
        self.p = subprocess.Popen(['ffmpeg', '-v', 'error', '-i', path, '-vf', f'scale={W}:{H}:flags=lanczos,unsharp=5:5:0.7',
                                   '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
        self.buf = []; self.idx = -1

    def get(self, i):
        while self.idx < i:
            b = self.p.stdout.read(W * H * 3)
            if len(b) < W * H * 3: break
            self.idx += 1
            self.buf.append(np.frombuffer(b, np.uint8).reshape(H, W, 3))
            if len(self.buf) > 10: self.buf.pop(0)
        k = max(0, len(self.buf) - 1 - max(0, self.idx - i))
        return self.buf[k] if self.buf else np.zeros((H, W, 3), np.uint8)

    def close(self):
        self.p.kill()


def frame_for(seq, mode, lt, dur):
    """Source position for local time lt using the speed curve; blur frames when moving fast."""
    f = speed_fn(mode); n = 60
    u = lt / dur
    pos = dur * sum(f((k + .5) / n * u) for k in range(n)) / n * u if u > 0 else 0.0
    i = int(pos * IFPS)
    sp = f(u)
    if sp > 1.4:   # shutter blur: average the frames this output frame spans
        span = max(2, int(sp * IFPS / FPS))
        acc = np.zeros((H, W, 3), np.float32)
        for k in range(span): acc += seq.get(i + k)
        return acc / span / 255
    return seq.get(i).astype(np.float32) / 255


def cut_frames(cuts):
    """Frame index where each cut lands: the frame that contains the hit (never late)."""
    return [int(math.floor(c * FPS + 1e-6)) for c in cuts]


_scene = {}
DETECTOR = 'hist'          # 'hist' (race footage, soft cuts) or 'scene' (cinematic films with lens flares)


def source_cuts(path):
    """Hard cuts inside a source film (cached)."""
    if DETECTOR == 'scene' and ('scene', path) not in _scene:
        import re
        r = subprocess.run(['ffmpeg', '-i', path, '-vf', "scale=160:-1,select='gt(scene,0.22)',showinfo", '-f', 'null', '-'],
                           capture_output=True, text=True).stderr
        _scene[('scene', path)] = sorted(float(x) for x in re.findall(r'pts_time:([0-9.]+)', r))
    if DETECTOR == 'scene': return _scene[('scene', path)]
    if path not in _scene:
        fps = 25.0
        p = subprocess.run(['ffmpeg', '-v', 'error', '-i', path, '-vf', f'fps={fps},scale=96:54,format=gray', '-f', 'rawvideo', '-'],
                           capture_output=True)
        fr = np.frombuffer(p.stdout, np.uint8).reshape(-1, 54, 96).astype(np.float32)
        d = np.abs(np.diff(fr, axis=0)).mean(axis=(1, 2))
        h = [np.histogram(f, 16, (0, 255))[0] for f in fr]
        hd = np.array([np.abs(h[i + 1] - h[i]).sum() / (96 * 54) for i in range(len(h) - 1)])
        det = [(i + 1) / fps for i in range(len(d)) if (d[i] > 18 and hd[i] > 0.22) or hd[i] > 0.45]
        # a real cut is a single-frame jump; runs of detections are flares, flashes or fast pans
        _scene[path] = [c for c in det if not any(0 < abs(c - o) < 0.09 for o in det)]
    return _scene[path]


def clean_span(path, src, need, margin=0.03):
    """Move src so [src, src+need] holds no source cut: first try just after the offending cut,
    then just before it. Returns the new src."""
    cuts = source_cuts(path)
    bad = [c for c in cuts if src - margin < c < src + need + margin]
    if not bad: return src
    after = bad[-1] + margin
    if not [c for c in cuts if after < c < after + need + margin]: return after
    before = bad[0] - need - margin
    if before > 0 and not [c for c in cuts if before - margin < c < before + need + margin]: return before
    raise ValueError(f'no clean {need:.2f}s span near {src:.2f} in {os.path.basename(path)} - use a slower mode or another take')
