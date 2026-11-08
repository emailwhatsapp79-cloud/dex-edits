"""BO - F1: the Sao Paulo GP week (Nov 10-13 2026), eight line -> drop edits (engine/linedrop.py) from the official race
highlights, commentary words timed by whisper (bra/words.json, auto-grouped into 1-3 word lines):
  kimi      Tue 12  "He loses it. Kimi Antonelli from the lead... spins at turn one, and Lando Norris leads." -> #167 "I'm so sad"
  mercedes  Tue 18  "Mercedes, for the first time in five years, have won it all. Mercedes are the world" CHAMPIONS. (#166)
  hamilton  Wed 12  "How can Hamilton be there? He's up 11 places... but he is." -> UP 11 PLACES. (#163) -> "Heart in mouth"
  lawson    Wed 18  "Lawson down the inside... a point to prove, hasn't he?" -> POINT PROVEN. (#165, moment raw)
  russell   Thu 12  "Round goes Russell... a nightmare position... he scrapes down the barrier" -> #167 again (sad)
  hulk      Thu 18  "the Audi man is checking the mirror... Hulkenberg keeps his foot in and takes the place" DELICIOUS. (#162)
  overtakes Fri 12  "It is an overtaking montage in Interlagos." -> ten passes on the beat (#161 What's up)
  leclerc   Fri 18  "Charles Leclerc became a father in the week..." -> "taking seventh position" -> DAD MODE. (#13)
Usage: python3 edit_bo_brazil_week.py <name> [...]   (DEX_FPS=50 for YouTube)."""
import os, sys, glob, json
sys.path.insert(0, os.path.dirname(__file__))
import linedrop

S = os.environ.get('SCRATCH', '/tmp')
B = os.path.join(S, 'bra')
SONGS = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'dex-edits-assets', 'songs')
song = lambda n: glob.glob(os.path.join(SONGS, n + '_*.mp3'))[0]
FILES = {'r': os.path.join(B, 'race.mp4'), 'm': os.path.join(B, 'mercs.mp4')}
WJ = os.path.join(B, 'words.json')


def words(talk):
    """1-3 word caption lines from whisper words inside each talk span (a new line at punctuation or after 3 words)."""
    W = json.load(open(WJ)); out = []
    src = {'r': W['race'], 'm': W['mercs']}
    for k, a, b, *_ in talk:
        line = []
        for s, e, w in src[k]:
            if a - 0.02 <= s <= b - 0.08:
                w = w.upper()
                if not line: out.append((k, max(s, a), '|' + w)); line = [w]
                else: out.append((k, s, w)); line.append(w)
                if len(line) == 3 or w[-1] in '.,?!': line = []
    return out


BASE = dict(size=(1280, 720), files=FILES, cap=(46, 0.6), shake=True)
CFG = {
    'kimi': dict(song=song('167'), drop=0.0, beat=60 / 98, big=('SO VERY, VERY SAD.', 4),
        talk=[('r', 227.10, 230.40, 0), ('r', 231.35, 235.05, 0, 'r', 230.30)],
        after=[(2, 'r', 7.00, 10.30), (2, 'r', 210.50, 211.88), (2, 'r', 254.20, 257.26), (2, 'r', 268.40, 270.54),
               (2, 'r', 240.00, 249.30), (2, 'r', 208.50, 211.88)]),
    'mercedes': dict(song=song('166'), drop=3.0, beat=60 / 130, big=('CHAMPIONS.', 2), files=FILES,
        talk=[('m', 0.00, 3.95, 0), ('m', 4.55, 6.75, 0)],
        after=[(2, 'r', 447.00, 460.60), (2, 'r', 7.50, 10.30), (2, 'r', 242.00, 249.30), (2, 'm', 32.95, 34.45),
               (2, 'r', 480.70, 482.84)]),
    'hamilton': dict(song=song('163'), drop=15.0, beat=60 / 108, big=('UP 11 PLACES.', 2),
        talk=[('r', 44.50, 48.70, 0), ('r', 48.95, 51.40, 0)],
        after=[(2, 'r', 53.80, 70.98), (2, 'r', 55.90, 70.98), (2, 'r', 59.40, 70.98), (2, 'r', 61.60, 66.00)],
        outro=('r', 335.00, 337.40, [('r', 335.06, '|OH, MY WORD.'), ('r', 336.06, '|HEART IN MOUTH'), ('r', 336.74, 'FOR HAMILTON.')])),
    'lawson': dict(song=song('165'), drop=13.0, beat=60 / 126, big=('POINT PROVEN.', 2), intro_song=0.0,
        talk=[('r', 17.30, 20.95, 0), ('r', 35.70, 40.70, 0)],
        after=[(2, 'r', 7.00, 10.30), (2, 'r', 114.00, 121.00), (2, 'r', 116.60, 121.00), (2, 'r', 381.40, 387.80),
               (2, 'r', 399.40, 404.00)]),
    'russell': dict(song=song('167'), drop=0.0, beat=60 / 98, big=('NIGHTMARE.', 4),
        talk=[('r', 178.70, 183.85, 0), ('r', 193.40, 194.30, 0)],
        after=[(2, 'r', 162.50, 164.00), (2, 'r', 188.50, 191.46), (2, 'r', 196.00, 202.60), (2, 'r', 199.50, 202.60)]),
    'hulk': dict(song=song('162'), drop=8.0, beat=60 / 123, big=('DELICIOUS.', 2),
        talk=[('r', 364.30, 371.70, 0)],
        after=[(2, 'r', 345.00, 366.56), (2, 'r', 350.00, 366.56), (2, 'r', 356.00, 366.56), (2, 'r', 361.00, 366.56)]),
    'overtakes': dict(song=song('161'), drop=7.0, beat=60 / 136, big=('OVERTAKES.', 2),
        talk=[('r', 156.30, 159.95, 0)],
        after=[(2, 'r', 17.50, 22.24), (2, 'r', 46.00, 48.20), (2, 'r', 59.50, 70.98), (2, 'r', 73.00, 74.84),
               (2, 'r', 88.00, 89.78), (2, 'r', 107.00, 108.08), (2, 'r', 153.00, 164.00), (2, 'r', 291.00, 305.68),
               (2, 'r', 370.00, 371.76), (2, 'r', 411.00, 413.36)]),
    'leclerc': dict(song=song('13'), drop=21.293, beat=0.6275, big=('DAD MODE.', 2),
        talk=[('r', 374.40, 377.80, 0), ('r', 410.00, 414.10, 0)],
        after=[(2, 'r', 380.50, 387.80), (2, 'r', 388.00, 390.12), (2, 'r', 405.00, 408.00), (2, 'r', 417.00, 423.10)]),
}

if __name__ == '__main__':
    fps = int(os.environ.get('DEX_FPS', 30))
    for name in sys.argv[1:]:
        cfg = dict(BASE, **CFG[name], name=name, fps=fps)
        cfg['words'] = words(cfg['talk'])
        out, drop, end = linedrop.render(cfg, S, os.path.join(S, 'out', f'bo_{name}_{fps}.mp4'))
        print(out, f'drop {drop:.2f} end {end:.2f}', flush=True)
