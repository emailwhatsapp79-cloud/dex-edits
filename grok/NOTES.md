# grok-trial — 18 Oct 2026

Three new edits. Nothing already posted was changed. No audio files in this repo.
30 fps only: the car film is 25 fps, the F1 highlights are 50 fps, the TikToks are ~30 fps.
None of those is a 60 fps master, so there is no 60 fps export.

Cut-to-beat error is the rendered cut frame versus the nearest drum hit.
One frame is 33 ms. Nothing below is late by more than one frame.

## CAR — Mission S on the pier

`grok/2026-10-18-mission-s-pier.mp4` (TikTok, 1920x1080) and `grok/mission-s-pier-yt.mp4` (YouTube Short).

One car, one place. The Mission S world premiere on a Queens pier with Manhattan behind it:
the car arrives, the details (rear, lamp, nose, side, wheel), then the hero front.
Refs N7 / N9 / N12. Song **#91** `91_porsche_911_gt3_cup_sav_edits001` (130 bpm).
LIBRARY has no lyric line for #91; N12 used this same sound as an instrumental, and that is how it is cut here.

- Source: official Porsche newsroom film, 4K 25 fps, downscaled to 1920x1080. No crop, no upscale.
  https://newstv.porsche.com/porschevideos/newstv.porsche.com_341406_en.mp4
- Script: `engine/grok_mission_s_pier.py`
- Length: 18.0 s
- Worst cut error: 15 ms early (the rear at 10.03 s). The rest are within 13 ms.
- Soft defocus takes in the film (around 46 s, 51 s and 55 s) were left out. The Porsche end card is not used.

Shot list (edit time → source time): 0.00→14.55 MISSION S, 1.86→11.95 pier, 3.51→38.70 rear,
5.33→63.45 lamp, 7.28→69.15 nose, 8.67→58.20 side, 10.03→80.80 rear, 11.59→61.05 flank,
13.24→74.90 wheel, 15.12→88.10 pier, 16.51→92.50 hero front.

Caption: Mission S. One night on a Queens pier. Would you take this over a 911?
#carsoftiktok #caredit #fyp #porsche #missions

## FOOTBALL — Dembélé, the 10

`grok/2026-10-18-dembele-the-10.mp4` (already vertical, so no separate Shorts file).

One player. The number 10: first World Cup goal, then the hat-trick. The drop of the song
cuts to the hat-trick. Source commentary is muted so the on-screen words are not fighting a voice.
Song **#37** `37_montagem_rune_slowed` (97 bpm). Instrumental until "thank you for watching" at 16.5 s,
and the edit is over before that.

- Sources, official @fifaworldcup, native 1080x1920, nothing cropped or scaled:
  - first goal https://www.tiktok.com/@fifaworldcup/video/7654401416228031747
  - hat-trick https://www.tiktok.com/@fifaworldcup/video/7666790102982495510
- Script: `engine/grok_dembele_the_10.py`
- Length: 13.5 s
- Worst cut error: 9 ms late. All five cuts are inside one frame of the hit. The drop cut (7.43 s) is 9 ms after the hit at 7.424 s.
- Why it is not ~20 s: the hat-trick TikTok is 6.7 s with one cut in it, and each side is used once.
  Padding it (a freeze, a repeated take, a slower fake) would break the rules. 13.5 s is inside 12–22 s and it ends on the celebration.

Shot list: 0.00 THE 10 (first-goal clip 4.45), 1.89 the strike (6.45), 4.36 FIRST (9.20),
7.42 AGAIN (hat-trick 0.35), 9.89 the finish (2.86, stops before the clip's own cut at 3.84),
10.83 HAT-TRICK (4.02).

Caption: Dembélé. The 10. First World Cup goal, then the hat-trick. Who else is wearing 10 like that?
#football #footballedit #fyp #worldcup #dembele

## F1 — Up next is Austin

`grok/2026-10-18-austin-up-next.mp4` (TikTok, 1280x720) and `grok/austin-up-next-yt.mp4` (YouTube Short).

Race-week formula (refs M6, M15, M22) for the next Grand Prix after 18 Oct 2026:
round 18, United States GP, Circuit of the Americas, Austin, 23–25 Oct (race on the 25th).
The 2026 race has not been run, so the pictures are the official 2025 United States GP highlights,
kept at native 1280x720. No crop, no upscale. Song **#5** `05_montagem_kali_slowed` (102 bpm), instrumental,
so the city, the round and the dates are ours — not another race's commentary.

- Source: https://www.formula1.com/en/video/race-highlights-2025-united-states-grand-prix.1846447535630260620
  Brightcove `videoId=1846447535630260620`
- Script: `engine/grok_austin_up_next.py`
- Length: 18.1 s
- Worst cut error: 25 ms early (5.63 s, one frame early of the hit at 5.658 s). No cut is late.
- The first 1.8 s is a close car, not the aerial. Panning smears in the highlights were not used.
  Official highlights still carry a small position bug in the corner. That is the source, not a title card we added.

Shot list (edit time → source time): 0.00→160.20 UP NEXT, 1.83→7.00 AUSTIN, 3.90→34.20 ROUND 18,
5.63→48.20 23-25 OCT, 7.10→170.30, 8.57→198.00, 10.33→231.00, 11.80→207.20, 13.27→258.00,
14.17→320.40, 15.03→400.20, 15.90→434.20 RACE, 16.47→458.00 WEEK.

Caption: Up next is Austin. What are we getting this weekend?
#f1 #formula1 #f1edit #fyp #austin
