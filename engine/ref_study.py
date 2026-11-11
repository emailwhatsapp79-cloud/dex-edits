"""Study a REFERENCE edit with Gemini (Desmond, Nov 11: "get a good analysis ... use Gemini ... every single detail").
Runs four focused passes on the video (shot-by-shot timeline | audio | text/graphics/colour | strategy + recipe) and writes
them to <out_dir>/gemini_<pass>.txt. The key is a network secret injected by the proxy (header x-goog-api-key) - never in code.
usage: python3 ref_study.py <video.mp4> <out_dir> [context line]"""
import sys, os, json, base64, subprocess, tempfile, time

MODELS = ['gemini-3-flash-preview', 'gemini-2.5-flash', 'gemini-2.5-flash-lite']
URL = 'https://generativelanguage.googleapis.com/v1beta/models/{}:generateContent'
BASE = ("You are a senior short-form video editor analysing a viral reference edit (TikTok). Watch AND listen to the whole video "
        "carefully, second by second. Be exact: use timestamps (m:ss.s), quote on-screen words and spoken words exactly, say "
        "'not sure' when unsure instead of guessing. {ctx}\n\n")
PASSES = {
 'timeline': "TASK: SHOT-BY-SHOT TIMELINE. For EVERY cut give: start time, duration, what is shown (subject, shot type: wide/close/onboard/crowd/"
             "archive; era/year/driver if recognisable), camera motion, any speed change (slow-mo/ramp), zoom, shake, flash, glitch, colour tint, "
             "the transition into the next shot, and the on-screen text word at that moment. Then give totals: number of cuts, average shot length "
             "for 0-10 s, 10-16 s, 16-35 s, 35-end; which shots are archive/older-era footage vs current.",
 'audio': "TASK: AUDIO ANALYSIS. (1) The music: genre, mood, tempo (bpm), instruments, where it starts, where it DROPS, any build-up, any "
          "recognisable song/remix (say not sure if unsure). (2) Spoken words: exact transcript with timestamps, who speaks (commentator? film "
          "clip?), and which movie/scene any dialogue comes from. (3) Sound effects: every SFX with timestamp (hits, whooshes, snaps, drum, "
          "crowd, engines). (4) Silences and volume dips: when and why. (5) How cuts and caption words sync to the beat/voice: on the beat, "
          "on the word, off-beat? (6) The ending: how the audio finishes (fade, cut, loop). (7) Is the audio clean, loud, balanced?",
 'visual': "TASK: TEXT, GRAPHICS AND LOOK. (1) On-screen text: font style, weight, italic?, colours, outline/shadow, size, position, the "
           "exact words and the animation (pop, slide, scale, per-letter, partial word), timing vs speech. (2) Watermarks / credits (exact text, "
           "position, when). (3) Colour grade per section (warm/cool/saturated/dark), contrast, vignette, grain, sharpness. (4) Frame format: "
           "aspect ratio, borders, letterbox, resolution feel, any zoom crop. (5) Effects list with timestamps (shake, flash, RGB split, blur, "
           "speed ramps, freeze). (6) The movie clip in the middle (what it is, how it is graded and cropped, why it works here).",
 'strategy': "TASK: STRATEGY AND RECIPE. This video has 610k views, 150k likes (24% like rate), 12k shares, 514 comments in 8 days; the creator "
             "normally gets far fewer. (1) The hook (0-3 s): exactly what makes a scroller stay. (2) The structure in acts with timestamps and "
             "the emotional arc. (3) Why people like/share/comment: name the specific triggers. (4) The 3 boldest editing choices. (5) What is "
             "weak or risky. (6) A step-by-step RECIPE to make an F1 edit with the same effect for a NEW race weekend: target length, number of "
             "acts and their timings, how many shots, shot lengths, caption rules, how to use a movie clip, music plan, ending. (7) What we must "
             "NOT copy (rights, repetition, other creator's brand).",
}


def ask(path, prompt):
    small = tempfile.mktemp(suffix='.mp4')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', path, '-vf', 'scale=960:-2', '-r', '30', '-c:v', 'libx264', '-crf', '29',
                    '-preset', 'fast', '-c:a', 'aac', '-b:a', '112k', small], check=True, stdin=subprocess.DEVNULL)
    body = {'contents': [{'parts': [{'inline_data': {'mime_type': 'video/mp4', 'data': base64.b64encode(open(small, 'rb').read()).decode()}},
                                    {'text': prompt}]}]}
    os.remove(small)
    req = tempfile.mktemp(suffix='.json'); open(req, 'w').write(json.dumps(body))
    try:
        for i in range(6):
            for m in MODELS:
                r = subprocess.run(['curl', '-s', '-X', 'POST', '-H', 'Content-Type: application/json', '--data-binary', '@' + req,
                                    URL.format(m)], capture_output=True, text=True)
                try: j = json.loads(r.stdout)
                except Exception: j = {}
                if 'candidates' in j: return f'[{m}]\n' + j['candidates'][0]['content']['parts'][0]['text']
            time.sleep(30 * (i + 1))
        return 'Gemini unavailable: ' + r.stdout[:300]
    finally:
        os.remove(req)


if __name__ == '__main__':
    video, out = sys.argv[1], sys.argv[2]; ctx = sys.argv[3] if len(sys.argv) > 3 else ''
    os.makedirs(out, exist_ok=True)
    for i, (name, task) in enumerate(PASSES.items()):
        if i: time.sleep(65)
        txt = ask(video, BASE.format(ctx=ctx) + task)
        open(os.path.join(out, f'gemini_{name}.txt'), 'w').write(txt)
        print(f'== {name}: {len(txt)} chars', flush=True)
