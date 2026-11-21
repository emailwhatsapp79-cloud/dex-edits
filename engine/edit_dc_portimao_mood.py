"""DC - MOTOGP PORTIMAO, MOOD EDIT (Sun 22 Nov 08:00, replaces the race-day card hype - Desmond: "change tomorrow's edit to
this type", refs AE1-AE5). No text, no commentary: full-screen 9:16 slow motion, one cut per bar of Purple Rain's intro,
8 shots that build to the winner - a rider alone on the straight, leans, the flag, Bezzecchi standing on the pegs, his
helmet. ~19 s at 720x1280 (engine/mood.py). Footage: 2025 Portuguese GP (vP51RMuSUsk highlights, EbJMANarkcQ best moments).
Usage: SRC=<sources folder> SCRATCH=<dir> python3 edit_dc_portimao_mood.py"""
import os, sys, glob
sys.path.insert(0, os.path.dirname(__file__))
import mood

S = os.environ.get('SCRATCH', '/tmp')
SRC = os.environ['SRC']
ASSETS = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'dex-edits-assets')
src = lambda vid: glob.glob(os.path.join(SRC, '**', f'*{vid}*.mp4'), recursive=True)[0]
A, B = src('vP51RMuSUsk'), src('EbJMANarkcQ')
SHOTS = [(A, 120.0, 1040), (A, 500.0, 1320), (A, 550.0, 880), (B, 171.0, 880), (A, 640.0, 1120), (B, 213.0, 1600),
         (B, 222.0, 840), (B, 243.0, 1080)]
CFG = dict(name='portimao_mood', shots=SHOTS, song=os.path.join(ASSETS, 'songs', 'trend', 'purple_rain_prince.mp3'),
           song_in=4.0, every=2, slow=0.5)

if __name__ == '__main__':
    fps = int(os.environ.get('DEX_FPS', 25))
    out, total = mood.render(dict(CFG, fps=fps), S, os.path.join(S, 'out', f'dc_portimao_mood_{fps}.mp4'))
    print(out, f'total {total:.1f}s', flush=True)
