"""BP - F1: the 3rd (morning, 08:00 Lagos) post of each day, Nov 11-15 2026 (Desmond's 3-a-day test). Line -> drop edits
(engine/linedrop.py) from formula1.com clips NOT used in the Sao Paulo week yet (commentary timed by whisper, n/words.json):
  alonso   Wed 11  "It's the members of the 400 Club... amazing commitment around the outside" -> AROUND THE OUTSIDE. (#162)
  piastri  Thu 12  "Instant overtake for Max Verstappen, not hanging around" -> INSTANT. (#161)
  p12      Fri 13  "Cover your eyes, Fred Vasseur. Ferrari on Ferrari on lap 9" -> FERRARI ON FERRARI. (#163)
Usage: python3 edit_bp_morning_week.py <name> [...]   (DEX_FPS=50 for YouTube). Clips live in $SCRATCH/n (yt-dlp, Brightcove ids)."""
import os, sys, glob, json
sys.path.insert(0, os.path.dirname(__file__))
import linedrop

S = os.environ.get('SCRATCH', '/tmp')
SONGS = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'dex-edits-assets', 'songs')
song = lambda n: glob.glob(os.path.join(SONGS, n + '_*.mp3'))[0]
N = os.path.join(S, 'n'); WJ = os.path.join(N, 'words.json')
FIX = {"STAPPEN'S": "VERSTAPPEN'S", 'PIAZ': 'PIASTRI', '-STREET.': 'PIASTRI.', '-STREET': 'PIASTRI', 'BUSSER.': 'VASSEUR.', 'HAMILTON!': 'HAMILTON.'}
HANG = {'SO', 'THE', 'A', 'AN', 'AND', 'OF', 'TO', 'IN', 'IS', 'HE', "HE'S", 'FROM', 'FOR', 'BUT', 'WITH', 'AT', 'ON', 'IT'}


def words(key, talk):
    """1-3 word caption lines from whisper words inside each talk span of clip `key`."""
    W = json.load(open(WJ))[key]; out = []
    for k, a, b, *_ in talk:
        line = []
        for s, e, w in W:
            if a - 0.02 <= s <= b - 0.08:
                w = FIX.get(w.upper(), w.upper())
                if not line: out.append((k, max(s, a), '|' + w)); line = [w]
                else: out.append((k, s, w)); line.append(w)
                if (len(line) >= 3 and w.strip('.,?!') not in HANG) or w[-1] in '.,?!': line = []
    return out


def files(clip):
    return {'c': os.path.join(N, clip + '.mp4'), 'r': os.path.join(S, 'bra', 'race.mp4')}


BASE = dict(size=(1088, 612), cap=(46, 0.8), shake=True, crop='crop=1088:612:176:54', crop_keys=['r'], grade='pop',
            fade=2.6, fade_curve='hsin', vfade=1.2, hold=1.8)   # no outro here: a long smooth half-sine fade (qsin stays loud then drops = 'cut off')
CFG = {
    'alonso': dict(clip='alonso', song=song('162'), drop=8.0, beat=60 / 123, big=('AROUND THE OUTSIDE.', 2),
        talk=[('c', 0.0, 5.40, 0, 'c', 0.65), ('c', 6.00, 10.95, 0)],   # cold open: the voice over Alonso's onboard
        after=[(2, 'r', 283.10, 284.95), (4, 'c', 10.78, 12.73, 0.5)]),
    'piastri': dict(clip='piastri', song=song('161'), drop=7.0, beat=60 / 136, big=('INSTANT.', 2),
        talk=[('c', 0.0, 5.42, 0, 'c', 1.70)], ttail=0.08,   # whole phrase 'Instant overtake for Max Verstappen'; cold open on the close side-by-side
        after=[(2, 'c', 8.00, 9.90), (2, 'c', 12.00, 13.90), (2, 'c', 20.00, 21.90), (2, 'c', 24.00, 25.90), (4, 'c', 36.00, 40.00, 0.6)]),
    'p12': dict(clip='p12', song=song('163'), drop=15.0, beat=60 / 108, big=('FERRARI ON FERRARI.', 2),
        talk=[('c', 0.0, 4.55, 0, 'c', 44.00)], ttail=0.12,   # cold open: the voice over the close front shot
        after=[(2, 'c', 21.00, 23.00), (2, 'c', 24.00, 26.00), (2, 'c', 32.00, 34.00), (2, 'c', 36.00, 38.00), (3, 'c', 48.60, 50.39, 0.45)]),
}

if __name__ == '__main__':
    fps = int(os.environ.get('DEX_FPS', 30))
    for name in sys.argv[1:]:
        c = dict(CFG[name]); clip = c.pop('clip')
        cfg = dict(BASE, **c, name=name, fps=fps, files=files(clip))
        cfg['words'] = words('c' if False else clip, cfg['talk'])
        out, drop, end = linedrop.render(cfg, S, os.path.join(S, 'out', f'bp_{name}_{fps}.mp4'))
        print(out, f'drop {drop:.2f} end {end:.2f}', flush=True)
