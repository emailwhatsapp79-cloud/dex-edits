"""Second opinion from Gemini on finished edits (Desmond, Nov 9: "send it to Gemini to check also"). Each video is shrunk
to 540x960 (~3-5 MB, the free key takes inline video under ~20 MB) and Gemini watches it like a strict editor:
cut-off endings, cut-off words, F1 graphics/logos/LAP cards/captions, blur, wrong shots, story direction, a score.
The key is a network secret injected by the proxy (header x-goog-api-key) - never in code.
usage: python3 qc_gemini.py <video.mp4> [...]   -> prints Gemini's verdict per video (VERDICT: PASS/FAIL)"""
import sys, os, json, base64, subprocess, tempfile, time

URL = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent'
PROMPT = """You are a strict editor checking a short F1 fan edit (TikTok/YouTube Short) before it is posted. Watch and LISTEN
to the whole video. Answer briefly:
1) ENDING: does the video end cleanly? Is the last spoken word complete and is the sentence finished? Is there at least
   half a second after the last word? Does any celebration or moment get cut off before it finishes?
2) CUT-OFF WORDS anywhere: any commentary or voice line that is chopped mid-word or mid-sentence (give timestamps)?
3) GRAPHICS: any official F1 logo wipe, 'LAP xx' card, results table, F1's own subtitles/captions, or other broadcast
   graphics that look out of place (timestamps)?
4) PICTURE: any blurry, soft, frozen, black or grey/empty shot (timestamps)?
5) STORY: in one line, what is the story? Is the direction clear? Do the on-screen words match what is said?
6) SCORE 1-10 for how ready it is to post, and the single most important fix.
Last line exactly: VERDICT: PASS or VERDICT: FAIL (FAIL if anything in 1-4 is a real problem)."""


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
