# HANDOFF - shared status between the PC session and the cloud session ("Video editing capabilities")

Desmond (Nov 21): the two sessions work hand in hand. PC on -> the PC session (Desmond's laptop, "Dex Edits video quality
review") does the jobs. PC off -> the cloud session does them. BOTH read this file first and update it (top section) before
stopping, then commit + push. A cloud session cannot message the PC session back, so THIS FILE is how it reports.

## Report everything (Desmond, Nov 21)
Every action either session takes (download, render, post scheduled/swapped/deleted, comment reply, campaign step, rule
change) gets ONE line in the Status section with the time, then commit + push right away - not only at the end. Start of
every session: `git pull`, read the Status lines written by the other session since your last entry, and tell Desmond what
it did.

## How to pick up
- Rules: ANALYSIS.md (read first), EDITING_RULES.md "NOV 17 RULES" (15-20 s, cold open on the payoff, hook + question +
  👇 captions, F1/MotoGP first, no NASCAR on YouTube), CLAUDE.md (posting, Zernio account IDs, CTA wording).
- Schedule + post IDs: WEEK_NOV16.md. History: POSTED.md. Paid campaigns: CAMPAIGNS.md. Winter plan: OFFSEASON_PLAN.md.
- Sources and the rendered files live on the PC (work/out, sources/); the cloud session works from this repo + the official
  YouTube highlights. Finished videos go in videos/ (GitHub raw URL = the Zernio media URL).

## Status - newest on top
### Sat 21 Nov 22:35 Lagos (PC session)
- 21:50 Desmond: v1 mood edit "not the same as the references, song too moody, they have MULTIPLE bikes". Measured the refs' music:
  bass-heavy instrumentals 89-125 BPM, loud - not a sad ballad.
- 22:26 RENDERED mood v2: packs/battles only (start funnel, pack through corners, three-wide, two-bike battles), no faces, no
  celebrations, no text; Montagem Kali (slowed), cut every 4 beats (~2.35 s), slow-mo, 16.2 s. (First try at every=6 ran 25 min -> stopped.)
- 22:33 DELETED v1 Sun 08:00 posts (YT 6b0200a4308ecb7edb59fb8f / TT 6b0200a643fb56d79b263199), SCHEDULED v2 Sun 22 08:00:
  YT 6b020ce19c9046eb10fce9eb / TT 6b020ce3e7cfa6d2603f9c95 (videos/2026-11-22-portimao-mood-v2-25.mp4).
- Mood renders are slow on the PC (AI slow-mo at 720x1280: ~15-18 min for 16 s) - start them early.

### Sat 21 Nov 21:40 Lagos (PC session)
- 20:45 Desmond sent 5 'mood' trackside TikToks (100-200K views) -> studied, saved as REFERENCES AE1-AE5 + EDITING_RULES "MOOD EDIT".
- 21:00 Desmond: "change tomorrow's edit to this type". NEW engine/mood.py: full-screen 9:16 at 720x1280, slow motion (RIFE),
  one cut per 2 beats, no text/commentary/banner, small DEX EDITS mark, end card.
- 21:30 RENDERED engine/edit_dc_portimao_mood.py (17.2 s, Purple Rain intro, 2025 Portimao footage).
- 21:38 DELETED the Sun 08:00 card hype (YT 6b01ef66dc03baa3505850c0 / TT 6b01ef68a6f03a00ca2f7dac) and SCHEDULED the mood edit
  Sun 22 08:00: YT 6b0200a4308ecb7edb59fb8f / TT 6b0200a643fb56d79b263199. Caption: "race day at portimao. who takes it? 👇".

### Sat 21 Nov 20:25 Lagos (PC session) - PC back online
- 20:10 Read the cloud's lines: Bezzecchi lap-record edit posted Sat 18:50; POST DIRECTLY rule noted.
- 20:12 Sun 08:00 plan changed: NO F1 race-day hype (the Vegas race ends ~07:00, before 08:00) -> MotoGP race-day hype instead.
- 20:19 RENDERED engine/edit_db_portimao_race_day.py (lyric cards, 15.0 s, Can I Ride) on 2025 Portimao race footage (vP51RMuSUsk):
  RACE DAY / BEZZECCHI pole + all-time lap record / MARC P2 on the grid / LAST YEAR Bezzecchi won here / RACE TODAY who takes it?
- 20:24 SCHEDULED Sun 22 08:00 (Desmond asked to post it tomorrow, not now): YT 6b01ef66dc03baa3505850c0 / TT 6b01ef68a6f03a00ca2f7dac.
- NEXT Sunday: 12:00 F1 Vegas race edit (F1 YouTube highlights ~07:00 - PC if on in the morning, else cloud);
  18:00 MotoGP Portimao race edit (race ~15:00 - PC if on in the evening, else cloud).

### Sat 21 Nov 18:40 Lagos (cloud session)
- 18:40 NEW RULE (Desmond): once an edit passes QC (picture + audio), PUBLISH IT DIRECTLY on both platforms (publish_now), then just tell Desmond it is live - no file to send. Added to CLAUDE.md (Posting).

### Sat 21 Nov 18:35 Lagos (cloud session)
- 18:05 motogp.com: today's sprint videos (sprint highlights, full sprint, 'Marc tumbles out of sprint', FP2/Q1/Q2) are VideoPass-only
  (403 user_not_granted). FREE today: 'Last 5 mins: Bezzecchi blazes to record-breaking pole' (1266837), onboard record lap (1266932),
  Q2 reactions (1266843). Downloaded the first two (1080p50) to the cloud scratch.
- 18:30 RENDERED engine/edit_da_bezzecchi_portimao_record.py (master.py, 21.8 s, song #162): Bez takes Marc's 2023 all-time lap record
  "by a whisker" + knocks Marc to P2 on the grid. Files: videos/2026-11-21-bez-portimao-record-25.mp4 (+ -yt1440). Pushed.
- 18:33 SCHEDULED Sat 18:50 Lagos (17:50 UTC): YT 6b01d5b2ae8ad5be91d943cc (title "Bezzecchi takes Marc's all-time Portimao lap record")
  / TT 6b01d5b69414bcef0cfb439d. Caption mentions Marc crashing out of the sprint (motogp.com headline) + "who wins tomorrow? 👇".
- NOT made: Sunday 08:00 race-day hype. Sunday plan if the PC is still off: F1 Vegas race edit from formula1.com (720p, only F1 source
  the cloud can reach) for 12:00; MotoGP race highlights will likely be VideoPass-locked -> cloud uses whatever free clip motogp.com has.

### Sat 21 Nov 17:55 Lagos (cloud session) - PC offline, cloud takes over (Desmond: "do your best edit and schedule it")
- 17:55 Zernio: Vegas quali (12:00) PUBLISHED on both. Nothing scheduled after it. PC logged nothing after 08:30.
- 17:55 START: MotoGP Portimao sprint edit (source: motogp.com official video, 1080p DASH - works from the cloud), NOV 17 rules,
  target post ~19:30 Lagos today (18:00 slot already missed).

### Sat 21 Nov 08:25 Lagos (cloud session) - log every action, one line each
- 08:25 Rule received (Desmond, via PC session): log EVERY action here right away (download, render, post scheduled/swapped/deleted,
  comment reply, campaign step, rule change); at session start pull + read the other session's lines and tell Desmond. Following it.
- 08:25 Pulled + read the PC lines: Vegas quali edit scheduled Sat 12:00 (YT 6b0147277fe923bccaec0fdb / TT 6b01472848ac025f65748ec4).
  Cloud did not touch it. (Correction: my entry below is timed "~08:45", real time was ~08:20 Lagos.)
- 08:25 Cloud actions so far today, all logged: none besides the HANDOFF status entry below. Nothing posted, swapped or deleted by cloud.
- Earlier cloud actions (before this rule), for the record: Nov 19 TikTok comment replies x1 (Max 2016/Lewis 2026 post); Nov 17 TikTok replies x4;
  Nov 14 poll check-in disabled (trigger) + CLAUDE.md poll rule removed + ANALYSIS.md added; Nov 15 "Make Mon16-Wed18 posts" trigger disabled.

### Sat 21 Nov 08:30 Lagos (PC session)
- DONE: Vegas quali edit scheduled Sat 12:00 (YT 6b0147277fe923bccaec0fdb / TT 6b01472848ac025f65748ec4).
- NEXT: MotoGP Portimao sprint edit for ~18:00 (highlights ~17:00); Sunday 08:00 race-day hype tonight.
- Note: the Claude app froze ~08:20 (app restart, not the PC); battery 41% discharging.

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
