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
# v2 (Desmond: "multiple bikes, not one person", "the song is too moody"): packs and battles only, no faces/celebrations
SHOTS = [(B, 9.0, 980), (A, 10.0, 1400), (A, 170.0, 980), (B, 63.0, 920), (A, 420.0, 960), (A, 620.0, 860)]
CFG = dict(name='portimao_mood', shots=SHOTS, song=os.path.join(ASSETS, 'songs', 'full', '05_montagem_kali_slowed.mp3'),
           song_in=13.0, every=4, slow=0.5)   # bass-heavy instrumental ~136 BPM like AE1-AE5

if __name__ == '__main__':
    fps = int(os.environ.get('DEX_FPS', 25))
    out, total = mood.render(dict(CFG, fps=fps), S, os.path.join(S, 'out', f'dc_portimao_mood_{fps}.mp4'))
    print(out, f'total {total:.1f}s', flush=True)
