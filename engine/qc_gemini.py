"""Second opinion from Gemini on finished edits (Desmond, Nov 9: "send it to Gemini to check also"). Each video is shrunk
to 540x960 (~3-5 MB, the free key takes inline video under ~20 MB) and Gemini watches it like a strict editor:
a FULL review - hook, story, sound/drop, pace, picture, graphics, text, emotion, ending, viral potential, top 3 fixes, score.
The key is a network secret injected by the proxy (header x-goog-api-key) - never in code.
usage: python3 qc_gemini.py <video.mp4> [...]   -> prints Gemini's verdict per video (VERDICT: PASS/FAIL)"""
import sys, os, json, base64, subprocess, tempfile, time

URL = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent'
PROMPT = """You are a strict, experienced short-form editor reviewing an F1 fan edit (TikTok / YouTube Short) BEFORE it is
posted. Watch and LISTEN to the whole video, second by second. Give a FULL analysis, briefly, with timestamps:
1) HOOK (0-2 s): is the first frame action or the most dramatic moment? Would a scroller stop? What would make it stronger?
2) STORY & DIRECTION: what is the story in one line? Is it clear from start to finish? Does it build to a payoff?
3) SOUND: does the song fit the mood? Is the drop on the payoff word/moment? Commentary/voice levels vs music - clear?
   Any word or line chopped mid-word or mid-sentence?
4) EDITING & PACE: are cuts on the beat? Any shot too long, too short, repeated, or confusing? Shakes/effects - too much?
5) PICTURE: every shot sharp? any blurry/soft/frozen/black/empty/grey shot? any F1 logo wipe, 'LAP xx' card, results table,
   F1's own subtitles or other graphics that look out of place?
6) ON-SCREEN TEXT: readable? matches what is said? well timed? style - would one big word per cut look better?
7) EMOTION / PASSION: does it make you feel something (hype, sadness, joy)? where does the energy dip?
8) ENDING: does it end on a complete moment (celebration/podium/payoff held, last word finished, music fades), or does it
   feel cut off / end on a talking head too suddenly?
9) VIRAL POTENTIAL: would F1 fans like/comment/share? What comment would they write?
10) TOP 3 FIXES, most important first.
SCORE: x/10
Last line exactly: VERDICT: PASS or VERDICT: FAIL (FAIL if anything in 3, 5 or 8 is a real problem, or SCORE < 7)."""


def ask(path):
    small = tempfile.mktemp(suffix='.mp4')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', path, '-vf', 'scale=540:-2', '-r', '25', '-c:v', 'libx264', '-crf', '30',
                    '-preset', 'fast', '-c:a', 'aac', '-b:a', '96k', small], check=True, stdin=subprocess.DEVNULL)
    body = {'contents': [{'parts': [{'inline_data': {'mime_type': 'video/mp4', 'data': base64.b64encode(open(small, 'rb').read()).decode()}},
                                    {'text': PROMPT}]}]}
    os.remove(small)
    req = tempfile.mktemp(suffix='.json'); open(req, 'w').write(json.dumps(body))
    try:
        for i in range(6):
            r = subprocess.run(['curl', '-s', '-X', 'POST', '-H', 'Content-Type: application/json', '--data-binary', '@' + req, URL],
                               capture_output=True, text=True)
            try: j = json.loads(r.stdout)
            except Exception: j = {}
            if 'candidates' in j: return j['candidates'][0]['content']['parts'][0]['text']
            time.sleep(15 * (i + 1))
        return 'Gemini unavailable: ' + r.stdout[:200]
    finally:
        os.remove(req)


if __name__ == '__main__':
    for p in sys.argv[1:]:
        print(f'===== {os.path.basename(p)}\n{ask(p)}\n', flush=True)
