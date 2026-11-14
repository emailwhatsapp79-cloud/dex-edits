"""CP - Las Vegas: QUALIFYING TONIGHT (Fri 20 Nov 18:00; quali is Fri 20:00 in Vegas = Sat 05:00 Lagos). Hype edit, every cut
animated: cold open on last year's pole sitter, B&W, freezing into the cutout with POLE behind him; then 2025's wet
qualifying cut on the hits of "Can I Ride" (SIDEPIECE - 481.8K TikTok videos), Q1 / Q2 / Q3 stamps, sparks, spray,
onboards, ending in B&W on 'TONIGHT.'. ~23.7 s, square in 1080x1920, 25 fps.
Sources: F1 'Qualifying Highlights | 2025 Las Vegas Grand Prix' (gC88zq9Y4gQ).
Usage: SRC=<folder with the mp4s> SCRATCH=<dir> python3 edit_cp_quali_tonight.py"""
import os, sys, glob
sys.path.insert(0, os.path.dirname(__file__))
import hype

S = os.environ.get('SCRATCH', '/tmp')
SRC = os.environ['SRC']
ASSETS = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'dex-edits-assets')
src = lambda vid: glob.glob(os.path.join(SRC, '**', f'*{vid}*.mp4'), recursive=True)[0]
CUTS = [15.07, 16.0, 16.9, 17.81, 18.72, 19.62, 20.53, 21.46, 22.36, 23.27, 24.17, 25.08, 26.01, 26.89, 27.82, 28.72,
        30.07, 31.0, 31.88]
sh = lambda t, fx, **kw: dict(k='q', t=t, fx=fx, **kw)
SHOTS = [sh(2.0, 'flash', stamp='Q1.'), sh(10.0, 'whip_l'), sh(30.0, 'zoom'), sh(40.0, 'punch'), sh(45.5, 'shake'),
         sh(50.0, 'whip_r'), sh(60.0, 'glitch'), sh(64.0, 'spin'), sh(86.0, 'whip_u', stamp='Q2.'), sh(104.0, 'flash'),
         sh(162.0, 'zoom'), sh(201.0, 'glitch'), sh(258.0, 'flash', stamp='Q3.'), sh(300.0, 'whip_l'), sh(330.0, 'shake'),
         sh(375.0, 'punch', ramp=0.8), sh(405.0, 'flash'), sh(411.0, 'spin'), sh(444.0, 'flash', bw=True, stamp='TONIGHT.')]
CFG = dict(name='quali_tonight', files={'q': src('gC88zq9Y4gQ')}, crop=420,
           song=os.path.join(ASSETS, 'songs', 'trend', 'can_i_ride_sidepiece.mp3'), song_in=12.07, cuts=CUTS, end=32.81,
           build=dict(k='q', t=443.6, freeze_at=1.0), shots=SHOTS, intro_text='POLE', banner_in=2.4,
           title='LAS VEGAS|QUALIFYING TONIGHT')

if __name__ == '__main__':
    fps = int(os.environ.get('DEX_FPS', 25))
    out, total = hype.render(dict(CFG, fps=fps), S, os.path.join(S, 'out', f'cp_quali_tonight_{fps}.mp4'))
    print(out, f'total {total:.1f}s', flush=True)
