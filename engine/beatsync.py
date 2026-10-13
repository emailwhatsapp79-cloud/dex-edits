"""Beat-sync toolkit.
hits(audio)    -> precise drum-hit times (kick/snare transients from the percussive part), with strength.
measure(video) -> every hard cut in a rendered video vs the nearest drum hit; prints errors."""
import subprocess, sys, json
import numpy as np, librosa

SR = 44100


def load(path, sr=SR, offset=0.0, duration=None):
    cmd = ['ffmpeg', '-v', 'error', '-ss', str(offset), '-i', path]
    if duration: cmd += ['-t', str(duration)]
    b = subprocess.run(cmd + ['-vn', '-ac', '1', '-ar', str(sr), '-f', 'f32le', '-'], capture_output=True).stdout
    return np.frombuffer(b, np.float32).copy()


def hits(path, offset=0.0, duration=None, min_strength=0.25):
    """Return [(time, strength, band)] of percussive transients. Times are sample-accurate (refined to the
    attack: the point where energy rises fastest), relative to `offset`."""
    y = load(path, offset=offset, duration=duration)
    perc = librosa.effects.percussive(y, margin=3.0)
    hop = 128
    S = np.abs(librosa.stft(perc, n_fft=1024, hop_length=hop))
    fr = librosa.fft_frequencies(sr=SR, n_fft=1024)
    out = []
    for band, (lo, hi) in {'kick': (30, 150), 'snare': (150, 5000)}.items():
        env = librosa.onset.onset_strength(S=librosa.amplitude_to_db(S[(fr >= lo) & (fr < hi)]), sr=SR, hop_length=hop)
        env = env / (env.max() + 1e-9)
        pk = librosa.util.peak_pick(env, pre_max=6, post_max=6, pre_avg=20, post_avg=20, delta=0.08, wait=20)
        for p in pk:
            if env[p] < min_strength: continue
            # refine: steepest rise of the raw amplitude envelope within +-10 ms
            t0 = p * hop / SR; a, b = int((t0 - 0.012) * SR), int((t0 + 0.012) * SR)
            seg = np.abs(perc[max(a, 0):b]);
            if len(seg) > 32:
                sm = np.convolve(seg, np.ones(32) / 32, 'same'); d = np.diff(sm)
                t0 = (max(a, 0) + int(np.argmax(d))) / SR
            out.append((round(t0, 4), round(float(env[p]), 3), band))
    out.sort()
    # merge kick+snare hits closer than 25 ms (keep strongest)
    merged = []
    for h in out:
        if merged and h[0] - merged[-1][0] < 0.025:
            if h[1] > merged[-1][1]: merged[-1] = h
        else:
            merged.append(h)
    return merged


def video_cuts(path, fps):
    """Frame-accurate hard cuts (big frame-to-frame change), returns times of the first new frame."""
    p = subprocess.run(['ffmpeg', '-v', 'error', '-i', path, '-vf', 'scale=96:170,format=gray', '-f', 'rawvideo', '-'],
                       capture_output=True)
    fr = np.frombuffer(p.stdout, np.uint8).reshape(-1, 170, 96).astype(np.float32)
    d = np.abs(np.diff(fr, axis=0)).mean(axis=(1, 2))
    h = [np.histogram(f, 16, (0, 255))[0] for f in fr]
    hd = np.array([np.abs(h[i + 1] - h[i]).sum() / (96 * 170) for i in range(len(h) - 1)])
    cuts = [(i + 1) / fps for i in range(len(d)) if (d[i] > 28 and hd[i] > 0.35) or hd[i] > 0.6]
    # drop cuts within 3 frames of the previous (flash frames)
    keep = []
    for c in cuts:
        if not keep or c - keep[-1] > 3.5 / fps: keep.append(c)
    return keep


def measure(video, fps, audio=None, label=''):
    audio = audio or video
    hs = hits(audio)
    ht = np.array([h[0] for h in hs])
    cuts = video_cuts(video, fps)
    errs = []
    for c in cuts:
        j = np.argmin(np.abs(ht - c)); errs.append(c - ht[j])
    errs = np.array(errs)
    on = np.abs(errs) <= 1.0 / fps + 0.002
    print(f'{label}: {len(cuts)} cuts | mean |err| {np.abs(errs).mean()*1000:.0f} ms | max {np.abs(errs).max()*1000:.0f} ms | '
          f'within 1 frame: {on.sum()}/{len(cuts)}')
    return cuts, errs


if __name__ == '__main__':
    measure(sys.argv[1], float(sys.argv[2]), label=sys.argv[1].split('/')[-1])


def grid(path, offset=0.0, duration=None, window=0.07):
    """Musical beat grid snapped to real transients: [(time, accent 0..1)].
    Beats come from the tracker (regular), each one moved to the strongest percussive attack within
    +-window; accent = how hard that hit is relative to the loudest in the song."""
    y = load(path, offset=offset, duration=duration)
    perc = librosa.effects.percussive(y, margin=3.0)
    hop = 128
    env = librosa.onset.onset_strength(y=perc, sr=SR, hop_length=hop)
    tempo, beats = librosa.beat.beat_track(onset_envelope=env, sr=SR, hop_length=hop, units='frames', tightness=100)
    hs = hits(path, offset, duration, min_strength=0.05)
    ht = np.array([h[0] for h in hs]); hsn = np.array([h[1] for h in hs])
    rms = librosa.feature.rms(y=perc, frame_length=1024, hop_length=hop)[0]
    out = []
    for b in beats:
        t = b * hop / SR
        m = np.abs(ht - t) <= window
        if m.any():
            idx = np.where(m)[0][np.argmax(hsn[m])]; t = ht[idx]
        i = int(t * SR / hop)
        out.append([round(float(t), 4), float(rms[i:i + 8].max()) if i < len(rms) else 0.0])
    mx = max(a for _, a in out) or 1
    return [(t, round(a / mx, 3)) for t, a in out], float(np.atleast_1d(tempo)[0])
