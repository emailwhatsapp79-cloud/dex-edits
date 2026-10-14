"""Save the sound of every edit Desmond sends into the song library.

    python3 engine/add_sound.py <tiktok/instagram link or local video> [...]

For each input: download (yt-dlp), extract the audio to <ASSETS>/songs/named/NN_slug.mp3, analyse it (tempo,
length, biggest energy jump = the drop, strongest drum hits, lyrics with word timings) and append a row to
songs/LIBRARY.md plus a lyric line, and a stub to REFERENCES.md (link, creator, caption). Sounds already in the
library (same TikTok music id or same title) are not added twice.
The audio goes to the PRIVATE repo dex-edits-assets (DEX_ASSETS) and is committed + pushed there; it is never
committed to this public repo (copyright)."""
import os, re, sys, json, glob, subprocess
import numpy as np

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.environ.get('DEX_ASSETS', '/home/user/dex-edits-assets')       # PRIVATE repo with the audio
NAMED = os.path.join(ASSETS, 'songs')
WORK = os.environ.get('DEX_WORK', '/tmp/claude-0/-home-user-scamdecoded-media/7be1f147-2656-5ce6-9a44-2202ae528a61/scratchpad')
LIB = os.path.join(REPO, 'songs', 'LIBRARY.md')
REFS = os.path.join(REPO, 'REFERENCES.md')
sys.path.insert(0, os.path.dirname(__file__))


def slugify(s, n=40):
    s = re.sub(r'[^a-z0-9]+', '_', s.lower()).strip('_')
    return s[:n] or 'sound'


def fetch(src, workdir):
    """Return (video_path, info dict)."""
    if os.path.exists(src):
        return src, {'title': os.path.basename(src), 'webpage_url': src}
    os.makedirs(workdir, exist_ok=True)
    tmpl = os.path.join(workdir, '%(id)s.%(ext)s')
    for _ in range(3):
        r = subprocess.run(['yt-dlp', '-q', '--no-warnings', '--write-info-json', '-o', tmpl, src], capture_output=True, text=True)
        js = sorted(glob.glob(os.path.join(workdir, '*.info.json')), key=os.path.getmtime)
        if r.returncode == 0 and js:
            info = json.load(open(js[-1])); vid = js[-1].replace('.info.json', '.mp4')
            if not os.path.exists(vid): vid = glob.glob(js[-1].replace('.info.json', '.*'))[0]
            return vid, info
    raise RuntimeError(f'download failed: {src}\n{r.stderr[-400:]}')


def analyse(audio):
    import librosa
    from beatsync import grid, hits
    y, sr = librosa.load(audio, sr=22050)
    dur = len(y) / sr
    win = int(0.5 * sr); rms = np.array([np.sqrt(np.mean(y[i:i + win] ** 2)) for i in range(0, len(y) - win, win)])
    jump = np.argmax(rms[2:] - rms[:-2]) + 2 if len(rms) > 3 else 0
    drop = jump * 0.5
    g, tempo = grid(audio)
    strong = sorted(hits(audio, min_strength=0.6), key=lambda h: -h[1])[:6]
    try:
        from faster_whisper import WhisperModel
        raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', audio, '-ac', '1', '-ar', '16000', '-f', 'f32le', '-'], capture_output=True).stdout
        segs, _ = WhisperModel('small', device='cpu', compute_type='int8').transcribe(np.frombuffer(raw, np.float32), word_timestamps=True)
        words = [(w.start, w.word.strip()) for s in segs for w in s.words]
    except Exception as e:
        words = []
    return dict(dur=dur, tempo=float(tempo), drop=drop, strong=sorted(round(h[0], 3) for h in strong), words=words)


def next_number():
    nums = [int(m) for m in re.findall(r'^\| (\d+) \|', open(LIB).read(), re.M)]
    return max(nums) + 1 if nums else 1


def add(src):
    title = None
    if '::' in src: src, title = src.split('::', 1)                       # local file::Title of the sound
    vid, info = fetch(src, os.path.join(WORK, 'refs_auto'))
    if title: info['title'] = info['track'] = title
    track = info.get('track') or info.get('title') or 'sound'
    artist = info.get('artist') or info.get('uploader') or ''
    lib = open(LIB).read()
    key = f"{track} – {artist}".strip(' –')
    norm = lambda x: re.sub(r'[^a-z0-9]', '', x.lower())
    generic = track.lower().startswith(('original sound', 'son original', 'som original', 'eredeti hang', 'sonido original', 'originalton', 'suono originale', 'son d.origine'))
    probe = norm(track + artist) if generic else norm(track)[:18]
    if track != 'sound' and probe and probe in norm(lib):
        print(f'already in library: {key}'); return None
    n = next_number(); name = f'{n:02d}_{slugify(track + "_" + artist if generic else track)}'
    os.makedirs(NAMED, exist_ok=True)
    mp3 = os.path.join(NAMED, name + '.mp3')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', vid, '-vn', '-c:a', 'libmp3lame', '-b:a', '256k', mp3], check=True)
    a = analyse(mp3)
    creator = info.get('uploader') or info.get('channel') or ''
    caption = (info.get('description') or info.get('title') or '').replace('|', '/').replace('\n', ' ')[:90]
    row = (f"| {n} | {name} | \"{track} – {artist}\" (from @{creator}: {caption}) | {a['tempo']:.0f} | {a['dur']:.1f}s | "
           f"biggest energy jump (drop) ≈ {a['drop']:.1f}s · strongest hits {' '.join(f'{x:.2f}' for x in a['strong'])} · added automatically |")
    lines = lib.split('\n')
    last = max(i for i, l in enumerate(lines) if re.match(r'^\| \d+ \|', l))
    lines.insert(last + 1, row)
    lib = '\n'.join(lines)
    if a['words']:
        lib = lib.rstrip('\n') + f"\n\n**{name}:** " + ' '.join(f'`{t:.2f}` {w}' for t, w in a['words']) + '\n'
    open(LIB, 'w').write(lib)
    with open(REFS, 'a') as fh:
        fh.write(f"\n| auto | {info.get('webpage_url', src)} | @{creator}: {caption} | sound saved as library #{n} ({a['tempo']:.0f} BPM, drop ≈ {a['drop']:.1f}s) |")
    print(f'added #{n} {name}: {a["tempo"]:.0f} BPM, {a["dur"]:.1f}s, drop ≈ {a["drop"]:.1f}s, {len(a["words"])} words')
    return name


def push_assets(names):
    if not names or not os.path.isdir(os.path.join(ASSETS, '.git')): return
    subprocess.run(['git', '-C', ASSETS, 'add', 'songs'], check=True)
    subprocess.run(['git', '-C', ASSETS, 'commit', '-q', '-m', 'Add sounds: ' + ', '.join(names)], check=True)
    r = subprocess.run(['git', '-C', ASSETS, 'push', '-q', 'origin', 'HEAD'], capture_output=True, text=True)
    print('assets pushed' if r.returncode == 0 else 'assets push FAILED: ' + r.stderr[-300:])


if __name__ == '__main__':
    added = []
    for s in sys.argv[1:]:
        try:
            n = add(s)
            if n: added.append(n)
        except Exception as e: print('FAILED', s, e)
    push_assets(added)
