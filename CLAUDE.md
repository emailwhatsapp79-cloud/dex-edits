# CLAUDE.md – DEX EDITS

This repo is the home of **DEX EDITS** (TikTok "Dex Edits"; YouTube coming): car, F1, football and movie edits
made with code. All Dex Edits work is committed and pushed HERE ONLY. Never push edits, code, rules or
videos to `scamdecoded-media` – that repo belongs to a different channel (@scamdecoded).

Before making or reviewing any edit, read and follow `EDITING_RULES.md`. Every edit needs a clear direction.

## Layout
- `EDITING_RULES.md` – the rules learned from Desmond's feedback (direction, hook, beat sync, no repeated takes, branding).
- `engine/` – the editing code. `beatsync.py` (drum-hit detection + cut measurement), `velocity.py` (speed ramps,
  source-take detection, clean spans), `brand.py` (DEX EDITS watermark pass), `cardedit.py` (shared engine for
  card/full-frame beat edits with take checks + cut measurement), `takesheet.py` (one thumbnail per source take),
  `edit_*.py` (one script per edit).
- Footage sources that work: IMDb GraphQL (official trailers, 1080p), Bugatti/Porsche newsrooms (press films),
  formula1.com via Brightcove, single TikTok videos via yt-dlp. YouTube downloads are blocked here.
- `songs/LIBRARY.md` – the sound library (titles, BPM, drops, lyric timings). Audio files are NOT stored here
  (copyrighted); keep them locally.
- `videos/` – finished, watermarked edits (`YYYY-MM-DD-slug.mp4`). Public URLs of these files are what
  Metricool uses when scheduling posts.
- `fonts/` – Anton, Orbitron, Archivo (SIL Open Font License).

## Posting
Scheduling goes through the Metricool connector (brand with TikTok "Dex Edits", timezone Africa/Lagos).
Media URL format: `https://raw.githubusercontent.com/emailwhatsapp79-cloud/dex-edits/main/videos/<file>.mp4`
