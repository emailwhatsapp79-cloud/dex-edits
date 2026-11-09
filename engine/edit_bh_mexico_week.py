"""BH - F1, Mexico City GP week (Nov 1 2026), four "line -> drop" edits (engine/linedrop.py), official formula1.com footage:
  max       Wed 18:00  race commentary "side by side, the two Ferraris" + Max: "they made it difficult for themselves, fighting
                       each other, and that's why I could -" CAPITALIZE (drop, Funk Mada #11) -> lap 1, the restart, the contact
  lindblad  Thu 12:00  Lindblad: "he was stuck behind me for over 10 laps... I wasn't just going to let him drive around the
                       outside of me" EASILY (drop, Oya-sa funk #06) -> the crash with Piastri
  hamilton  Thu 18:00  "for the first time since 2023, Lewis Hamilton is on Grand Prix pole. His first Grand Prix pole for"
                       FERRARI (drop, Funk Unico #13) -> Ferrari celebrates; outro, Lewis: "all the questions people have about a
                       40-year-old... still got it. There you go."
  italy     Fri 18:00  "No one has ever won it this young. And at last, Ascari has his" HEIR (drop, Party Funk #31) -> Kimi's
                       final laps and the celebration; outro "Italy's 73-year wait is over."
Usage: python3 edit_bh_mexico_week.py <name> [...]  (DEX_FPS=50 for the YouTube master; the source is 50 fps)."""
import os, sys, glob
sys.path.insert(0, os.path.dirname(__file__))
import linedrop

S = os.environ.get('SCRATCH', '/tmp')
M = os.environ.get('DEX_MEX', os.path.join(S, 'mex'))
SONGS = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'dex-edits-assets', 'songs')
song = lambda n: glob.glob(os.path.join(SONGS, n + '_*.mp3'))[0]
FILES = {k: os.path.join(M, k + '.mp4') for k in ('race', 'maxwin', 'quali', 'qend', 'hampole', 'lindint', 'lindcrash', 'season60', 'bologna')}
BASE = dict(size=(1280, 720), files=FILES, cap=(46, 0.8))

