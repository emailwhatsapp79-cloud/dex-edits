"""F1 - UP NEXT IS AUSTIN. Race-week formula (refs M6, M15, M22) for round 18, 23-25 Oct 2026.
The 2026 race has not been run, so the pictures are the official 2025 United States GP highlights
(formula1.com Brightcove 1846447535630260620) kept at native 1280x720. No crop, no upscale.
Song #5 Montagem Kali, instrumental. First shot is a close car, not the aerial.
Panning smears (src ~90, ~246, ~294, ~309, ~446) are not used."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import wideedit

S = os.environ.get('SCRATCH', '/tmp')
SRC = os.path.join(S, 'dexsrc', 'usgp2025.mp4')
ASSETS = os.environ.get('DEX_ASSETS', os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'dex-edits-assets'))
SHOTS = [
    (0.000, 160.20, 'UP NEXT'),    # sharpest car, the hook
    (1.833, 7.00, 'AUSTIN.'),      # the circuit from above — beat 1.840
    (3.900, 34.20, 'ROUND 18'),
    (5.633, 48.20, '23-25 OCT'),   # beat 5.658, one frame early
    (7.100, 170.30, ''),           # beat 7.124
    (8.567, 198.00, ''),           # beat 8.585
    (10.333, 231.00, ''),          # beat 10.343
    (11.800, 207.20, ''),          # beat 11.803
    (13.267, 258.00, ''),          # beat 13.286
    (14.167, 320.40, ''),
    (15.033, 400.20, ''),          # beat 15.048
    (15.900, 434.20, 'RACE'),      # beat 15.909
    (16.467, 458.00, 'WEEK.'),     # beat 16.497, one frame early
]
CFG = dict(
    song=os.path.join(ASSETS, 'songs', '05_montagem_kali_slowed.m4a'),
    off=0.0, end=18.133, size=(1280, 720),
    font=os.path.join(wideedit.ROOT, 'fonts', 'Anton.ttf'), fs=92,
    shots=[(t, SRC, st, w) for t, st, w in SHOTS])

if __name__ == '__main__':
    wideedit.run(CFG, 'grok_austin_up_next', sys.argv)
