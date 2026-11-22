"""DD - F1 LAS VEGAS 2026 RACE (Sun 22 Nov morning, made by the CLOUD session while the PC was off).
Story: Max Verstappen wins Las Vegas from pole after Russell keeps taking the lead off him - the commentary call of the swap:
  1 "Warp speed for Russell. The race lead for George Russell and now he will try and break clear. Nothing Max Verstappen
     could do. George Russell leads in Las Vegas."
  2 "...but here comes back Max Verstappen. Round turn 17, sparks flying, retaking the lead."
Payoff (banner + caption): Max wins, Norris P2, Piastri P3; both Mercedes fell back late (Russell P9, Antonelli P4).
Sources: formula1.com clips (Brightcove 6057949432001) 'Russell and Verstappen trade lead' (1882531463419115202) = L,
'Verstappen leads off the grid' (1882530768537215948) = S. They are 1280x720: shown as a DOWNSCALED 16:9 band inside the
square (1080x608, no upscale) instead of a 1.5x square crop (EDITING_RULES: no upscale over ~1.4x).
Song: #04 Legacy phonk. Usage: SRC=<folder with the two mp4s> SCRATCH=<dir> python3 <this>"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import master

S = os.environ.get('SCRATCH', '/tmp')
SRC = os.environ['SRC']
ASSETS = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'dex-edits-assets')
BAND = 'scale=1080:608:flags=lanczos,pad=1080:1080:0:236'
FILES = {'L': (os.path.join(SRC, '1882531463419115202.mp4'), BAND), 'S': (os.path.join(SRC, '1882530768537215948.mp4'), BAND)}
W1 = [(6.86, 'WARP SPEED FOR RUSSELL.'), (8.34, 'THE RACE LEAD FOR GEORGE RUSSELL'), (9.92, 'AND NOW HE WILL'),
      (10.86, 'TRY AND BREAK CLEAR.'), (12.50, 'NOTHING MAX VERSTAPPEN COULD DO.'), (14.38, 'GEORGE RUSSELL'),
      (14.90, 'LEADS IN LAS VEGAS.')]
W2 = [(20.92, 'BUT HERE COMES BACK'), (21.96, 'MAX VERSTAPPEN.'), (23.50, 'ROUND TURN 17,'), (25.32, 'SPARKS FLYING,'),
      (26.40, 'RETAKING THE LEAD.')]
CFG = dict(name='vegas26_race', files=FILES, song=os.path.join(ASSETS, 'songs', '04_legacy_phonk_108bpm.mp3'),
           song_in=4.0, title='LAS VEGAS GP|MAX WINS IT', banner_in=0.0,
           segments=[dict(type='voice', k='L', a=6.8, b=16.3, words=W1),
                     dict(type='voice', k='L', a=20.85, b=27.6, words=W2),
                     dict(type='outro', shots=[('S', 8.0), ('S', 22.4), ('S', 25.6), ('S', 4.5), ('S', 9.6)])])

if __name__ == '__main__':
    fps = int(os.environ.get('DEX_FPS', 25))
    out, total = master.render(dict(CFG, fps=fps), S, os.path.join(S, 'out', f'dd_vegas26_race_{fps}.mp4'))
    print(out, f'total {total:.1f}s', flush=True)
    import look; look.yt1440(out, out.replace('.mp4', '_yt1440.mp4'))
