"""Edit L - FOOTBALL. Direction: "19. Already past Messi." Lamine Yamal became the youngest player ever to reach 50
goals for Barcelona - younger than Messi was. Hook: his face (19 YEARS OLD.) -> the build: dribbles (50 GOALS FOR
BARÇA.) -> drop: the goals (YOUNGEST EVER. / YOUNGER THAN MESSI.) -> celebrations -> ending: the name and the 10 on
his back (THE NEW NUMBER 10.). Song: 11 "Funk Mada" from 4.0 s (drop 11.633 -> 7.633). Official club/league
TikTok clips (vertical), full-frame layout."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import cardedit
from cardedit import ROOT

A, B, C, D = 'laliga_7662434915010514198.mp4', 'laliga_7502103327602167062.mp4', 'fcbarcelona_7692412797816179990.mp4', 'espnfc_7591238901046512909.mp4'
E, F, G, I = 'espnfc_7611951679151344927.mp4', 'espnfc_7604166026011479327.mp4', 'laliga_7504778318395297046.mp4', 'fcbarcelona_7481568044716772630.mp4'
J, K, L, M = 'laliga_7461355471870430496.mp4', 'cbssportsgolazo_7556349129341914423.mp4', 'fcbarcelona_7428746011541081377.mp4', 'laliga_7482762558869490966.mp4'
sh = lambda t, f, src, cx=0.5, mode='real': dict(t=t, file=f, src=src, cx=cx, mode=mode)

PLAN = [
    sh(0.000, F, 5.90),               # hook: his face
    sh(1.291, B, 0.30),               # smile
    sh(2.062, L, 15.00, 0.5, 'slow'), # close-up (slow: the source dissolves at ~15.6)
    # build: the dribbles
    sh(3.037, C, 0.20),
    sh(4.457, L, 4.00),
    sh(4.875, J, 6.50),
    sh(5.259, B, 46.85),
    sh(5.650, E, 6.50),
    sh(6.045, C, 3.50),
    sh(6.451, B, 16.50),
    sh(7.053, B, 30.85),
    # drop: the goals
    sh(7.633, D, 6.10),
    sh(8.765, B, 19.60),
    sh(10.226, B, 43.25),
    sh(10.820, B, 51.30),
    sh(11.215, B, 2.50),
    sh(11.610, B, 25.05),
    sh(12.014, B, 6.45),
    sh(12.418, C, 7.95),
    sh(13.012, L, 9.75),
    sh(13.402, J, 10.95),
    sh(14.390, I, 5.80),
    # celebrations
    sh(14.775, F, 9.30),
    sh(15.174, G, 1.00),
    sh(16.183, B, 13.70),
    sh(16.576, B, 35.60),
    sh(17.165, F, 7.66),
    sh(17.558, B, 11.45),
    sh(17.960, I, 15.00),
    sh(18.355, B, 56.10),
    sh(18.759, 'fcbarcelona_7478030001242115350.mp4', 17.30),
    # ending: the name and the 10
    sh(19.758, A, 26.40, 0.5, 'slow'),
]
END = 22.6

CFG = dict(
    name='L', layout='full', srcdir=os.path.join(ROOT, 'src_fb'), tmp=os.path.join(ROOT, 'tmp_l'),
    song=os.path.join(ROOT, 'songs', 'named', '11_funk_mada_icedmane.mp3'), song_offset=4.0,
    out=os.path.join(ROOT, 'out', 'edit_L_yamal.mp4'), end=END, plan=PLAN,
    swing=set(), drop={11}, punch=set(range(11, 22)), warm=0.0, sat=1.1,
    text=[(0.0, 2.062, '19 YEARS OLD.'), (4.457, 7.053, '50 GOALS|FOR BARÇA.'),
          (7.633, 10.226, 'YOUNGEST|EVER.'), (10.226, 12.418, 'YOUNGER|THAN MESSI.'),
          (19.758 + 0.2, END, 'THE NEW|NUMBER 10.')],
    text_cy=1050,
)

if __name__ == '__main__':
    cardedit.run(CFG, sys.argv)
