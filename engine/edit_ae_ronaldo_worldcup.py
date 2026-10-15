"""Edit AE - FOOTBALL, RONALDO, rebuild of AD (Desmond: "the edit is blurry ... most of the things don't land or don't
make sense"). ONE story, ONE tournament, only sharp official footage: the 2026 World Cup.
Direction: "6 World Cups. Still him."
  build (quiet)  -> the stare before the knockout penalty (two close-ups), the run-up
  DROP 5.31      -> the ball hits the net (behind-the-goal angle), contact just before it
  then           -> he runs at the pitch-side camera, the stare, the fans explode, the SIU jump ON 9.99,
                    the early group goal: the net-cam shakes ON 14.36, celebrations on the hits,
                    the end: he looks up at the sky while the song fades.
Song: Funk Unico section (16.03-42.0 of the full song) - cuts on the 808 hits (onsets measured from the low band).
Layout 'full' at native 1080x1920 (no blurred bands, no upscaling on the FIFA clips); FOX clips cropped above their
burned-in caption. Footage: @fifaworldcup and @foxsports TikTok (1080p)."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import cardedit
from cardedit import ROOT

P, G, C = 'fifaworldcup_7658141867128737027', 'fifaworldcup_7665722631781420310', 'fifaworldcup_7654667605822737686'
F1, F2, F3 = 'foxsports_7654639679110679839', 'foxsports_7654640059387333919', 'foxsports_7658093909209320734'
sh = lambda t, f, src, mode='real', cx=0.5: dict(t=t, file=f + '.mp4', src=src, cx=cx, mode=mode)
PLAN = [
    sh(0.00, P, 0.00),          # the stare
    sh(1.54, F3, 0.10),         # closer
    sh(3.65, F3, 4.12),         # the run-up (wide)
    sh(4.89, P, 4.93),          # behind the goal: contact -> the ball hits the net ON the drop 5.31
    sh(6.40, C, 6.30),          # he runs at the pitch-side camera, past it
    sh(8.60, F1, 5.80),         # the fans explode
    sh(9.07, F2, 2.10),         # the bench claps behind him...
    sh(9.99, F2, 6.40),         # ...the SIU jump ON 9.99, the scream
    sh(12.82, G, 5.80),         # the group goal from the net-cam: the keeper dives...
    sh(14.36, G, 7.63),         # ...the net shakes ON 14.36
    sh(14.68, F3, 9.95),        # celebrations on the hits
    sh(15.93, C, 11.95),        # at the corner flag
    sh(17.19, F1, 9.50),
    sh(18.45, C, 28.20),        # the hug
    dict(sh(20.29, C, 30.60), jump=True),   # laughing
    dict(sh(22.20, C, 36.30), jump=True),   # looks up at the sky - the end
]
END = 25.97

CFG = dict(
    name='AE', layout='full',
    active={F1 + '.mp4': (0, 1350), F2 + '.mp4': (0, 1230), F3 + '.mp4': (0, 1370)},
    srcdir=os.path.join(ROOT, 'src_cr7b'), tmp=os.path.join(ROOT, 'tmp_ae'),
    song=os.path.join(ROOT, 'songs', 'cr7_funkunico.mp3'), song_offset=0.0,
    out=os.path.join(ROOT, 'out', 'edit_AE_ronaldo_worldcup.mp4'), end=END, plan=PLAN,
    swing=set(), drop=set(), punch=set(), cut_flash=False, warm=0.0, sat=1.04, grain=0.0, vig=0.2,
    fx={}, text=[], crf=12,
)

if __name__ == '__main__':
    cardedit.run(CFG, sys.argv)
