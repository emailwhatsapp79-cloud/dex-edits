"""BC - MOVIE: "TELL THEM WE READY." Avengers: Doomsday (Dec 18 2026) x "Ready" - Madara Dusal (Desmond's pick, Oct 23).
Shape learned from the Avengers lyric edits Desmond sent (3.5M / 2.2M / 892k, all 1920x1080): horizontal native, one
lyric word stamped per beat, a cut on every beat. Intro (0-6.4): Doom and the storm, "IT IS MY TIME". 6.41-12.61: one
hero per READY - the roll call. 13.10 white flash. 13.58-20.71: the war, a cut every beat. "YOU DON'T NEED LIGHTER /
CAUSE I BRING THE FIRE" over fire, then the official Dec 18 title card.
Footage: official Marvel trailers (IMDb, 1920x1080, letterboxed), pixels 1:1. Song: the TikTok sound (ref, 123 bpm)."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import wideedit

M = os.environ.get('DEX_MOVIE', '/tmp/claude-0/-home-user-scamdecoded-media/7be1f147-2656-5ce6-9a44-2202ae528a61/scratchpad/src_movie')
f = lambda n: os.path.join(M, n + '.mp4')
DT, DS, T3, T4, W = f('doom_trailer'), f('doom_special'), f('doom_t3'), f('doom_t4'), f('white')

SHOTS = [
    # intro - Doom, the storm, "it is my time"
    (0.00, DS, 51.60, ''),   # Doom's eye behind the mask
    (1.16, DS, 80.80, ''),   # lightning hits the field, Doom stands
    (2.14, DT, 30.00, ''),   # New York from above
    (3.07, DS, 27.00, ''),   # Doom's armour in the dark
    (4.04, DS, 1.00, ''),    # the green throne room
    (4.95, DS, 84.85, ''),   # Doom's mask
    (5.94, T4, 33.25, ''),   # Wakanda's warriors
    # READY - the roll call, one face per beat
    (6.41, DT, 40.60, ''),   # Thor
    (6.90, DT, 43.30, ''),   # Shuri
    (7.38, DT, 44.55, ''),   # M'Baku
    (7.87, T4, 17.00, ''),   # Talokan
    (8.34, DT, 63.60, ''),   # Loki
    (8.80, DS, 21.70, ''),   # Steve Rogers
    (9.29, DS, 50.30, ''),   # Reed Richards
    (9.75, DS, 66.95, ''),   # Cyclops
    (10.24, DS, 57.90, ''),  # Magneto
    (10.70, DT, 77.90, ''),  # Professor X
    (11.19, DT, 83.30, ''),  # Sue Storm
    (11.68, T4, 38.40, ''),  # The Thing
    (12.14, DT, 92.10, ''),  # Gambit
    (12.61, DS, 65.50, ''),  # Shuri and her guard
    (13.10, W, 0.00, ''),    # white flash
    (13.23, DS, 98.60, ''),  # Doom, the fire behind him
    # READY - the war, a cut every beat
    (13.58, DS, 82.20, ''),  # Thor in the lightning
    (14.05, DS, 83.95, ''),  # Thor's eyes
    (14.51, T3, 45.75, ''),  # Cyclops' blast
    (15.00, DT, 87.20, ''),  # the red figure
    (15.49, DS, 86.10, ''),  # Thor swings
    (15.95, DS, 86.85, ''),  # Thor, blue eyes
    (16.44, T4, 29.00, ''),  # Wakanda marches
    (16.90, DT, 57.10, ''),  # the purple blade
    (17.39, DT, 59.70, ''),  # Shang-Chi
    (17.86, DT, 97.00, ''),  # lightning
    (18.34, T4, 36.00, ''),  # M'Baku roars
    (18.81, DT, 46.50, ''),  # Wakanda's throne room
    (19.30, DS, 88.20, ''),  # the charge
    (19.76, DT, 89.85, ''),  # Sue screams
    (20.25, DT, 64.60, ''),  # the desert
    (20.71, DT, 10.95, ''),  # golden light
    # "you don't need lighter" - fire
    (22.15, DT, 24.72, ''),  # comic fire
    (22.62, DT, 25.35, ''),  # comic fire
    (23.10, DS, 93.60, ''),  # green fire
    (24.06, DT, 33.80, ''),  # the ring
    # "cause I bring the fire"
    (25.01, DS, 100.10, ''), # Doom, arms out, fire
    (25.94, DT, 90.45, ''),  # Sue, the force field
    (26.42, T3, 47.15, ''),  # the fire wave
    (26.91, DS, 87.60, ''),  # Thor's eyes, last look
    (27.38, DT, 125.10, ''),  # official title: AVENGERS DOOMSDAY
]

WORDS = [(0.40, 'TRYNA'), (0.60, 'ACT'), (0.80, 'LIKE'), (1.00, 'THEY'), (1.60, 'VIBE'), (2.00, 'I'), (2.20, "DON'T"),
         (2.40, 'KNOW'), (2.80, "DON'T"), (3.00, 'WANT'), (3.30, 'THE'), (3.60, 'SHINE'), (4.40, 'CARE'), (4.60, 'BECAUSE'),
         (4.85, 'IT'), (5.00, 'IS'), (5.20, 'MY'), (5.40, 'TIME'), (5.80, 'TELL'), (6.00, 'THEM'), (6.20, 'WE')]
WORDS += [(t, 'READY') for t in (6.41, 6.90, 7.38, 7.87, 8.34, 8.80, 9.29, 9.75, 10.24, 10.70, 11.19, 11.68, 12.14)]
WORDS += [(12.61, 'IF'), (12.80, 'THEY'), (13.58, 'THEM'), (13.80, 'WE')]
WORDS += [(t, 'READY') for t in (14.05, 14.51, 15.00, 15.49, 15.95, 16.44, 16.90, 17.39, 17.86, 18.34, 18.81, 19.30, 19.76, 20.25)]
WORDS += [(21.18, 'YOU'), (21.80, "DON'T"), (22.15, 'NEED'), (22.62, 'LIGHTER'), (23.10, 'LIGHTER'), (23.57, 'LIGHTER'),
          (24.06, 'LIGHTER'), (25.01, 'CAUSE'), (25.47, 'I'), (25.75, 'BRING'), (26.15, 'THE'), (26.42, 'FIRE'), (26.91, 'FIRE')]
END = 28.60
TEXT = [(t, (WORDS[i + 1][0] if i + 1 < len(WORDS) else 27.38) - 0.02, w) for i, (t, w) in enumerate(WORDS)]

cfg = dict(song=f('ready_song'), off=0.0, end=END, size=(1920, 1080), font=os.path.join(wideedit.ROOT, 'fonts', 'Anton.ttf'),
           fs=118, shots=SHOTS, words=TEXT)

if __name__ == '__main__':
    wideedit.run(cfg, 'bc_doomsday_ready', sys.argv)