CFG = {
    'max': dict(BASE, song=song('11'), drop=13.0, beat=0.7895, crop='crop=1070:602:105:118',   # lap 1 box off, 1.2x
        talk=[('race', 24.80, 30.40, 0), ('maxwin', 26.55, 30.52, 0)],
        words=[('race', 24.80, '|SIDE BY SIDE,'), ('race', 25.90, 'THE TWO FERRARIS'), ('race', 26.70, 'FOR THE LEAD.'),
               ('maxwin', 26.62, '|I DO THINK'), ('maxwin', 27.42, 'THEY MADE IT'), ('maxwin', 27.74, 'A LITTLE BIT DIFFICULT'),
               ('maxwin', 28.18, 'FOR THEMSELVES,'), ('maxwin', 29.06, '|FIGHTING EACH OTHER'), ('maxwin', 29.70, '|AND THAT\'S WHY'),
               ('maxwin', 30.28, 'I COULD')],
        big=('CAPITALIZE.', 2),
        after=[(1, 'race', 15.10, 19.84), (1, 'race', 19.90, 23.88), (1, 'race', 33.10, 41.84), (1, 'race', 37.00, 41.84),
               (1, 'race', 44.70, 51.72), (1, 'race', 47.60, 51.72), (1, 'race', 51.75, 57.32), (1, 'race', 232.70, 235.76),
               (1, 'race', 236.90, 240.98), (1, 'race', 241.00, 245.06), (2, 'race', 245.10, 252.54)]),
    'lindblad': dict(BASE, song=song('06'), drop=13.5, beat=0.8333,
        talk=[('lindint', 15.80, 19.40, 0), ('lindint', 21.85, 26.14, 0)],
        words=[('lindint', 15.88, '|WE WERE IN A GENUINE FIGHT'), ('lindint', 17.30, '|HE WAS STUCK BEHIND ME'),
               ('lindint', 18.14, 'FOR OVER 10 LAPS'), ('lindint', 21.92, '|I WAS COMMITTED'), ('lindint', 22.60, 'TO FIGHTING'),
               ('lindint', 23.44, 'FOR THAT POSITION'), ('lindint', 24.32, '|I WASN\'T JUST GOING TO LET HIM'),
               ('lindint', 25.20, '|DRIVE AROUND THE OUTSIDE'), ('lindint', 25.86, 'OF ME')],
        big=('EASILY.', 2),
        after=[(1, 'lindcrash', 0.10, 1.40), (1, 'lindcrash', 1.00, 3.40), (1, 'lindcrash', 1.85, 3.40), (1, 'lindcrash', 3.40, 7.00),
               (2, 'lindcrash', 4.25, 7.00)],
        hits=[(3, 0.35)]),
    'hamilton': dict(BASE, song=song('13'), drop=21.293, beat=0.6275,
        talk=[('quali', 402.60, 411.45, 0), ('quali', 412.60, 415.10, 0)],
        words=[('quali', 402.62, '|BUT HEAR THIS,'), ('quali', 403.58, '|FOR THE FIRST TIME'), ('quali', 405.22, 'SINCE 2023.'),
               ('quali', 407.88, '|LEWIS HAMILTON'), ('quali', 409.02, 'IS ON'), ('quali', 410.06, 'GRAND PRIX POLE.'),
               ('quali', 412.66, '|HIS FIRST'), ('quali', 413.26, 'GRAND PRIX POLE'), ('quali', 414.66, 'FOR')],
        big=('FERRARI.', 2),
        after=[(2, 'qend', 25.10, 32.24), (1, 'qend', 33.00, 79.00), (1, 'race', 160.10, 162.28), (1, 'qend', 45.00, 79.00),
               (1, 'race', 163.00, 173.16), (1, 'race', 168.00, 173.16), (1, 'race', 227.60, 232.66), (1, 'race', 232.70, 235.76),
               (1, 'qend', 38.00, 79.00), (1, 'qend', 72.00, 79.00)],   # no F1 logo wipe, no results table
        outro=('hampole', 106.95, 110.95, [('hampole', 106.98, '|ALL THE QUESTIONS PEOPLE HAVE'),
                                           ('hampole', 107.94, '|ABOUT A 40-YEAR-OLD,'), ('hampole', 109.46, '|STILL GOT IT.'),
                                           ('hampole', 110.56, '|THERE YOU GO.')])),
    'italy': dict(BASE, song=song('31'), drop=6.0, beat=0.93,
        talk=[('race', 387.35, 389.35, 0), ('race', 398.90, 401.86, 0)],
        words=[('race', 387.42, '|NO ONE HAS EVER WON IT'), ('race', 389.02, 'THIS YOUNG.'), ('race', 398.98, '|AND AT LAST,'),
               ('race', 400.18, '|ASCARI'), ('race', 400.94, 'HAS HIS')],
        big=('HEIR.', 2),
        after=[(1, 'race', 416.95, 437.68), (1, 'race', 410.55, 416.92), (1, 'race', 430.00, 437.68), (1, 'season60', 54.14, 55.24),
               (1, 'race', 441.85, 465.68), (1, 'race', 452.00, 465.68), (2, 'race', 472.15, 475.16)],
        outro=('race', 423.85, 428.15, [('race', 423.90, '|ITALY\'S 73-YEAR WAIT'), ('race', 426.20, 'IS OVER.')])),
    # Fri 12:00 - TOP 10 ONBOARD, Mexico: a cut every 2 beats on Brutus (#112, 144 bpm), no talk - the cars do the talking
    'onboard': dict(BASE, song=song('112'), drop=0.42, beat=0.8333, talk=[], words=[], big=('MEXICO. ONBOARD.', 2),
        files=dict(FILES, onboard10=os.path.join(M, 'onboard10.mp4')),
        after=[(1, 'onboard10', o, e) for o, e in [(0.05, 1.44), (2.40, 5.14), (5.20, 8.18), (14.00, 15.04), (17.00, 20.72),
               (22.00, 27.64), (30.00, 38.00), (41.45, 43.00), (43.05, 45.84), (50.00, 58.52), (64.00, 68.24), (69.00, 73.40),
               (85.00, 97.44), (100.00, 126.98), (128.00, 136.20), (145.00, 158.20), (165.00, 172.76), (175.00, 179.24),
               (185.00, 205.72), (240.00, 260.12), (265.00, 283.12), (290.00, 315.24), (345.00, 363.90)]]),
}

if __name__ == '__main__':
    fps = int(os.environ.get('DEX_FPS', 30))
    for name in sys.argv[1:]:
        cfg = dict(CFG[name], name=name, fps=fps)
        out, drop, end = linedrop.render(cfg, S, os.path.join(S, 'out', f'bh_{name}_{fps}.mp4'))
        print(out, f'drop {drop:.2f} end {end:.2f}')
