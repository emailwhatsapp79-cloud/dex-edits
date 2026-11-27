"""FB01 - FOOTBALL CHANNEL (@dexedits62 / @dexedits-y3y), Fri 27 Nov ~22:00: preview of Arsenal vs Man City (Sun 29, 17:30 Lagos). Hook: 'If you're coming for the king, you best not miss' - Haaland + Grealish at the Emirates 2023. Source: Man City 'ICONIC MOMENTS | Arsenal v Man City' (b_RsmsIUVJo).
NOV 17 rules: 15-20 s, short commentary runs (Content ID: each run < 8 s), beat outro + card."""
import os, sys, glob
sys.path.insert(0, os.path.dirname(__file__))
import master

S = os.environ.get('SCRATCH', '/tmp')
SRC = os.environ['SRC']
ASSETS = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'dex-edits-assets')
src = lambda vid: glob.glob(os.path.join(SRC, '**', f'*{vid}*.mp4'), recursive=True)[0]
FILES = {'a': (src('b_RsmsIUVJo'), 'crop=1080:1080:420:0')}
NAME = 'fb01_arsenal_city_king.py'.replace('.py', '')
CFG = dict(name=NAME, files=FILES, song=os.path.join(ASSETS, 'songs', 'trend', 'bow_bow_bow_zeddy_will.mp3'), song_in=54.45, title="SUNDAY: ARSENAL vs MAN CITY|'IF YOU COME FOR THE KING...'", banner_in=0.2,
           segments=[dict(type='voice', k='a', a=0.7, b=4.45, pic=('a', 589.5), words=[(0.75, "IF YOU'RE COMING FOR THE KING,"), (3.01, 'YOU BEST NOT MISS.')]),
                     dict(type='voice', k='a', a=565.1, b=567.95, pic=('a', 577.0), words=[(565.14, 'FODEN ON THE EDGE OF THE AREA.'), (567.02, 'ON TO HAALAND!')]),
                     dict(type='voice', k='a', a=607.0, b=612.3, words=[(607.07, 'GUNDOGAN INSIDE HIM.'), (608.59, 'GREALISH WAITING.'), (610.41, 'JACK GREALISH SCORES!')]),
                     dict(type='outro', shots=[('a', 590.5), ('a', 614.0), ('a', 580.0), ('a', 592.0), ('a', 614.5, 0.6)])])

if __name__ == '__main__':
    fps = int(os.environ.get('DEX_FPS', 25))
    out, total = master.render(dict(CFG, fps=fps), S, os.path.join(S, 'out', f'{NAME}_{fps}.mp4'))
    print(out, f'total {total:.1f}s', flush=True)
    import look; look.yt1440(out, out.replace('.mp4', '_yt1440.mp4'))
