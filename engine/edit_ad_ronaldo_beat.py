"""Edit AD - FOOTBALL, RONALDO, action ON the beat (Desmond: "nothing matches the beat"). Full song: Funk Unico
(super slowed, ICEDMANE & DYSMANE) from 16.03 s - the build, right before the part people wait for - to 42.0 s where the
song itself drops away (fade). Every KEY ACTION is placed on a hit, not just the cut:
  drop 21.34  -> the volley: foot meets ball (source 8.34) exactly on the drop
  24.32       -> Osasuna: ball into the net (19.0)
  26.82       -> Al Nassr: the ball past the diving keeper (50.3)
  29.33       -> the first SIU ever: the pose (11.4)
  30.72       -> the scream (Madrid)
  end         -> the smile, slow, as the song fades.
Build (before the drop): close faces. Layout 'tall' (3:4, sharp); ESPN clips cropped above their text banners.
Official clips: @realmadrid, @alnassr, @espnfc, @espnmx TikTok (1080p vertical)."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import cardedit
from cardedit import ROOT

S0 = 16.03                                  # song time of edit 0
RM, RMA, RMB = 'realmadrid_7117253704331398406', 'realmadrid_7696530374939151638', 'realmadrid_7608867196927773974'
N1, N2, N3 = 'alnassr_7427249589536738568', 'alnassr_7481429251779054864', 'alnassr_7694912506078170386'
EF, EM = 'espnfc_7626863403608427789', 'espnmx_7603404090026036501'
e = lambda song_t: round(song_t - S0, 3)
sh = lambda t, f, src, mode='real', cx=0.5: dict(t=t, file=f + '.mp4', src=src, cx=cx, mode=mode)
DROP = e(21.339)
PLAN = [
    # build - the faces
    sh(0.00, RM, 6.2),                      # purple kit, the look
    sh(e(17.29), EF, 9.0, 'slow'),          # white, the look
    sh(e(19.68), N2, 26.3, 'slow'),         # yellow, the look
    # into the drop: the volley connects ON the drop
    sh(e(20.94), RM, 8.34 - (DROP - e(20.94))),
    sh(e(21.83), RM, 9.4),                  # the celebration of that goal
    sh(e(23.08), RMA, 1.0),                 # Madrid attack
    sh(e(23.53), RMB, 19.0 - (e(24.323) - e(23.53))),   # ball into the net ON 24.32
    sh(e(24.79), RMB, 12.0),                # the celebration
    sh(e(25.73), N3, 42.5),                 # Al Nassr attack
    sh(e(26.25), N3, 50.3 - (e(26.819) - e(26.25))),    # past the keeper ON 26.82
    sh(e(27.61), N1, 5.0),                  # the run, the jump
    sh(e(28.54), EM, 7.6, 'slow', cx=0.4),  # the first SIU - the turn
    sh(e(28.93), EM, 11.4 - (e(29.327) - e(28.93)), cx=0.32),   # the SIU pose (11.4) ON 29.33
    sh(e(30.27), RMA, 12.0),                # the scream (30.72)
    sh(e(31.67), RM, 12.8),                 # purple - in the box
    sh(e(32.60), N1, 8.0),
    sh(e(33.54), EF, 20.5),                 # the last SIU at the Bernabeu
    sh(e(34.80), N2, 14.2),                 # the strike
    sh(e(36.19), RMB, 15.0, 'slow'),        # the hug
    sh(e(37.60), N3, 12.6),
    sh(e(38.93), N3, 16.0),                 # GOAL
    sh(e(40.26), N3, 21.3, 'slow'),         # the smile - the end
]
END = 25.97

CFG = dict(
    name='AD', layout='tall', active={EF + '.mp4': (0, 1440), EM + '.mp4': (0, 1130)},
    srcdir=os.path.join(ROOT, 'src_cr7'), tmp=os.path.join(ROOT, 'tmp_ad'),
    song=os.path.join(ROOT, 'songs', 'cr7_funkunico.mp3'), song_offset=0.0,
    out=os.path.join(ROOT, 'out', 'edit_AD_ronaldo_beat.mp4'), end=END, plan=PLAN,
    swing=set(), drop=set(), punch=set(), cut_flash=False, warm=0.0, sat=1.06, grain=0.0, vig=0.3,
    fx={}, text=[],
)

if __name__ == '__main__':
    cardedit.run(CFG, sys.argv)
