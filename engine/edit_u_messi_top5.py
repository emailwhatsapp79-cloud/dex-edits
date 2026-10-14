"""Edit U - FOOTBALL, star of the day: MESSI. "Messi / Top 5" countdown (DEX template COUNTDOWN). Hook: 1.4 s teaser
of #1 (the ball flying at the Liverpool wall) with WAIT FOR #1., then #5 -> #1, each goal with its own commentary /
crowd audio (picture = what is said), the celebration after it. #1 carries its clip's own song ("I'm the world's
greatest"). Footage: official @fcbarcelona, @intermiamicf, @mls, @espnfc TikTok clips."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import countdown
from cardedit import ROOT

D = os.path.join(ROOT, 'src_messi')
F = lambda n: os.path.join(D, n + '.mp4')
ESP, M4, M3, M2, FCB = (F('espnfc_7634968557062786318'), F('mls_7523761026202881310'), F('mls_7421350900834258218'),
                        F('mls_7491489181160508702'), F('fcbarcelona_6723364392915832069'))
PIECES = [
    dict(file=FCB, a=8.9, b=10.3, rank=1, cap='', teaser=True),
    dict(file=ESP, a=23.4, b=30.9, rank=5, cap='BARCA 2005 / HIS FIRST GOAL', blur=[(0.83, 0.985)]),
    dict(file=ESP, a=11.9, b=13.4, rank=5, cap='BARCA 2005 / HIS FIRST GOAL', blur=[(0.83, 0.985)], cont=True),
    dict(file=M4, a=5.5, b=13.6, rank=4, cap='INTER MIAMI / MESSI MAGIC', blur=[(0.625, 0.67)]),
    dict(file=M3, a=10.6, b=15.8, rank=3, cap='INTER MIAMI / FREE-KICK'),
    dict(file=M2, a=19.5, b=26.0, rank=2, cap='INTER MIAMI / THE SMALLEST WINDOW'),
    dict(file=M2, a=36.9, b=40.6, rank=2, cap='INTER MIAMI / THE SMALLEST WINDOW', cont=True),
    dict(file=FCB, a=2.6, b=12.6, rank=1, cap='VS LIVERPOOL / UCL GOAL OF THE SEASON'),
    dict(file=FCB, a=0.0, b=2.4, rank=1, cap='VS LIVERPOOL / UCL GOAL OF THE SEASON', cont=True),
]
OUT = os.path.join(ROOT, 'out', 'edit_U_messi_top5.mp4')

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'stills':
        for n, lt in [(0, 0.6), (1, 0.3), (1, 3.0), (2, 0.5), (3, 0.4), (3, 5.0), (4, 0.4), (4, 3.5), (5, 0.4), (5, 5.5), (6, 1.0), (7, 0.4), (7, 6.5), (8, 1.0)]:
            countdown.still(PIECES, 'MESSI', n, lt, os.path.join(ROOT, 'out', f'U_{n}_{lt}.jpg'))
    else:
        countdown.render(PIECES, 'MESSI', OUT, os.path.join(ROOT, 'tmp_u'))
