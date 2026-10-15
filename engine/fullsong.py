"""Find the FULL song behind every short TikTok sound in the library (Desmond: "isn't there a way to get the whole
song" - most edits should not need the sound repeated).

    python3 engine/fullsong.py [NN ...]        # library numbers; default: all

For each sound: (1) identify it with Shazam (shazamio), (2) search SoundCloud for "title artist" (yt-dlp scsearch),
(3) download the candidates, (4) VERIFY by audio: the TikTok clip must be found inside the full track (onset-envelope
cross-correlation, also tried at the slowed/sped-up speeds TikTok sounds often use). Only a verified match is kept:
<ASSETS>/songs/full/NN_slug.mp3, with the offset where the TikTok clip starts. Results -> songs/FULL.md (public repo:
names/links/offsets only, never audio)."""
import os, re, sys, json, glob, asyncio, subprocess, tempfile
import numpy as np

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.environ.get('DEX_ASSETS', '/home/user/dex-edits-assets')
NAMED, FULL = os.path.join(ASSETS, 'songs'), os.path.join(ASSETS, 'songs', 'full')
REPORT = os.path.join(REPO, 'songs', 'FULL.md')
SR, HOP = 11025, 256


def shazam(path):
    from shazamio import Shazam
    async def go():
        r = await Shazam().recognize(path)
        t = r.get('track') or {}
        return t.get('title'), t.get('subtitle')
    try: return asyncio.run(go())
    except Exception: return None, None


def onset(path, offset=0.0, dur=None):
    import librosa
    y, _ = librosa.load(path, sr=SR, offset=offset, duration=dur)
    o = librosa.onset.onset_strength(y=y, sr=SR, hop_length=HOP)
    return (o - o.mean()) / (o.std() + 1e-9)


def locate(clip, full):
    """Best normalised correlation of the clip's onset envelope inside the full track, over playback speeds."""
    import librosa
    yc, _ = librosa.load(clip, sr=SR, duration=12)
    best = (0.0, 0.0, 1.0)
    f = onset(full)
    for speed in (1.0, 0.8, 0.85, 0.9, 1.1, 1.15, 1.2, 1.25):
        yy = librosa.effects.time_stretch(yc, rate=1 / speed) if speed != 1.0 else yc   # clip at the track's speed
        c = librosa.onset.onset_strength(y=yy, sr=SR, hop_length=HOP); c = (c - c.mean()) / (c.std() + 1e-9)
        if len(c) >= len(f): continue
        corr = np.correlate(f, c, 'valid') / len(c)
        k = int(np.argmax(corr))
        if corr[k] > best[0]: best = (float(corr[k]), k * HOP / SR, speed)
    return best   # (score, offset seconds in full track, speed of the TikTok clip relative to the track)


def candidates(query, n=4):
    r = subprocess.run(['yt-dlp', '-q', '--no-warnings', '--flat-playlist', '--print', '%(url)s\t%(title)s [%(uploader)s]\t%(duration)s',
                        f'scsearch{n}:{query}'], capture_output=True, text=True, timeout=120)
    out = []
    for line in r.stdout.strip().splitlines():
        p = line.split('\t')
        if len(p) == 3: out.append((p[0], p[1], float(p[2]) if p[2] not in ('NA', 'None', '') else 0.0))
    return out


def same_song(title, artist, sc_title):
    """The SoundCloud result must carry the song title and (one word of) the artist - stops look-alike tracks."""
    n = lambda x: re.sub(r'[^a-z0-9 ]', ' ', (x or '').lower())
    t, a, s = n(title), n(artist), n(sc_title)
    t_ok = all(w in s.split() for w in t.split()[:3] if len(w) > 1)
    a_ok = any(w in s for w in a.replace(' x ', ' ').split() if len(w) > 3) if a.strip() else True
    return t_ok, a_ok


