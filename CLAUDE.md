# CLAUDE.md – DEX EDITS

This repo is the home of **DEX EDITS** (TikTok "Dex Edits"; YouTube coming): car, F1, football and movie edits
made with code. All Dex Edits work is committed and pushed HERE ONLY. Never push edits, code, rules or
videos to `scamdecoded-media` – that repo belongs to a different channel (@scamdecoded).

Before making or reviewing any edit, read and follow `EDITING_RULES.md`. Every edit needs a clear direction.
HARD RULE (EDITING_RULES §0): every edit must be clear and sharp with no sign of blur - sharp official sources, no
upscale over ~1.4x, no interpolation/blur effects, stills checked before rendering, 100% crops checked after. A soft
edit is never scheduled.

## Layout
- `GOALS.md` – this month's targets (followers, views, likes, comments; per-video targets) + the weekly check-in table.
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
- `.claude/skills/humanizer/` – blader/humanizer (MIT): rewrites text so it doesn't read as AI-written. Run every caption,
  YouTube title and poll question through it before scheduling (short, plain, like a fan wrote it).

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
POLL COMMENT FORMAT (Desmond, Nov 7): the QUESTION ONLY, e.g. "Quick poll 👇 Does Lewis win another race before he retires?" - no "Reply ✅ YES or ❌ NO" options typed after it.
COMMENTS (Desmond, Nov 3 - posts stall with likes but no comments): Desmond adds a TikTok comment POLL by hand when each post
goes live (app-only feature) and pins it. On YOUTUBE Claude posts a "Quick poll 👇 ... Reply 🔴 X or 🔵 Y" text comment ~7 min
after each post goes live on TikTok AND YouTube (Zernio comments_reply_to_inbox_post) - it worked (replies within the hour, Nov 3).
With every new edit, give Desmond a poll question + 2-3 options that make people take a side. FACT-CHECK the question: the
Nov 3 one called Max a "youngest champion" and a viewer corrected it (Vettel held the record until Kimi).
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

## Gemini (watch + listen helper, since Nov 4)
The environment "for s scraper" holds a Gemini API key as a network secret (header x-goog-api-key, injected by the proxy -
never put a key in code). Call https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent with
inline_data (audio/mp3 or video/mp4 under ~20 MB; bigger files via the Files API) to get a TEXT description: is a sound clean
(no speech/SFX from another edit), where the drop is, the mood, what happens when in a reference edit. Use it instead of loading
dozens of frame images when studying references; still verify hit sync frame by frame yourself.
Tested Nov 4: #157 = clean instrumental, Middle-Eastern/Mediterranean, upbeat, beat kicks in at 0:04.

## Race weekends (Desmond, Nov 4)
- Before scheduling several days ahead, CHECK THE F1 CALENDAR. If a race falls inside the window, schedule only up to the day
  before / one day ahead and TELL Desmond why ("race tomorrow - only 1 day ahead").
- Race day: as soon as the official highlights are on formula1.com (~1-2 h after the flag), make a quick race edit and post it
  that night or first thing next morning. Fresh clips beat backdated ones.
- Reminders set in this session: Sat Nov 7 09:00 Lagos (plan Sat/Sun posts), Sun Nov 8 21:30 Lagos (Brazil race edit).

## YouTube numbers (Nov 4, Zernio analytics, 46 subscribers)
- Like rate is fine on the strong F1 posts: finish the job 256/5,465 (4.7%), Austin keep watching 182/4,743 (3.8%),
  around the world 41/953 (4.3%), Antonelli champion 34/1,319 (2.6%).
