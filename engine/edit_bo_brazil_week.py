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
FILES = {k: os.path.join(B, v + '.mp4') for k, v in [('r', 'race'), ('m', 'mercs'), ('li', 'lawint'), ('ai', 'antint'), ('hi', 'hamint2'),
         ('ri', 'rusint'), ('ki', 'hulkint'), ('ld', 'lecdad')]}
WJ = os.path.join(B, 'words.json')


FIX = {'SHARL': 'CHARLES', 'SHARLES': 'CHARLES', 'LECLEC': 'LECLERC', 'LECLERC,': 'LECLERC,', 'ALBANY': 'ALBON', 'ALBANY.': 'ALBON.',
       'HAJAR': 'HADJAR', 'HADJARA': 'HADJAR', 'LIMBLAD': 'LINDBLAD', 'INTELARGOS.': 'INTERLAGOS.', 'INTELAGOS.': 'INTERLAGOS.',
       'HULKENBERG': 'HÜLKENBERG', 'CARSWIT': 'CAR', 'KIMMY': 'KIMI', 'STAPPEN': 'VERSTAPPEN'}
HANG = {'SO', 'THE', 'A', 'AN', 'AND', 'OF', 'TO', 'IN', 'IS', 'HE', 'HE\'S', 'FROM', 'FOR', 'BUT', 'WITH', 'AT', 'ON'}


def words(talk):
    """1-3 word caption lines from whisper words inside each talk span (a new line at punctuation or after 3 words)."""
    W = json.load(open(WJ)); out = []
    src = {'r': W['race'], 'm': W['mercs']}
    for k, a, b, *_ in talk:
        line = []
        for s, e, w in src[k]:
            if a - 0.02 <= s <= b - 0.08:
                w = FIX.get(w.upper(), w.upper())
                if not line: out.append((k, max(s, a), '|' + w)); line = [w]
                else: out.append((k, s, w)); line.append(w)
                if (len(line) >= 3 and w.strip('.,?!') not in HANG) or w[-1] in '.,?!': line = []
    return out


