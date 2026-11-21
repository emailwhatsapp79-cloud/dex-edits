"""DB - MOTOGP RACE DAY, PORTIMAO (Sun 22 Nov 08:00). Hype card edit before the race: Bezzecchi on pole with Marc's
all-time lap record, Marc P2 on the grid, and Bezzecchi won here last year. Cut every 2 beats, Anton cards, ~18 s.
Facts from the cloud session's Sat 21 Nov notes (motogp.com): Bez pole + all-time Portimao lap record, Marc P2 on the grid.
Footage: MotoGP 'MotoGP HIGHLIGHTS | 2025 Portuguese GP' (vP51RMuSUsk) - race action + the 2025 winner (Bezzecchi).
Song: Can I Ride (SIDEPIECE) from 40 s.
Usage: SRC=<sources folder> SCRATCH=<dir> python3 edit_db_portimao_race_day.py"""
import os, sys, glob
sys.path.insert(0, os.path.dirname(__file__))
import lyric, hype

S = os.environ.get('SCRATCH', '/tmp')
SRC = os.environ['SRC']
ASSETS = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'dex-edits-assets')
src = lambda vid: glob.glob(os.path.join(SRC, '**', f'*{vid}*.mp4'), recursive=True)[0]
SONG = os.path.join(ASSETS, 'songs', 'trend', 'can_i_ride_sidepiece.mp3')
SONG_IN = 40.0
FILES = {'m': (src('vP51RMuSUsk'), 'crop=1080:1080:420:0')}
SHOTS = [('m', 10.0), ('m', 40.0), ('m', 110.0), ('m', 170.0), ('m', 220.0), ('m', 410.0), ('m', 420.0), ('m', 450.0),
         ('m', 480.0), ('m', 500.0), ('m', 550.0), ('m', 620.0), ('m', 640.0, 0.7), ('m', 670.0, 0.7)]
beats = [b - SONG_IN for b in hype.song_beats(SONG, SONG_IN, 30.0, 2)]
beats = [0.0] + [b for b in beats if b > 0.6]
CUTS = [(round(beats[i], 2), k, t, *sp) for i, (k, t, *sp) in enumerate(SHOTS)]
END = round(beats[len(SHOTS)] + 0.6, 2) if len(beats) > len(SHOTS) else CUTS[-1][0] + 2.0
WORDS = [(0.0, 'RACE DAY.|PORTIMÃO', 210, CUTS[3][0]), (CUTS[3][0], 'BEZZECCHI|POLE + ALL-TIME LAP RECORD', 200, CUTS[6][0] - CUTS[3][0]),
         (CUTS[6][0], 'MARC MÁRQUEZ|P2 ON THE GRID', 200, CUTS[9][0] - CUTS[6][0]),
         (CUTS[9][0], 'LAST YEAR|BEZZECCHI WON HERE', 200, CUTS[12][0] - CUTS[9][0]),
         (CUTS[12][0], 'RACE TODAY.|WHO TAKES IT?', 210, END - CUTS[12][0])]
CFG = dict(name='portimao_race_day', files=FILES, cuts=CUTS, end=END, words=WORDS, flash=[CUTS[3][0], CUTS[6][0], CUTS[9][0], CUTS[12][0]],
           font='anton', grade=False, song=SONG, song_in=SONG_IN, title='RACE DAY|PORTIMÃO', banner_in=0.6)

if __name__ == '__main__':
    fps = int(os.environ.get('DEX_FPS', 25))
    out, total = lyric.render(dict(CFG, fps=fps), S, os.path.join(S, 'out', f'db_portimao_race_day_{fps}.mp4'))
    print(out, f'total {total:.1f}s', flush=True)
    import look; look.yt1440(out, out.replace('.mp4', '_yt1440.mp4'))
