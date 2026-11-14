"""CH - Las Vegas 2023: the lead swaps - hype edit, every cut animated (Wed 18 Nov 08:00). Max -> LECLERC -> PEREZ ->
LECLERC -> MAX, a stamp on each pass, the Max/Russell contact, Leclerc's last-corner move, B&W fireworks ending.
Cold open: Max's team celebrating in B&W, freezes into the cutout with VEGAS behind. Song: Ramalama (Bang Bang) - Róisín
Murphy (the 3-5M-view Halloween trend; 107.7 BPM, drop at 8.64), cut every 2 beats. ~28 s, square in 1080x1920, 25 fps.
Sources: F1 'Race Highlights | 2023 Las Vegas Grand Prix' (Q9qSwDxF6YI); pass times from bra/vegas23.json.
Usage: SRC=<folder with the mp4s> SCRATCH=<dir> python3 edit_ch_vegas23_lead_swaps.py"""
import os, sys, glob
sys.path.insert(0, os.path.dirname(__file__))
import hype

S = os.environ.get('SCRATCH', '/tmp')
SRC = os.environ['SRC']
ASSETS = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'dex-edits-assets')
src = lambda vid: glob.glob(os.path.join(SRC, '**', f'*{vid}*.mp4'), recursive=True)[0]
CUTS = [8.64, 9.78, 10.89, 12.0, 13.14, 14.26, 15.37, 16.49, 17.62, 18.74, 19.88, 20.99, 22.11, 23.24, 24.36, 25.47,
        26.61, 27.72, 28.84, 29.98, 31.09, 32.21]
sh = lambda t, fx, **kw: dict(k='v', t=t, fx=fx, **kw)
SHOTS = [sh(12.0, 'flash', stamp='LIGHTS OUT.'), sh(15.0, 'whip_l'), sh(27.0, 'zoom'), sh(39.0, 'punch'), sh(84.0, 'whip_r'),
         sh(154.0, 'flash', stamp='LECLERC.'), sh(178.5, 'glitch'), sh(201.0, 'shake', stamp='CONTACT.'), sh(213.0, 'spin'),
         sh(268.0, 'whip_u'), sh(271.5, 'punch', stamp='PEREZ.'), sh(300.0, 'zoom'), sh(322.5, 'flash', stamp='LECLERC.'),
         sh(342.0, 'glitch'), sh(359.5, 'whip_l', stamp='MAX.'), sh(366.0, 'shake'), sh(417.5, 'punch'),
         sh(438.5, 'zoom', ramp=1.3, stamp='WHAT A MOVE.'), sh(444.0, 'whip_r'), sh(459.0, 'flash'),
         sh(468.0, 'spin', bw=True), sh(478.3, 'flash', bw=True, stamp='MAX WINS VEGAS.')]
CFG = dict(name='vegas23_lead_swaps', files={'v': src('Q9qSwDxF6YI')}, crop=420,
           song=os.path.join(ASSETS, 'songs', 'trend', 'ramalama_roisin_murphy.mp3'), song_in=5.3, cuts=CUTS, end=33.34,
           build=dict(k='v', t=468.5, freeze_at=1.0), shots=SHOTS, intro_text='VEGAS', banner_in=2.4,
           title='LAS VEGAS 2023|THE LEAD SWAPS')

if __name__ == '__main__':
    fps = int(os.environ.get('DEX_FPS', 25))
    out, total = hype.render(dict(CFG, fps=fps), S, os.path.join(S, 'out', f'ch_vegas23_lead_swaps_{fps}.mp4'))
    print(out, f'total {total:.1f}s', flush=True)