BASE = dict(size=(1280, 720), files=FILES, cap=(46, 0.6), shake=True, crop='crop=1088:612:176:54', crop_keys=['r'])   # end well: last shot >= ~2 s, song fades 1 s
CFG = {
    'kimi': dict(song=song('167'), drop=0.0, beat=60 / 98, big=('SO VERY, VERY SAD.', 4),
        talk=[('r', 228.30, 230.45, 0), ('r', 231.35, 235.05, 0, 'r', 230.30)],
        after=[(2, 'r', 7.00, 10.30), (2, 'r', 210.50, 211.88), (2, 'r', 254.20, 257.26), (2, 'r', 208.50, 211.88),
               (2, 'r', 240.00, 249.30), (3, 'r', 268.40, 270.54)],
        outro=('ai', 11.55, 24.55, [('ai', 11.60, "|I'M EXTREMELY"), ('ai', 13.46, 'DISAPPOINTED'), ('ai', 14.12, 'WITH THE RACE,'),
                                    ('ai', 16.72, "|BUT I'M GOING TO"), ('ai', 17.52, 'PUT IT ASIDE,'), ('ai', 18.92, '|BECAUSE TODAY'),
                                    ('ai', 20.92, '|IS A GREAT DAY'), ('ai', 21.78, 'FOR THE TEAM,'), ('ai', 22.38, '|AND THEY ALL DESERVE IT.')],
               [('r', 255.50, 1.2), ('ai', 12.75, 10.4), ('m', 4.60, 99)])),
    'mercedes': dict(song=song('166'), drop=8.36, song_from=4.8, beat=60 / 130, big=('CHAMPIONS.', 2), files=FILES,
        talk=[('m', 0.00, 3.95, 0), ('m', 4.55, 6.75, 0)],
        after=[(2, 'm', 32.95, 34.45), (2, 'r', 447.00, 460.60), (2, 'r', 242.00, 249.30), (2, 'r', 7.50, 10.30),
               (4, 'r', 480.70, 482.84)]),
    'hamilton': dict(song=song('163'), drop=15.0, beat=60 / 108, big=('UP 11 PLACES.', 2),
        talk=[('r', 44.50, 48.70, 0), ('r', 48.95, 51.40, 0)],
        after=[(2, 'r', 323.60, 343.00), (2, 'r', 325.90, 343.00), (2, 'r', 328.20, 343.00), (2, 'r', 330.50, 343.00)],   # Lewis only: onboard, slicks, the spin
        outro=('hi', 9.84, 14.30, [('hi', 9.86, '|I HAD A GREAT START'), ('hi', 12.66, '|AND I THOUGHT I WAS ON'), ('hi', 13.14, 'FOR SOMETHING POSITIVE.')],
               [('r', 333.00, 1.2), ('hi', 11.04, 1.96), ('r', 336.00, 99)])),
    'lawson': dict(song=song('166'), drop=6.45, song_from=4.8, beat=60 / 130, big=('POINT PROVEN.', 2),
        talk=[('r', 17.30, 20.95, 0), ('r', 35.70, 40.70, 0)],
        after=[(2, 'r', 7.00, 10.30), (2, 'r', 114.00, 121.00), (2, 'r', 116.60, 121.00), (2, 'r', 381.40, 387.80),
               (2, 'r', 399.40, 404.00)],
        words=[('r', 17.32, '|LAWSON'), ('r', 17.70, 'DOWN THE INSIDE,'), ('r', 18.30, '|AND NORRIS,'), ('r', 18.92, "|HE'S UP TO SECOND."),
               ('r', 19.92, '|LAWSON GETS BY.'), ('r', 35.74, '|LAWSON,'), ('r', 36.04, 'SO OPPORTUNISTIC.'), ('r', 37.90, '|BRAVE FROM THIRD.'),
               ('r', 39.30, "|HE'S GOT A POINT"), ('r', 39.90, 'TO PROVE,'), ('r', 40.30, "HASN'T HE?")],
        outro=('li', 43.15, 45.75, [('li', 43.32, '|HONESTLY,'), ('li', 44.00, 'JUST TRYING'), ('li', 44.48, '|TO ENJOY DRIVING'), ('li', 45.10, 'AT THE MOMENT.')],
               [('r', 401.00, 1.2), ('li', 44.35, 0.6), ('r', 118.00, 99)])),
    'russell': dict(song=song('167'), drop=0.0, beat=60 / 98, big=('NIGHTMARE.', 4),
        talk=[('r', 178.70, 183.85, 0), ('r', 193.40, 194.30, 0)],
        after=[(2, 'r', 162.50, 164.00), (2, 'r', 188.50, 191.46), (2, 'r', 196.00, 202.60), (4, 'r', 199.50, 202.60)],
        outro=('ri', 32.45, 38.30, [('ri', 32.50, '|PROBABLY JUST TOOK'), ('ri', 33.56, 'TOO MUCH RISK,'), ('ri', 34.08, '|BECAUSE I WAS SEEING'), ('ri', 35.30, '|AN OPPORTUNITY'), ('ri', 35.78, '|TO GO FOR THE WIN.')],
               [('r', 186.00, 1.2), ('ri', 33.65, 3.25), ('r', 160.00, 99)])),
    'hulk': dict(song=song('162'), drop=8.0, beat=60 / 123, big=('DELICIOUS.', 2),
        talk=[('r', 364.30, 371.70, 0)],
        after=[(2, 'r', 345.00, 366.56), (2, 'r', 351.00, 366.56), (2, 'r', 356.00, 366.56), (4, 'r', 361.00, 366.56)],
        outro=('ki', 14.40, 20.45, [('ki', 14.42, '|IT WAS A GOOD MOVE.'), ('ki', 15.38, '|SET HIM UP A BIT'), ('ki', 16.78, '|ON THE ENTRY FOR THE EXIT'), ('ki', 18.54, '|WITH AN UNDERCUT.')],
               [('r', 353.20, 1.2), ('ki', 15.60, 3.45), ('r', 369.20, 99)])),
    'overtakes': dict(song=song('161'), drop=7.0, beat=60 / 136, big=('OVERTAKES.', 2),
        talk=[('r', 156.30, 159.95, 0)],
        after=[(2, 'r', 17.50, 22.24), (2, 'r', 46.00, 48.20), (2, 'r', 59.50, 70.98), (2, 'r', 73.00, 74.84),
               (2, 'r', 88.00, 89.78), (2, 'r', 107.00, 108.08), (2, 'r', 153.00, 164.00), (2, 'r', 411.00, 413.36),
               (2, 'r', 370.00, 371.76), (6, 'r', 291.00, 305.68)]),
    'leclerc': dict(song=song('13'), drop=21.293, beat=0.6275, big=('DAD MODE.', 2),
        talk=[('r', 374.40, 377.80, 0), ('r', 410.00, 414.10, 0)],
        after=[(2, 'r', 380.50, 387.80), (2, 'r', 388.00, 390.12), (2, 'r', 405.00, 408.00), (4, 'r', 383.40, 387.80)],
        outro=('ld', 24.35, 32.62, [('ld', 24.40, "|IT'S A VERY, VERY"), ('ld', 25.32, 'SPECIAL MOMENT,'), ('ld', 27.96, '|AND DEFINITELY A WEEK'),
                                    ('ld', 30.04, "|I'LL FOREVER REMEMBER"), ('ld', 31.20, '|FOR ALL THE'), ('ld', 31.78, 'POSITIVE REASONS.')],
               [('r', 395.50, 1.2), ('ld', 25.55, 5.75), ('r', 410.90, 99)])),
}

if __name__ == '__main__':
    fps = int(os.environ.get('DEX_FPS', 30))
    for name in sys.argv[1:]:
        cfg = dict(BASE, **CFG[name], name=name, fps=fps)
        cfg['words'] = cfg.get('words') or words(cfg['talk'])
        out, drop, end = linedrop.render(cfg, S, os.path.join(S, 'out', f'bo_{name}_{fps}.mp4'))
        print(out, f'drop {drop:.2f} end {end:.2f}', flush=True)
