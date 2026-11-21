"""DA - MotoGP PORTIMAO 2026 QUALIFYING (Sat 21 Nov evening, made by the CLOUD session while the PC was off).
Story: Bezzecchi takes Marc Marquez's three-year-old all-time Portimao lap record "by a whisker" (1:37.201) and knocks Marc
down to second on the grid, the day the title can be decided. NOV 17 rules: ~20 s, payoff title on frame 1, two commentary
runs (never chopped), beat outro + end card.
  1 "Is this an all-time lap record coming in from Marco Bezzecchi? Is he going to take the three-year-old all-time lap
     record? He does by a whisker."   (picture: the lap crossing the line, FASTEST, the Aprilia garage)
  2 "He knocks Marc Marquez back down to second on the grid as it stands right now, and he takes away Marc's three-year-old
     2023 all-time lap record to boot."   (picture: aerial + trackside, the wheelie)
Sources (motogp.com, free, 1080p50): 'Last 5 mins: Bezzecchi blazes to record-breaking pole' (1266837) = last5,
'Onboard: ride with Bezzecchi on his record-breaking lap at Portimao' (1266932) = onboard.
Song: #162 Funk Loading (slowed). Usage: SRC=<folder with last5.mp4 + onboard.mp4> SCRATCH=<dir> python3 <this>"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import master

S = os.environ.get('SCRATCH', '/tmp')
SRC = os.environ['SRC']
ASSETS = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'dex-edits-assets')
C = 'crop=1080:1080:420:0'
FILES = {'l': (os.path.join(SRC, 'last5.mp4'), C), 'o': (os.path.join(SRC, 'onboard.mp4'), C)}
W1 = [(210.25, 'IS THIS AN ALL-TIME LAP RECORD'), (211.43, 'COMING IN FROM MARCO BEZZECCHI?'), (213.13, 'IS HE GOING TO TAKE'),
      (213.73, 'THE THREE-YEAR-OLD'), (214.25, 'ALL-TIME LAP RECORD?'), (215.81, 'HE DOES'), (216.25, 'BY A WHISKER.')]
W2 = [(228.91, 'HE KNOCKS MARC MARQUEZ'), (229.65, 'BACK DOWN TO SECOND ON THE GRID'), (231.07, 'AS IT STANDS RIGHT NOW'),
      (232.17, 'AND HE TAKES AWAY'), (233.63, "MARC'S THREE-YEAR-OLD"), (235.29, '2023 ALL-TIME LAP RECORD'),
      (237.73, 'TO BOOT.')]
CFG = dict(name='bez_portimao_record', files=FILES, song=os.path.join(ASSETS, 'songs', '162_funk_loading_slowed.mp3'),
           song_in=8.0, title="PORTIMAO QUALIFYING|BEZZECCHI BREAKS MARC'S RECORD", banner_in=0.0,
           segments=[dict(type='voice', k='l', a=210.2, b=217.6, words=W1, pic=('l', 213.0)),
                     dict(type='voice', k='l', a=228.85, b=238.3, words=W2, pic=('l', 226.0)),
                     dict(type='outro', shots=[('o', 16.0), ('o', 36.0), ('o', 100.0), ('o', 112.0), ('l', 223.6)])])

if __name__ == '__main__':
    fps = int(os.environ.get('DEX_FPS', 25))
    out, total = master.render(dict(CFG, fps=fps), S, os.path.join(S, 'out', f'da_bez_portimao_record_{fps}.mp4'))
    print(out, f'total {total:.1f}s', flush=True)
    import look; look.yt1440(out, out.replace('.mp4', '_yt1440.mp4'))