- Weak: football/movie/generic - Bellingham 0.7%, Kane 1.2%, Doomsday 1.0%, Ferrari 1.5%, I get it 1.0% (496 views).
- So the fix is the post, not YouTube: a named star + a stake in the title, a hook in the first second, a payoff, a loop.
- YouTube Studio / Gemini breakdown (Nov 4): lifetime 55,749 views, 21,874 unique viewers, 1,612 likes, +46 subs, avg
  "stayed to watch" 45.1%. THE DECIDING NUMBER IS STAYED-vs-SWIPED: above ~52-57% a Short scales into the thousands
  (Antonelli "20 years old. One race from history" 11,119 views / 52.7%; finish the job 52.8%; Austin keep watching 57.9%);
  in the low 40s it stalls (Lap 1 Austin 40.6%, I get it 45.6%). Drop-off happens in the first 1-2 s. Target: 60%+.
  -> Every edit's FIRST FRAME must already be the action or the most dramatic face/moment - no fade-in, no slow build, no
  talking head first. Driver-narrative stories (Antonelli, Max vs Kimi, Hamilton in red) win. Only 14 comments channel-wide.

## Progress check Nov 6 (Zernio) - THE TIKTOK PROBLEM IS THE FORMAT
- YouTube 46 -> 54 subs. Lindblad "easily" Short = 10,489 views / 512 likes (4.9%) in a day - our 2nd best ever. Max 1,778,
  Antonelli champ 1,942, Hamilton 1,290, I get it 1,248. YouTube gets the VERTICAL ytshort version.
- TikTok still 5 followers. Every post stops at ~250-330 views (Antonelli 994) even though like rate is huge (14-17%).
  TikTok gets the HORIZONTAL 16:9 file: small picture with black bars on a phone -> retention collapses: 100% -> ~40% by 2 s,
  ~30% by 3 s, completion 3-16%. 97-99% of views come from For You and 100% are non-followers. Audience: UK, Italy, Poland,
  Germany, Netherlands (Europe).
- FIX: post the VERTICAL version on TikTok too (ytshort.py at 30 fps), and keep edits short (Lindblad 13 s had the best
  TikTok retention: 59% at 2 s, 16% completion; and the best YouTube result).

## TikTok test (Desmond, Nov 7) - FULL SCREEN, posted BY HAND
- TikTok gets a FULL-SCREEN 9:16 file: no black bars, no title text (centre crop of the 16:9 source, 405x720 -> 540x960 =
  1.33x, sharp; DEX_VERT=1 in edit_bk_norris_pole.py). The song stays in the edit (never send a silent edit).
- YouTube keeps the band + title Short (ytshort.py) - it works there.
- For 1-2 days Desmond posts TikTok BY HAND (so the trending sound can be attached in-app); Claude schedules YouTube only and
  sends him the TikTok file + caption + poll question. Then compare views (were ~250-330 per post via Zernio).

## Trend 48 (Desmond's app, repo emailwhatsapp79-cloud/trend-48, Nov 6)
Shows named songs moving on TikTok + YouTube Shorts (tokchart.com sounds/songs by country NG/US/UK/BR/PH, kabo.sh,
charts.youtube.com SHORTS_TRACKS_BY_USAGE daily by market). tokchart.com answers 403 to plain requests from this container -
read it through Playwright or use Desmond's deployed app. Use it to pick trending, CLEAN songs (check with Gemini).

## Ideas saved for later (Desmond, Nov 4 - not built yet, do not start without him)
- TREND RADAR: a tool in the container that checks what is trending on TikTok right now (top songs/sounds, by country:
  Nigeria, US, UK) to pick hook sounds. Feasible: TikTok Creative Center's "Popular music" page
  (ads.tiktok.com/business/creativecenter/inspiration/popular/music) - its API refuses plain requests (needs signed headers),
  so read the page with the preinstalled Playwright/Chromium. Save the top ~20 with add_sound (clean versions only).
- REVIEW PAGE: one link per edit where Desmond leaves notes on the exact second (idea from mrpaidsocial's video-editor-agent;
  that repo has no licence - build our own, e.g. as an Artifact page).
- GOALS DASHBOARD: a live page with progress bars for GOALS.md (Desmond wants it, on hold Nov 4 - weekly usage nearly used up).
- AUTO-QA: script that scans every finished file for black/frozen frames, loudness, the DEX EDITS mark, before scheduling.
- Desmond will later move the work to his own PC (Claude desktop app) when he is home on Wi-Fi.
