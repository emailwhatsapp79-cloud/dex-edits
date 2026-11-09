"""QC the ENDING of finished edits (Desmond, Nov 9: "some were still cut off"): whisper the last 12 s and report the last
word and how much picture is left after it. FAIL if the last word ends less than 0.7 s before the end of the file, or
the last word has no full stop (a sentence that does not finish).
usage: python3 qc_end.py <video.mp4> [...]"""
import sys, subprocess, tempfile, os
import soundfile as sf
from faster_whisper import WhisperModel

m = WhisperModel('small', compute_type='int8')
bad = 0
for f in sys.argv[1:]:
    wav = tempfile.mktemp(suffix='.wav')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-sseof', '-12', '-i', f, '-vn', '-ac', '1', '-ar', '16000', wav], check=True)
    a, sr = sf.read(wav, dtype='float32'); os.remove(wav); L = len(a) / sr
    ws = [w for s in m.transcribe(a, word_timestamps=True)[0] for w in s.words]
    if not ws: print(f'OK   {os.path.basename(f)}: no speech at the end (music ending)'); continue
    last = ws[-1]; gap = L - last.end; txt = ' '.join(w.word.strip() for w in ws[-6:])
    ok = gap >= 0.7 and last.word.strip()[-1:] in '.!?'
    bad += not ok
    print(f"{'OK  ' if ok else 'FAIL'} {os.path.basename(f)}: '...{txt}'  {gap:.2f} s after the last word")
sys.exit(1 if bad else 0)
