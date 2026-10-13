"""Edit K - MOVIE. Direction: "Dec 18. Two worlds. One day." Dune: Part Three and Avengers: Doomsday open on the
same day. Hook: Dune / Doom shots trade blows on the intro hits -> black silence: DECEMBER 18. SAME DAY. -> drop:
Dune's world (the final chapter) -> Marvel's world (Doom) -> the clash, cutting between both -> split-screen
ending: DUNE OR DOOMSDAY? Song: 19 "Destroy It All" (gap 2.8-4.8 s, drop 4.795). Official 1080p trailers (IMDb)."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import cardedit
from cardedit import ROOT

D2, DT, DM, DS = 'dune_t2.mp4', 'dune_teaser.mp4', 'doom_trailer.mp4', 'doom_special.mp4'
DUNE, DOOM = 'DUNE: PART THREE', 'AVENGERS: DOOMSDAY'
sh = lambda t, f, src, cx=0.5, mode='real', label='': dict(t=t, file=f, src=src, cx=cx, mode=mode, label=label)

PLAN = [
    # hook: the two films trade shots on the intro hits
    sh(0.000, D2, 14.55, 0.50, 'real', DUNE),        # Paul
    sh(0.520, DM, 97.85, 0.50, 'real', DOOM),        # Doom's mask
    sh(1.044, D2, 22.20, 0.45, 'real', DUNE),        # Chani screams
    sh(1.558, DS, 86.08, 0.50, 'real', DOOM),        # Thor, lightning
    sh(2.099, D2, 150.36, 0.50, 'real', DUNE),       # sand explodes
    sh(2.439, DS, 84.78, 0.50, 'real', DOOM),        # Doom in the storm
    dict(t=2.777, mode='black'),                     # silence: DECEMBER 18. / SAME DAY.
    # drop - Dune's world
    sh(4.795, DT, 87.72, 0.50),                      # the Fremen army charges
    sh(5.529, D2, 8.00, 0.50),                       # Paul and Chani
    sh(6.134, D2, 66.50, 0.60),                      # ornithopters burning at night
    sh(6.638, DT, 16.80, 0.50),                      # leap on the dunes
    sh(7.263, D2, 47.46, 0.50),                      # knife fight
    sh(7.638, D2, 138.86, 0.50),                     # spear
    sh(8.300, DT, 116.72, 0.50, 'slow'),             # Chani, blue eyes (slow-mo)
    sh(9.163, D2, 121.42, 0.50, 'slow'),             # Fremen crawl the sand
    sh(10.026, DT, 123.15, 0.50),                    # Paul climbs the steps
    sh(10.401, DT, 125.12, 0.50),                    # the pyramid crowd
    # Marvel's world
    sh(11.060, DM, 29.95, 0.50),                     # New York
    sh(12.051, DM, 40.50, 0.55),                     # Thor
    sh(12.789, DM, 43.20, 0.50),                     # Shuri
    sh(13.166, DS, 21.60, 0.55),                     # Steve Rogers
    sh(13.826, DM, 89.85, 0.50),
    sh(14.606, DS, 66.85, 0.50),                     # Cyclops
    sh(15.552, DM, 83.20, 0.45),                     # Sue Storm, the wave
    sh(15.927, DM, 67.20, 0.50),                     # the heroes line up
    sh(16.586, DS, 57.80, 0.50),                     # Magneto
    sh(17.306, DS, 96.10, 0.50),                     # Doom's army
    # the clash: one shot each, back and forth
    sh(18.315, D2, 122.15, 0.50, 'real', DUNE),
    sh(18.690, DS, 83.20, 0.50, 'real', DOOM),
    sh(19.078, D2, 147.80, 0.50, 'real', DUNE),
    sh(19.349, DS, 98.60, 0.50, 'real', DOOM),
    sh(19.733, DT, 131.88, 0.50, 'real', DUNE),
    sh(20.100, DS, 80.75, 0.50, 'real', DOOM),
    sh(20.730, DT, 120.30, 0.50, 'real', DUNE),
    sh(21.078, DM, 97.00, 0.50, 'real', DOOM),
    # ending: both at once
    dict(t=21.453, mode='split', sub_mode='slow', parts=[(D2, 29.50, 0.5), (DS, 26.65, 0.5)]),
]
END = 22.9

CFG = dict(
    name='K', layout='card', srcdir=os.path.join(ROOT, 'src_movie'), tmp=os.path.join(ROOT, 'tmp_k'),
    song=os.path.join(ROOT, 'songs', 'named', '19_destroy_it_all_yuji_slowed.mp3'), song_offset=0.0,
    out=os.path.join(ROOT, 'out', 'edit_K_dune_doomsday.mp4'), end=END, plan=PLAN,
    active={D2: (108, 864), DT: (108, 864), DM: (140, 800), DS: (140, 800)},
    swing={7, 17, 27}, drop={7}, punch=set(range(8, 17)) | set(range(27, 35)), warm=0.0, sat=1.05,
    text=[(2.777, 3.912, 'DECEMBER 18.'), (3.912, 4.795, 'SAME DAY.'),
          (4.795, 6.134, 'THE FINAL|CHAPTER.'), (11.060, 12.789, 'DOOM IS|COMING.'),
          (18.315, 19.349, 'ONE DAY.'), (19.349, 20.730, 'TWO WORLDS.'),
          (21.453 + 0.35, END, 'DUNE|OR|DOOMSDAY?')],
    text_cy=960,
)

if __name__ == '__main__':
    cardedit.run(CFG, sys.argv)
