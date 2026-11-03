# CLAUDE.md – DEX EDITS

This repo is the home of **DEX EDITS** (TikTok "Dex Edits"; YouTube coming): car, F1, football and movie edits
made with code. All Dex Edits work is committed and pushed HERE ONLY. Never push edits, code, rules or
videos to `scamdecoded-media` – that repo belongs to a different channel (@scamdecoded).

Before making or reviewing any edit, read and follow `EDITING_RULES.md`. Every edit needs a clear direction.
HARD RULE (EDITING_RULES §0): every edit must be clear and sharp with no sign of blur - sharp official sources, no
upscale over ~1.4x, no interpolation/blur effects, stills checked before rendering, 100% crops checked after. A soft
edit is never scheduled.

## Layout
- `EDITING_RULES.md` – the rules learned from Desmond's feedback (direction, hook, beat sync, no repeated takes, branding).
- `REFERENCES.md` – every reference edit studied and what it taught (permanent memory of the training).
- `engine/` – the editing code. `beatsync.py` (drum-hit detection + cut measurement), `velocity.py` (speed ramps,
  source-take detection, clean spans), `brand.py` (DEX EDITS watermark pass), `cardedit.py` (shared engine for
  card/full-frame beat edits with take checks + cut measurement), `takesheet.py` (one thumbnail per source take),
  `edit_*.py` (one script per edit).
- Footage sources that work: IMDb GraphQL (official trailers, 1080p), Bugatti/Porsche newsrooms (press films),
  formula1.com via Brightcove, single TikTok videos via yt-dlp. YouTube downloads are blocked here.
- `songs/LIBRARY.md` – the sound library (titles, BPM, drops, lyric timings). The audio files live in the PRIVATE
  repo `dex-edits-assets` (`songs/`, same numbers/names) – never commit audio to this public repo.
- `videos/` – finished, watermarked edits (`YYYY-MM-DD-slug.mp4`). Public URLs of these files are what
  Metricool uses when scheduling posts.
- `fonts/` – Anton, Orbitron, Archivo (SIL Open Font License).

## Every link or video Desmond sends
1. Save its sound: `python3 engine/add_sound.py <link or file[::Title]>` – downloads, analyses (tempo, drop,
   strongest hits, lyrics with word timings) and adds it to `songs/LIBRARY.md` (+ a stub in `REFERENCES.md`).
2. Study the edit (cuts vs hits, effects, text, story) and write what it teaches into `REFERENCES.md` /
   `EDITING_RULES.md`. Keep the link, not the video.
3. If the sound has speech or lyrics, the picture must show what is being said (EDITING_RULES §3).

## Posting
Scheduling goes through the ZERNIO connector (since Nov 3 2026; Metricool's free plan stops at 20 posts/month/network).
Zernio accounts: TikTok dex_edit0 = 6aea02e372766ee660c00d1b, YouTube dexedits-z3p = 6aea02c8e64468f4036068d9 (first 2
accounts free, unlimited posts - never connect a 3rd). Media = the public GitHub raw URL below (check its size first).
posts_create with schedule_minutes; timezone Africa/Lagos (Zernio shows UTC).
COMMENTS (Desmond, Nov 3 - posts stall with likes but no comments): Desmond adds a TikTok comment POLL by hand when each post
goes live (app-only feature) and pins it. Claude does NOT post automatic text comments (he deleted them; the scheduled task is
off). With every new edit, give him a poll question + 2-3 options that make people take a side.
Daily slots (Desmond, Oct 23): TWO posts a day - 12:00 and 18:00 (was 3/day at 10/12/18 until Oct 23). Fewer, bigger edits:
the strongest edit of the day at 18:00. Mix football / F1 / cars / movies across the week, not one of each per day.
FRESHNESS (Desmond, Oct 18): the three edits of a day are made together, close to the post date, from the newest material
(latest race, matches from the last few days, newest car launches incl. Chinese brands). Older footage only when nothing new
exists, and never stale. Details: EDITING_RULES "Freshness".
HARD RULE (Desmond, Oct 17) - never post a 30 fps file to YouTube when a 60 fps version exists: TikTok gets the 30 fps
file, YouTube gets the 60 fps file (`brand(..., fps=60)`) as a SEPARATE YouTube-only post. Horizontal edits also get a
vertical YouTube Shorts version (`engine/ytshort.py`). Details: EDITING_RULES "Frame rate per platform".
Media URL format: `https://raw.githubusercontent.com/emailwhatsapp79-cloud/dex-edits/main/videos/<file>.mp4`

## Status (Nov 3 2026) - read first in a new session
- NICHE: F1 ONLY (Desmond confirmed Nov 3). Cars, football and movies dropped for now. 2 posts/day 12:00 + 18:00.
- Posted: Lap 1 Brazil (Nov 3, by hand). Scheduled in Zernio: Antonelli World Champion, Nov 3 18:00 (TikTok + YouTube).
- Scheduled in Zernio (TikTok + YouTube each): Nov 4 12:00 I get it (Max), 18:00 Max 'capitalize'; Nov 5 12:00 Lindblad
  'easily', 18:00 Hamilton Ferrari pole; Nov 6 12:00 Mexico onboard, 18:00 Antonelli 'Ascari has his heir' (edit_bh_mexico_week.py).
- Next: Nov 7 posts, then the Brazil GP (Sun Nov 8): race edit the same night from
  formula1.com official highlights (yt-dlp on players.brightcove.net/6057949432001/default_default/index.html?videoId=<id>,
  ids from https://www.formula1.com/en/video), posted Monday 12:00.
- Remaining unposted edits: I get it (Max), 911 emergency (car - dropped if F1 only), Isidor (football).
- Start a new session every day or two to save usage: everything needed is in this repo.
