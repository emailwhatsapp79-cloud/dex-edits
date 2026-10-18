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
Scheduling goes through the Metricool connector (brand with TikTok "Dex Edits", timezone Africa/Lagos).
Daily slots (Desmond, Oct 15): 10:00 FOOTBALL, 12:00 F1, 18:00 CAR - one of each every day, stars rotating.
FRESHNESS (Desmond, Oct 18): the three edits of a day are made together, close to the post date, from the newest material
(latest race, matches from the last few days, newest car launches incl. Chinese brands). Older footage only when nothing new
exists, and never stale. Details: EDITING_RULES "Freshness".
HARD RULE (Desmond, Oct 17) - never post a 30 fps file to YouTube when a 60 fps version exists: TikTok gets the 30 fps
file, YouTube gets the 60 fps file (`brand(..., fps=60)`) as a SEPARATE YouTube-only post. Horizontal edits also get a
vertical YouTube Shorts version (`engine/ytshort.py`). Details: EDITING_RULES "Frame rate per platform".
Media URL format: `https://raw.githubusercontent.com/emailwhatsapp79-cloud/dex-edits/main/videos/<file>.mp4`
