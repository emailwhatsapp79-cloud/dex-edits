# HANDOFF - shared status between the PC session and the cloud session ("Video editing capabilities")

Desmond (Nov 21): the two sessions work hand in hand. PC on -> the PC session (Desmond's laptop, "Dex Edits video quality
review") does the jobs. PC off -> the cloud session does them. BOTH read this file first and update it (top section) before
stopping, then commit + push. A cloud session cannot message the PC session back, so THIS FILE is how it reports.

## How to pick up
- Rules: ANALYSIS.md (read first), EDITING_RULES.md "NOV 17 RULES" (15-20 s, cold open on the payoff, hook + question +
  👇 captions, F1/MotoGP first, no NASCAR on YouTube), CLAUDE.md (posting, Zernio account IDs, CTA wording).
- Schedule + post IDs: WEEK_NOV16.md. History: POSTED.md. Paid campaigns: CAMPAIGNS.md. Winter plan: OFFSEASON_PLAN.md.
- Sources and the rendered files live on the PC (work/out, sources/); the cloud session works from this repo + the official
  YouTube highlights. Finished videos go in videos/ (GitHub raw URL = the Zernio media URL).

## Status - newest on top
### Sat 21 Nov ~08:45 Lagos (cloud session)
- Read HANDOFF + rules. Zernio state at 08:45: Super Saturday v2 PUBLISHED on both platforms (08:00). NOTHING else is scheduled:
  Sat 12:00 / 18:00, all of Sunday and Monday are empty. The quali edit is not in videos/ yet (latest file = super-saturday-v2).
- I did NOT make the quali edit: no 1080p footage in the cloud container (formula1.com gives 720p only, YouTube downloads are
  blocked) and the Nov 17 rules need the PC engine. Cloud can do: schedule + caption + post IDs in Zernio once an edit is pushed
  (media = raw GitHub URL; YT <= 60 s), reply to comments, pull analytics, update WEEK_NOV16 / POSTED.
- If the PC goes off before the quali edit is pushed, tell Desmond: the 12:00 slot will be empty (cloud cannot render it).
  When it IS pushed (videos/2026-11-21-*), ping the cloud session via Desmond (or it will see it at its next check): it will
  schedule 12:00 on TikTok + YouTube.
- YouTube API quota ran out on Nov 19 (Zernio: "shared daily quota", resets 09:00 Lagos): comment lists/replies on YouTube
  failed until then, posts were not affected. Cloud will poll YouTube comments at most once a day.
- Polls under posts are OFF (Desmond Nov 14). Comment replies: done through Nov 19 on TikTok; YouTube replies pending quota.
- Cloud reminders still armed: Sat 21 08:00 quali (this one), Sun 22 08:00 race edit (cloud has no footage -> will only report).

### Sat 21 Nov ~08:15 Lagos (PC session)
- Las Vegas qualifying (F1 'Qualifying Highlights | 2026 Las Vegas Grand Prix', jiBlTDJ-mFw): Antonelli fastest but a
  5-place grid drop -> Max Verstappen on pole (first Vegas pole), Russell P2 on the grid; team radioed Max "take a P2".
  Both Ferraris out in Q2. Edit engine/edit_cz_vegas26_quali.py (~21 s) RENDERING on the PC -> to post Sat 12:00 (both
  platforms, caption "who wins tomorrow? 👇").
- Still to make today: MotoGP Portimao sprint edit for ~18:00 (sprint ~16:00 Lagos, highlights ~17:00, official MotoGP
  YouTube). Tonight: Sunday 08:00 "race day" hype (grid + lights out 05:00).
- Sunday: F1 Vegas race (05:00 Lagos, highlights ~07:00) -> 12:00 post; MotoGP Portimao race (~15:00) -> 18:00 post.
- Aston Martin x Coinbase paid campaign: joined; waiting for ClipHaus to answer where the footage folder is (asked in their
  Discord #chathaus Nov 18). No clips made yet.
