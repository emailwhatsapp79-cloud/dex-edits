"""Action-on-the-beat (Desmond, Oct 23-24, ref K1 @kam_cuts): the HIT inside a shot - punch contact, muzzle flash,
sword slash, foot stomp, impact, a car passing the lens - must land on the music event, not only the cut.

peaks(path, t0, t1)            -> action-peak times in a source window (motion spikes + brightness flashes, per frame)
events(song, off, t0, t1)      -> audio events (onsets) in the edit timeline
fit(path, cut_t, dur, events, search=(a, b))
                               -> best source in-point so the shot's action peaks land on the events inside
                                  [cut_t, cut_t + dur]; returns (src_t, hits, n_peaks, errors_ms)
Usage in an edit: for each shot give a search window in the source; fit() picks the in-point frame-exactly."""
import subprocess, sys
import numpy as np, librosa

FPS = 30


def _frames(path, t0, t1, w=160, h=90):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{t0:.3f}', '-i', path, '-t', f'{t1 - t0:.3f}', '-vf',
                          f'fps={FPS},scale={w}:{h},format=gray', '-f', 'rawvideo', '-'], capture_output=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(-1, h, w).astype(np.float32)


def curve(path, t0, t1):
    """Per-frame action score: motion (frame difference) + positive brightness jumps (flashes, sparks, explosions)."""
    f = _frames(path, t0, t1)
    if len(f) < 3: return np.zeros(len(f)), t0
    mot = np.r_[0, np.abs(np.diff(f, axis=0)).mean(axis=(1, 2))]
    lum = f.mean(axis=(1, 2)); flash = np.r_[0, np.clip(np.diff(lum), 0, None)]
    z = lambda v: (v - np.median(v)) / (np.std(v) + 1e-6)
    return z(mot) + 1.5 * z(flash), t0


def peaks(path, t0, t1, k=1.2):
    c, base = curve(path, t0, t1)
    idx = [i for i in range(1, len(c) - 1) if c[i] > k and c[i] >= c[i - 1] and c[i] >= c[i + 1]]
    return [base + i / FPS for i in idx], c


def events(song, off, t0, t1, delta=0.25):
    sys.path.insert(0, __import__('os').path.dirname(__file__)); import beatsync
    sr = 22050; y = beatsync.load(song, sr=sr, offset=off)
    o = librosa.onset.onset_detect(y=y, sr=sr, units='time', delta=delta)
    return [float(x) for x in o if t0 <= x < t1]


def fit(path, cut_t, dur, evs, search, tol=1.0 / FPS):
    """Slide the in-point over `search` (source seconds) frame by frame; score = events met by an action peak (±1 frame),
    tie-break on total peak strength at the events. Returns (src_t, met, n_events, errors_ms)."""
    ev = [e - cut_t for e in evs if cut_t <= e < cut_t + dur]
    a, b = search
    c, base = curve(path, a, b + dur)
    best = None
    for s in range(0, max(1, int((b - a) * FPS))):
        win = c[s:s + int(round(dur * FPS))]
        if len(win) < 2: break
        pk = [i / FPS for i in range(1, len(win) - 1) if win[i] > 1.2 and win[i] >= win[i - 1] and win[i] >= win[i + 1]]
        met, err, strength = 0, [], 0.0
        for e in ev:
            if pk:
                d = min(pk, key=lambda p: abs(p - e))
                if abs(d - e) <= tol: met += 1; err.append(round((d - e) * 1000)); strength += win[int(round(d * FPS))]
        key = (met, strength)
        if best is None or key > best[0]: best = (key, a + s / FPS, met, err)
    return round(best[1], 3), best[2], len(ev), best[3]


if __name__ == '__main__':
    # quick report: python3 actionsync.py <video> <t0> <t1>
    p, t0, t1 = sys.argv[1], float(sys.argv[2]), float(sys.argv[3])
    pk, _ = peaks(p, t0, t1)
    print('action peaks:', ' '.join(f'{x:.3f}' for x in pk))
