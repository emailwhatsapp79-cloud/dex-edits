"""BY - MotoGP: Bezzecchi, DOWN ON SATURDAY, WINNER ON SUNDAY (2026 Qatar GP) - first lyric-style pro edit (Desmond, Nov 13:
the @moto.rho look - one giant serif word per beat, film grade, emotion over effects; trending sound from TikTok).
21.4 s, square in 1080x1920, 25 fps. Song: Chris Grey "Let the World Burn" (TikTok guitar cut, 95.7 BPM, drop at 11.22).
  verse  (0-11.2)  Saturday: the start, the contact, the slide, sparks through the fence, the Aprilia garage, the crowd's
                   shock, Bezzecchi riding back on a marshal's scooter
  drop   (11.2-)   Sunday: last lap, the pit wall jumping, the fist, fireworks, the flag, the hugs, champagne, the flag again
Words tell the story (no lyrics on screen): SATURDAY. DOWN. SUNDAY. WINNER. BEZZECCHI.
Usage: SRC=<sources folder> SCRATCH=<work dir> python3 edit_by_bezzecchi_sat_sun.py"""
import os, sys, glob
sys.path.insert(0, os.path.dirname(__file__))
import lyric

S = os.environ.get('SCRATCH', '/tmp')
SRC = os.environ['SRC']
ASSETS = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'dex-edits-assets')
src = lambda vid: glob.glob(os.path.join(SRC, '**', f'*{vid}*.mp4'), recursive=True)[0]
SQ = 'crop=1080:1080:420:0'
FILES = {'m': (src('dBf-CVXVLwk'), SQ), 'b': (src('0CIRv1O6Ghs'), SQ)}
# (t, source, source in, speed) - verse every 2 beats, drop every beat; never the same angle twice in a row
CUTS = [(0.00, 'm', 0.3), (1.49, 'm', 8.6), (2.83, 'm', 12.0), (4.06, 'm', 54.0), (5.36, 'm', 18.0), (6.66, 'm', 75.0),
        (7.94, 'm', 142.0, 0.8), (10.47, 'b', 167.0),
        (11.22, 'b', 170.0), (11.80, 'b', 172.0), (12.45, 'b', 180.0), (13.10, 'b', 182.0), (13.75, 'b', 174.0),
        (14.40, 'b', 186.0), (15.05, 'b', 176.0), (15.72, 'b', 188.0), (16.37, 'b', 192.0), (17.00, 'b', 198.0),
        (17.62, 'b', 202.0), (18.27, 'b', 206.0, 0.7)]
WORDS = [(0.26, 'SATURDAY.', 190), (4.06, 'DOWN.', 260), (10.47, 'SUNDAY.', 220), (13.10, 'WINNER.', 230),
         (17.62, 'BEZZECCHI.', 190)]
CFG = dict(name='bezzecchi_sat_sun', files=FILES, cuts=CUTS, end=21.4, words=WORDS, flash=[4.06, 11.22],
           song=os.path.join(ASSETS, 'songs', 'trend', 'let_the_world_burn_tiktok_guitar.mp3'),
           title='DOWN ON SATURDAY|WINNER ON SUNDAY', banner_in=0.6)

if __name__ == '__main__':
    fps = int(os.environ.get('DEX_FPS', 25))
    out, total = lyric.render(dict(CFG, fps=fps), S, os.path.join(S, 'out', f'by_bezzecchi_sat_sun_{fps}.mp4'))
    print(out, f'total {total:.1f}s', flush=True)