def chroma_check(clip, full, off, speed):
    """Melody check: chroma of the clip vs the full track at the found offset (cosine similarity, 0..1)."""
    import librosa
    yc, _ = librosa.load(clip, sr=SR, duration=10)
    if speed != 1.0: yc = librosa.effects.time_stretch(yc, rate=1 / speed)
    yf, _ = librosa.load(full, sr=SR, offset=max(0, off), duration=len(yc) / SR)
    a = librosa.feature.chroma_cqt(y=yc, sr=SR, hop_length=1024); b = librosa.feature.chroma_cqt(y=yf, sr=SR, hop_length=1024)
    m = min(a.shape[1], b.shape[1]); a, b = a[:, :m].flatten(), b[:, :m].flatten()
    return float(a @ b / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-9))


def fetch(url, dst):
    subprocess.run(['yt-dlp', '-q', '--no-warnings', '-x', '--audio-format', 'mp3', '--audio-quality', '0',
                    '-o', dst.replace('.mp3', '.%(ext)s'), url], capture_output=True, timeout=300)
    return dst if os.path.exists(dst) else None


def one(clip):
    name = os.path.basename(clip).rsplit('.', 1)[0]
    wav = os.path.join(tempfile.mkdtemp(), 'clip.wav')                     # librosa can't read every container
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', clip, '-ac', '1', '-ar', str(SR), wav], check=True)
    clip_dur = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', clip],
                                    capture_output=True, text=True).stdout or 0)
    title, artist = shazam(wav)
    res = dict(sound=name, clip=round(clip_dur, 1), title=title, artist=artist, status='not identified')
    if not title: return res
    res['status'] = 'identified, no full track found'
    tmp = tempfile.mkdtemp()
    for q in (f'{title} {artist}', title):
        for url, sc_title, dur in candidates(q):
            if dur and dur < clip_dur + 15: continue                         # previews / snippets
            t_ok, a_ok = same_song(title, artist, sc_title)
            if not t_ok: continue
            p = fetch(url, os.path.join(tmp, f'c{abs(hash(url)) % 10**8}.mp3'))
            if not p: continue
            score, off, speed = locate(wav, p)
            chroma = chroma_check(wav, p, off, speed) if score > 0.45 else 0.0
            if (a_ok and score > 0.45 and chroma > 0.75) or (score > 0.7 and chroma > 0.85) or (score > 0.95 and chroma > 0.8):
                os.makedirs(FULL, exist_ok=True)
                dst = os.path.join(FULL, name + '.mp3'); os.replace(p, dst)
                res.update(status='FULL', full_title=sc_title, url=url, full_dur=round(dur, 1), score=round(score, 2), chroma=round(chroma, 2),
                           offset=round(off, 2), speed=speed)
                return res
        if res['status'] == 'FULL': break
    return res


def report(rows):
    lines = ['# Full songs behind the TikTok sounds', '',
             'Made by `engine/fullsong.py`. Audio lives in the private repo (`dex-edits-assets/songs/full/`). '
             '`offset` = where the TikTok clip starts inside the full song; `speed` = TikTok clip speed vs the full track '
             '(e.g. 0.85 = the TikTok sound is a slowed version).', '',
             '| sound | clip | identified as | status | full track | length | match | offset | speed |',
             '|---|---|---|---|---|---|---|---|---|']
    for r in rows:
        lines.append(f"| {r['sound']} | {r['clip']}s | {r.get('title') or '-'} – {r.get('artist') or ''} | {r['status']} | "
                     f"{r.get('full_title', '')} | {r.get('full_dur', '')} | {r.get('score', '')} | {r.get('offset', '')} | {r.get('speed', '')} |")
    open(REPORT, 'w').write('\n'.join(lines) + '\n')


if __name__ == '__main__':
    clips = sorted(glob.glob(os.path.join(NAMED, '*.*')))
    clips = [c for c in clips if re.match(r'\d+_', os.path.basename(c)) and not os.path.isdir(c)]
    if len(sys.argv) > 1:
        want = {int(a) for a in sys.argv[1:]}
        clips = [c for c in clips if int(os.path.basename(c).split('_')[0]) in want]
    rows = []
    for c in clips:
        r = one(c); rows.append(r); print(json.dumps(r, ensure_ascii=False), flush=True)
    report(rows)
