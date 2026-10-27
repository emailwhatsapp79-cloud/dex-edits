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

# v2 — 18 Oct 2026

The three edits above are the first cut. They stay in the branch. v2 is the cut to watch. Nothing was scheduled.

## CAR v2 — Mission S, the studio

`grok/2026-10-18-mission-s-studio-v2.mp4` (1920x1080) and `grok/2026-10-18-mission-s-studio-v2-yt.mp4` (YouTube Short).

One car, one room. The newsroom film also has the pier, a 1953 550 Spyder, the launch crowd and the Brooklyn Bridge. None of those are in this cut. Studio only: the rear, the light bar, the wheel, the cockpit, the gauges, the gear, the badge, the engine deck, then the hero rear. Refs N7 / N9 / N12. Song **#91** `91_porsche_911_gt3_cup_sav_edits001` (130 bpm), instrumental.

- Source: official Porsche newsroom, 4K 25 fps, downscaled to 1920x1080. No crop, no upscale.
  https://newstv.porsche.com/porschevideos/newstv.porsche.com_341406_en.mp4
- Script: `engine/grok_mission_s_studio_v2.py`
- Length: 16.5 s
- Worst cut error: 17 ms early (the light bar at 3.00 s, hit at 3.017 s). Nothing is late by more than 6 ms.

Shot list (edit time → source time): 0.00→60.12 MISSION S, 3.00→55.20 light bar, 5.33→67.02 wheel,
6.20→63.80 cockpit, 8.20→72.25 gauges, 10.03→77.42 gear, 11.13→79.15 badge, 12.50→81.15 deck, 14.40→88.20 hero.

Caption: Mission S. Same car, same room, nothing else in the cut. Would you take it over a 911?
#carsoftiktok #caredit #fyp #porsche #missions

## FOOTBALL v2 — Kevin Pina, from range

`grok/2026-10-18-pina-way-out-v2.mp4` (already vertical).

One player, one goal. The strike is from distance, the drop is the goal, and the celebration is held to the fade. Not Dembélé. Not a red number 19.

Proof, all three shots are the same official post (three takes, no repeated range):
- Post: https://www.tiktok.com/@fifaworldcup/video/7693949914702679318
- Caption: "Kevin Pina from WAY out" #FIFAWorldCup
- On screen: Cape Verde in red, Uruguay in sky blue. The celebration ends on a red 6, which is his 2026 number. A teammate in 5 is also in the huddle, so the edit does not stamp a number over the pile.
- Native 1080x1920, nothing cropped or scaled. Source commentary is muted.
- Song **#37** `37_montagem_rune_slowed`. Instrumental until "thank you for watching" at 16.48 s. The edit ends at 15.77 s, before that line.
- Script: `engine/grok_pina_way_out_v2.py`
- Length: 15.8 s
- Worst cut error: 9 ms late (the goal at 7.43 s, the drop is 7.424 s). The celebration cut is 7 ms late.

Shot list: 0.00 PINA / WAY OUT (source 2.40, the range, through the strike), 7.43 GOAL (source 10.18, the net), 10.83 the celebration held (source 14.30).

Caption: Pina. From range. Then he stayed there. Who else is scoring them like that?
#football #footballedit #fyp #worldcup #pina

## F1 v2 — Max, first Singapore win

`grok/2026-10-18-max-singapore-v2.mp4` (already vertical, official @f1).

Not Austin, not a race week, no lap counter and no position tower. M21 shape: black cards on the beat (MAX / SINGAPORE / FIRST WIN), then one driver in black and white — the car, the helmet, the track, and the trophy held. Singapore 2026 was 11 October. He won it from pole. That is the story. Ferrari's podium and Antonelli are not this edit.

- Source: official @f1, native 1080x1920, 50 fps mastered at 30. No crop, no upscale.
  https://www.tiktok.com/@f1/video/7696506664224296214
  Caption: "it was a weekend of going from strength to strength for max"
- The file carries a small Friday / Saturday / Sunday tag and the F1 bug. Shots with a lap number, a position board or a panning smear were left out. Song **#5** `05_montagem_kali_slowed` is instrumental, so the cards are not fighting a voice.
- Script: `engine/grok_max_singapore_v2.py`
- Length: 15.0 s
- Worst cut error: 15 ms late (the track shot at 8.60 s, hit at 8.585 s). Nothing else is later than 10 ms.

Shot list: 0.00 MAX, 1.83 SINGAPORE, 3.90 FIRST WIN, 5.67 the car (source 0.45), 7.13 the helmet (source 2.40), 8.60 the track (source 8.92), 11.23 the trophy (source 39.72, held).

Caption: Max. First time in Singapore. He did not give that one back.
#f1 #formula1 #f1edit #fyp #maxverstappen

# v3 — 18 Oct 2026

Three more cuts. v1 and v2 stay in the branch. Nothing was scheduled.
TikTok files are 30 fps. The two horizontal F1 edits also have a YouTube Short at the source rate, 50 fps.
`engine/ytshort.py` takes an optional 4th argument for that. `engine/wideedit.py` reads `DEX_FPS` and stays at 30 when it is unset.

## FOOTBALL v3 — Wilson Isidor, top corner

`grok/2026-10-24-isidor-top-corner.mp4` — 1080x1920, 30 fps, 15.03 s, 27.6 MB.
No YouTube file. The source is 30 fps.

One player, one goal. The first frame is the strike in the top corner, then a rewind to the build-up, then the celebration held through the fade. No number is stamped. The pile has other shirts in it.

Proof:
- Post: https://www.tiktok.com/@fifaworldcup/video/7694302696496532758
- Caption: "Straight into the top corner from Isidor"
- On screen: Haiti in blue, Morocco in red. The celebration is a blue 18, which is Wilson Isidor's 2026 number (Sunderland). The same pile shows Lenny Joseph 16 and Danley Jean Jacques 17, who are his teammates, plus 22, 4 and 5. So the edit says ISIDOR and never a number. The surname is not claimed off the shirt. The name is the caption, the 18, and that roster.
- Native 1080x1920. Nothing cropped or scaled. Source commentary is muted.
- Song **#5** `05_montagem_kali_slowed`. Instrumental. The edit ends at 15.03 s.
- Script: `engine/grok_isidor_top_corner_v3.py`
- Worst cut error: 25 ms early (the rewind at 5.633 s, hit 5.658 s, and the pile at 12.633 s, hit 12.658 s). Nothing is late.

Shot list: 0.00 the strike (source 8.10, ISIDOR / TOP CORNER), 2.87 the build-up (source 1.00, ISIDOR only), 5.63 the run (source 11.49, blue 18), 10.33 the pile (source 16.26), 12.63 the pile held (source 18.62).

Caption: Isidor. Top corner. Then he stayed there.
#football #footballedit #fyp #worldcup #isidor

## F1 v3 — Around the world

`grok/2026-10-24-around-the-world.mp4` — 1280x720, 30 fps.
`grok/2026-10-24-around-the-world-yt.mp4` — 1080x1920, 50 fps.
Master rendered with `DEX_FPS=50`. TikTok is `brand.py` at 30. YouTube is `ytshort.py` at 50.

One 2026 track per shot. Monaco harbour, then the Barcelona start, the Sepang crowd, and a Singapore night aerial. The vocal is one line. The bracket waits for the word, then stays.

- Song **#100** `100_simple_edit_mb_i_ve_been_busy_scp_piastr` (115 bpm, 20.5 s). Words: 0.00 Bound, 1.68 the, 1.98 Wheels, 2.46 Around, 3.10 the, 3.92 World. Nothing on screen contradicts that. [AROUND] at 2.46, [AROUND THE] at 3.10, [AROUND THE WORLD] from 3.92 to the fade.
- Sources, official formula1.com 2026 race highlights, 1280x720, 50 fps, kept 1:1. No crop, no upscale.
  - Monaco https://www.formula1.com/en/video/race-highlights-2026-monaco-grand-prix.1867355748376897082
  - Barcelona id 1867987150306679134
  - Sepang id 1878118714727462605
  - Singapore https://www.formula1.com/en/video/race-highlights-2026-singapore-grand-prix.1878763614925929557
- No lap counter and no timing tower. A small F1 bug and trackside boards (Pirelli, MSC, Formula 1 hoardings) are in some frames. Monza was left out: a RACE bug is on the grid by 2.2 s. The Singapore reel has a red SINGAPORE banner around 106 s, so that piece starts after it.
- These source ranges are not the ones in the lights-out cut, and they are not the ranges in the greatest-show edit.
- Script: `engine/grok_around_the_world_v3.py`
- Length: 15.28 s
- Worst cut error: 18 ms early (Sepang at 9.780 s, hit 9.798 s). The night aerial is held across the 13.87 s hit. Nothing is late.

Shot list: 0.00 Monaco harbour (source 459.90), 5.82 Barcelona (source 1.18), 9.78 Sepang (source 14.32), 11.68 Singapore night (source 107.55, held).

Caption: Around the world. One lap of it.
#f1 #formula1 #f1edit #fyp #aroundtheworld

## F1 v3 — Lights out

`grok/2026-10-25-lights-out.mp4` — 1280x720, 30 fps, 15.04 s.
`grok/2026-10-25-lights-out-yt.mp4` — 1080x1920, 50 fps, 15.04 s.
Same split as the other F1 cut. `DEX_FPS=50`, then brand at 30 and `ytshort.py` at 50.

The five reds are on at frame 0 and out before 1.2 s. Then 2026 starts from five other tracks. The last shot is held, and the line is AUSTIN. TODAY. There is no picture of Austin. Austin 2025 is not in it. Las Vegas 2026 has not been run.

- Song **#5** `05_montagem_kali_slowed`. Instrumental, so the cards are not fighting a voice.
- Sources, official formula1.com 2026 race highlights, 1280x720, 50 fps, kept 1:1.
  - Monaco https://www.formula1.com/en/video/race-highlights-2026-monaco-grand-prix.1867355748376897082
  - Singapore https://www.formula1.com/en/video/race-highlights-2026-singapore-grand-prix.1878763614925929557
  - Austria id 1869253533864637800
  - Sepang id 1878118714727462605
  - Baku id 1877401243065210101
  - Madrid (Spanish GP) id 1876231054932125334
- No lap counter, no position tower, no RACE bug. A small F1 bug stays, and so do trackside sponsors (Louis Vuitton, Singapore Airlines, Lenovo, Gulf Air, Qatar Airways, TAG Heuer). The "12" on the Madrid gantry is the start-light board, not a lap.
- Script: `engine/grok_lights_out_v3.py`
- Worst cut error: 18 ms early (Sepang at 5.640 s, hit 5.658 s). 1.840 and 3.900 land on the hit. Nothing is late.

Shot list: 0.00 Monaco lights (source 3.22), 1.84 Singapore (source 6.94), 3.90 Austria (source 1.50), 5.64 Sepang (source 3.40), 8.58 Baku (source 1.70), 10.34 Madrid, held (source 4.32, AUSTIN. TODAY.).

Caption: Lights out. Austin, today.
#f1 #formula1 #f1edit #fyp #lightsout

# v4 — 18 Oct 2026

v3 of around-the-world stays in the branch. It was four shots and a long Monaco hold, so it felt slow. v4 is the same song cut on the beat. Nothing was scheduled.

## F1 v4 — Around the world

`grok/2026-10-24-around-the-world-v4.mp4` — 1280x720, 30 fps, 17.74 s, 26.3 MB.
`grok/2026-10-24-around-the-world-v4-yt.mp4` — 1080x1920 Short, 50 fps, 17.74 s, 26.0 MB. Title AROUND THE WORLD / F1 2026.

The 2026 season, one car at speed, a different place every cut. Eight tracks. The hook is an onboard at Melbourne, not a hold and not a title card. Song **#100** `100_simple_edit_mb_i_ve_been_busy_scp_piastr`, 115 bpm, so a beat is 0.522 s. Before the drop the cut is every two beats. From 11.38 s it is every beat. 21 shots. Nothing is longer than 1.48 s. The phrase AROUND THE WORLD is on screen from 2.46 s (the word "Around" in LIBRARY) through 4.20 s (just after "World" at 3.92 s). After that, only the track name, small, Anton, black border.

Official formula1.com race highlights, 1280x720, 50 fps, kept 1:1. No lap counter, no timing tower, no RACE bug, no replay wipe. A small F1 logo and the trackside boards stay. None of these ranges are the lights-out shots, and none of them are Austin.

- Melbourne https://www.formula1.com/en/video/race-highlights-2026-australian-grand-prix.1859073701054990671
- Shanghai https://www.formula1.com/en/video/race-highlights-2026-chinese-grand-prix.1859720122095299762
- Suzuka https://www.formula1.com/en/video/race-highlights-2026-japanese-grand-prix.1860981885174442903
- Miami https://www.formula1.com/en/video/race-highlights-2026-miami-grand-prix.1864198818823907914
- Silverstone https://www.formula1.com/en/video/race-highlights-2026-british-grand-prix.1869893362466065062
- Spa https://www.formula1.com/en/video/race-highlights-2026-belgian-grand-prix.1871156468094962300
- Hungaroring https://www.formula1.com/en/video/race-highlights-2026-hungarian-grand-prix.1871795237413048481
- Singapore https://www.formula1.com/en/video/race-highlights-2026-singapore-grand-prix.1878763614925929557

Script: `engine/grok_around_the_world_v4.py`

Cuts measured with `beatsync.video_cuts` on the 50 fps master against the hits in song #100. Offset is cut minus the hit it was snapped to. One frame at 50 fps is 20 ms. Worst is 19 ms early. Nothing is late.

| edit | hit | offset | track | source |
|---|---|---|---|---|
| 1.080 | 1.085 | -5 ms | SUZUKA | japan 8.05 |
| 2.160 | 2.175 | -15 ms | MIAMI | miami 8.20 |
| 3.160 | 3.179 | -19 ms | SILVERSTONE | britain 20.60 |
| 4.200 | 4.210 | -10 ms | SPA | belgium 14.80 |
| 5.260 | 5.264 | -4 ms | SHANGHAI | china 12.20 |
| 6.300 | 6.303 | -3 ms | SINGAPORE | singapore 104.20 |
| 7.380 | 7.380 | 0 | HUNGARY | hungary 12.50 |
| 8.380 | 8.397 | -17 ms | MIAMI | miami 24.05 |
| 9.340 | 9.347 | -7 ms | SILVERSTONE | britain 15.55 |
| 10.440 | 10.452 | -12 ms | SPA | belgium 30.55 |
| 11.380 | 11.398 | -18 ms | SHANGHAI | china 33.15 |
| 11.920 | 11.923 | -3 ms | HUNGARY | hungary 23.70 |
| 12.420 | 12.436 | -16 ms | MELBOURNE | australia 26.30 |
| 12.940 | 12.954 | -14 ms | SUZUKA | japan 17.80 |
| 13.460 | 13.478 | -18 ms | SILVERSTONE | britain 33.20 |
| 14.020 | 14.036 | -16 ms | MIAMI | miami 27.20 |
| 14.600 | 14.604 | -4 ms | HUNGARY | hungary 30.20 |
| 15.140 | 15.145 | -5 ms | SUZUKA | japan 25.80 |
| 15.720 | 15.726 | -6 ms | SHANGHAI | china 23.40 |
| 16.260 | 16.272 | -12 ms | SPA | belgium 19.35, held to 17.74 |

Opens at 0.00 on the Melbourne onboard (australia 12.40).

Caption: Around the world. Eight races, one pass each, no waiting around.
#f1 #formula1 #f1edit #fyp #aroundtheworld

# v5 — 18 Oct 2026

v4 stays in the branch. The pace was right. The graphics were not. The Melbourne open was a replay, and 17 of the 21 shots carried the black FIA lap card. v5 is the same song, the same 21 cuts, the same text. Every shot is a new window from the same eight highlights. Nothing was scheduled.

## F1 v5 — Around the world

`grok/2026-10-24-around-the-world-v5.mp4` — 1280x720, 30 fps, 17.74 s, 26.3 MB.
`grok/2026-10-24-around-the-world-v5-yt.mp4` — 1080x1920 Short, 50 fps, 17.74 s, 26.0 MB. Title AROUND THE WORLD / F1 2026.
`grok/around-the-world-v5-corners.jpg` — the top-left 260x130 of every shot, native, no scale.

The hook is a Suzuka onboard at speed, not the Melbourne replay. Song **#100** `100_simple_edit_mb_i_ve_been_busy_scp_piastr`, 115 bpm. Before the drop the cut is every two beats. From 11.38 s it is every beat. 21 shots. Nothing is longer than 1.48 s. AROUND THE WORLD is on screen from 2.46 s through 4.20 s. After that, only the track name, small, Anton, black border.

Official formula1.com race highlights, 1280x720, 50 fps, kept 1:1. No crop, no upscale. These packages keep the LAP card, or a red REPLAY tag, up for almost the whole race. The windows below are the ones where a 260x130 corner crop is only the small F1 logo. That was counted on the pixels (logo present, no lap text, no red REPLAY word), then the corner sheet was looked at. A red flash inside the Spa onboard is a track post going past the logo, not a REPLAY word. None of these ranges are the v4 ranges, the lights-out shots, or Austin.

- Melbourne https://www.formula1.com/en/video/race-highlights-2026-australian-grand-prix.1859073701054990671
- Shanghai https://www.formula1.com/en/video/race-highlights-2026-chinese-grand-prix.1859720122095299762
- Suzuka https://www.formula1.com/en/video/race-highlights-2026-japanese-grand-prix.1860981885174442903
- Miami https://www.formula1.com/en/video/race-highlights-2026-miami-grand-prix.1864198818823907914
- Silverstone https://www.formula1.com/en/video/race-highlights-2026-british-grand-prix.1869893362466065062
- Spa https://www.formula1.com/en/video/race-highlights-2026-belgian-grand-prix.1871156468094962300
- Hungaroring https://www.formula1.com/en/video/race-highlights-2026-hungarian-grand-prix.1871795237413048481
- Singapore https://www.formula1.com/en/video/race-highlights-2026-singapore-grand-prix.1878763614925929557

Script: `engine/grok_around_the_world_v5.py`

Cuts measured with `beatsync.video_cuts` on the 50 fps master against the hits in the original song #100 mp3. Offset is the cut minus the hit it was snapped to. One frame at 50 fps is 20 ms. Worst is 19 ms early. Nothing is late. The fade near 17.6 s is not a cut.

| edit | hit | offset | track | source |
|---|---|---|---|---|
| 1.080 | 1.085 | -5 ms | SINGAPORE | singapore 112.72 |
| 2.160 | 2.175 | -15 ms | MELBOURNE | australia 18.75 |
| 3.160 | 3.179 | -19 ms | SINGAPORE | singapore 97.22 |
| 4.200 | 4.210 | -10 ms | SUZUKA | japan 3.42 |
| 5.260 | 5.264 | -4 ms | SINGAPORE | singapore 91.50 |
| 6.300 | 6.303 | -3 ms | HUNGARY | hungary 228.75 |
| 7.380 | 7.380 | 0 | SINGAPORE | singapore 116.55 |
| 8.380 | 8.397 | -17 ms | SILVERSTONE | britain 312.38 |
| 9.340 | 9.347 | -7 ms | SINGAPORE | singapore 88.68 |
| 10.440 | 10.452 | -12 ms | MELBOURNE | australia 16.92 |
| 11.380 | 11.398 | -18 ms | SINGAPORE | singapore 120.40 |
| 11.920 | 11.923 | -3 ms | SINGAPORE | singapore 102.26 |
| 12.420 | 12.436 | -16 ms | SHANGHAI | china 13.36 |
| 12.940 | 12.954 | -14 ms | SINGAPORE | singapore 94.80 |
| 13.460 | 13.478 | -18 ms | SPA | belgium 334.96 |
| 14.020 | 14.036 | -16 ms | SINGAPORE | singapore 130.48 |
| 14.600 | 14.604 | -4 ms | SPA | belgium 5.20, the grid |
| 15.140 | 15.145 | -5 ms | SINGAPORE | singapore 133.42 |
| 15.720 | 15.726 | -6 ms | MIAMI | miami 2.20 |
| 16.260 | 16.272 | -12 ms | SINGAPORE | singapore 124.42, held to 17.74 |

Opens at 0.00 on the Suzuka onboard (japan 416.50).

Singapore is most of the logo-only racing in these eight films, so it comes back. The green Mercedes is three of those shots, each from a different cut between the lap stings, not one repeated range. 11.38 and 11.92 are both Singapore on purpose: a side pass, then a Haas onboard. There is no 21st clean at-speed shot on another track, so 14.60 is the Spa grid, live, logo only, half a second. Miami is the safety-car train. That is the whole clean Miami reel. Shanghai is the cars on the straight at 13.36, after v4's window.

Caption: Around the world. Eight races, cut on the beat.
#f1 #formula1 #f1edit #fyp #aroundtheworld

# Oct 26 — 18 Oct 2026

Three edits. Nothing scheduled. M26 and N17 are not in REFERENCES.md (it stops at M24). The F1 text is the M26 idea taken from the flow edit itself, drawn sharp, with none of its blur. The car edit is the one-colour profile the brief asked for. N10 in the repo is a CGI one-colour world. This one is a real press film.

## FOOTBALL — Salah

`grok/2026-10-26-salah.mp4` — 1080x1920, 30 fps, 4.87 s, 27.0 MB.
No YouTube file. The source is 29.97, not 50 or 60.
`grok/salah-corners.jpg` — top-left and bottom-left 260x130 of the run, the strike, the net and the arms. Crowd and grass. No score bug.

Egypt 1–2 up against New Zealand, BC Place, Vancouver, 21 June 2026. The go-ahead, 67th minute, after a one-two. Number 10, red. Official @fifaworldcup, native vertical, kept 1:1.

https://www.tiktok.com/@fifaworldcup/video/7654129160910097686

The live angle is one camera and it ends just after 5.4 s, when the clip cuts to a replay of the same goal. The replay is not used. The 60-second FIFA highlight of the same match has a score bug in the corner the whole way, so that celebration close-up was left out. What is here is the run, the strike, the ball in the net, and his arms-wide finish, in that order, and the edit ends on the arms. It is short because that is the clean take.

Song **#4** `04_legacy_phonk_108bpm`. The vocal ("they hate on me") starts at 17.8 s. This edit uses 0.00–4.86 s. Instrumental.

Script: `engine/grok_salah.py`

Cuts are the frame the new shot starts. The two angles are the same wide camera, so the automatic detector only flags the harder change inside the celebration. The frame difference is at 2.167 and 4.433. One frame at 30 fps is 33 ms. Both are early.

| edit | hit | offset | what |
|---|---|---|---|
| 2.167 | 2.198 | -31 ms | the one-two, source 2.70 |
| 4.433 | 4.460 | -27 ms | arms wide, source 5.02, held to 4.86 |

Opens at 0.00 on the run (source 0.20). SALAH. is on from the first frame. THE GO-AHEAD. comes on as the shot is struck.

Caption: Salah. The go-ahead in Vancouver. Did you see the one-two?
#football #footballedit #fyp #worldcup #salah

## F1 — I get it

`grok/2026-10-26-i-get-it.mp4` — 1280x720, 30 fps, 10.90 s, 25.5 MB.
`grok/2026-10-26-i-get-it-yt.mp4` — 1080x1920 Short, 50 fps, 10.90 s, 24.1 MB. Title I GET IT / MAX VERSTAPPEN.
`grok/i-get-it-corners.jpg` — top-left and bottom-left of every shot. The small F1 logo only. No lap card, no replay word.

Library has no file #105. The sound is the 11.8 s recording on the flow edit that uses this text (https://www.tiktok.com/@aep.quin/video/7568164152951311638). That video is not the footage. The stamps sit on the kicks in this recording: 0.48, 2.80, 5.34, 7.36. The voice peaks about a fifth of a second later, so the words are up as the line is sung. White vertical bar, IT over GET, Anton. The third stamp (5.34) is gold. A thin double frame punches in on the hit and is gone in half a second. No blur.

The hook is tyre smoke. It is the 2023 Abu Dhabi #1 donuts, the season-finale laps, not the race the title was decided in. That is the official donut film with the smoke in the first frame. Said plainly so it is not billed as the title-clinch.

- 2023 Abu Dhabi donuts, formula1.com, Brightcove 1783637921051439731. Smoke 1.60, arms 12.60, helmet off 16.20.
- 2022 Abu Dhabi donuts, formula1.com, Brightcove 1750030099497815599. Smoke 5.40.
- https://www.formula1.com/en/video/2026-bahrain-grand-prix-verstappen-crosses-the-line-to-take-his-first-win-of-the-season.1878116592061332264 — head-on 0.30, the car along the straight 1.70. Sepang, his first win of 2026.
- https://www.formula1.com/en/video/2026-singapore-grand-prix-verstappen-crosses-the-line-to-take-his-first-singapore-gp-win.1878763527671997097 — the finish straight 0.40. The rest of that clip is team radio with burned subtitles, so it is not used.

All four are 1280x720, kept 1:1. No source twice in a row. The donut film is used three times, from three different ranges.

Script: `engine/grok_i_get_it.py`

Cuts measured on the 50 fps master against the wav, not the AAC and not the Short. One frame at 50 fps is 20 ms. The stamp leaving at 5.88 is not a cut. 7.16 and 8.74 are cuts. The night shots sit under the detector's bar (frame diff 20 and 22). They are on the hits.

| edit | hit | offset | what |
|---|---|---|---|
| 1.640 | 1.647 | -7 ms | Sepang, head-on |
| 2.780 | 2.787 | -7 ms | 2022 smoke |
| 3.800 | 3.801 | -1 ms | arms up |
| 5.320 | 5.328 | -8 ms | the car, side-on. Gold stamp at 5.34 |
| 7.160 | 7.168 | -8 ms | helmet off |
| 8.740 | 8.746 | -6 ms | Singapore, held to 10.90 |

Opens at 0.00 on the smoke (donuts 1.60).

Caption: I get it. The smoke, then the line. Did he?
#f1 #formula1 #f1edit #fyp #verstappen

## CAR — one colour

`grok/2026-10-26-one-colour.mp4` — 1920x1080, 30 fps, 6.44 s, 25.2 MB.
`grok/2026-10-26-one-colour-yt.mp4` — 1080x1920 Short, 25 fps, 6.44 s, 17.1 MB. No title on the picture.
`grok/one-colour-corners.jpg` — top-left and bottom-left of every shot. No type.

One car. Porsche 911 Carrera T Sonderwunsch "Formosa", Paint to Sample Ipanema Blue Metallic. The body is that blue. Suzuka Grey is trim, not a second body colour. Official newsroom film, 3840x2160 25 fps, downscaled to 1920x1080. No crop, no upscale.

https://newsroom.porsche.com/en/2025/products/porsche-sonderwunsch-911-carrera-t-formosa-41254.html
Film: https://newstv.porsche.com/porschevideos/newstv.porsche.com_328485_en.mp4

The film is a drive through Taiwan, not a studio walkaround, and a different red car turns up later. That car is not in this cut. Neither is the line "THERE IS NO SUBSTITUTE", which fades on at 116.9 s. The clean takes of this blue car are short, so the edit is 6.44 s and it stops before the type.

- 52.08 side, parked, the shop
- 55.28 the mirror
- 57.62 the light
- 58.96 the rear
- 115.12 the ridge, held to 116.40

Dark, cool grade so the blue reads. No text.

Sound #104 is not in the library. Song **#73** `73_gt3_rs_gulf_blue_showroom_porschebakersf` is the Paint-to-Sample showroom sound. Used 0.00–6.44 s, inside the 10.90 s line. The words in that window are "Take me to the room where we both fell in love." Nothing after 10.90 is in the file.

Script: `engine/grok_one_colour.py`

Cuts measured on the 25 fps master against the original mp3. One frame at 25 fps is 40 ms. None are late.

| edit | hit | offset | what |
|---|---|---|---|
| 0.600 | 0.607 | -7 ms | the mirror |
| 2.080 | 2.106 | -26 ms | the light |
| 2.760 | 2.795 | -35 ms | the rear |
| 5.160 | 5.187 | -27 ms | the ridge, held to 6.44 |

Opens at 0.00 on the side (52.08).

Caption: Ipanema Blue. One of one. Would you order it?
#carsoftiktok #caredit #fyp #porsche #911

# Oct 26 v2 — 18 Oct 2026

The three Oct 26 edits, cut again. v1 is still on disk. Nothing scheduled. Not pushed to scamdecoded-media.

## FOOTBALL — Salah v2

`grok/2026-10-26-salah-v2.mp4` — 1080x1920, 30 fps, 11.30 s, 28.8 MB.
No YouTube file. Both sources are ~30 fps, not 50 or 60.
`grok/2026-10-26-salah-v2-corners.jpg` — top-left and bottom-left 260x130 after the bug crop. Crowd, grass, a stadium board. No score bug, no name tag.

Egypt, the go-ahead against New Zealand, BC Place, 21 June 2026. Number 10.

- https://www.tiktok.com/@fifaworldcup/video/7654129160910097686 — the pitchside angle, native 1080x1920, no bug. The run (source 0.35) and the strike through the net (source 4.18, ends 5.21, before the replay at 5.48). He is not a close-up in this clip. The replay after 5.48 is players as dots, so it is not used.
- https://www.tiktok.com/@fifaworldcup/video/7654126408284851478 — the match highlight. A score bug sits at the top of every frame. Shots are cropped from y=300 (1080x1620) and scaled back, 1.19x, which puts the bug above the frame. The other angle of the move (38.25), the keeper and the ball (40.10), then him, close, 42.60–45.87. That close take ends at 45.91. The next shot is wide, so the edit stops.

He is big for the last 3.3 s, which is the whole clean close-up. There is no second close of him that is actually him: the celebration at 52 s is a different player. Club goals were not used. 11.30 s is the length of the clean pictures. Stretching it would be the wide replay or the bug.

Sound: library **#5** `05_montagem_kali_slowed`, instrumental phonk. TikTok sound: https://www.tiktok.com/music/MONTAGEM-KALI-Slowed-7677012374906259457
The lights-out edit uses 0.00–15.03 s of this file. This cut starts at 15.05 s, so it does not reuse that range. The strike is the cut at 7.00, on the hit. SALAH. from the first frame. THE GO-AHEAD. from 7.00.

Script: `engine/grok_salah_v2.py`

Cuts measured on the 30 fps master against a wav of the same 15.05–26.35 s. One frame at 30 fps is 33 ms. All four are early.

| edit | hit | offset | what |
|---|---|---|---|
| 1.400 | 1.420 | -20 ms | the run, number 10 |
| 4.967 | 4.974 | -7 ms | the keeper, the ball |
| 7.000 | 7.027 | -27 ms | the strike and the net |
| 8.033 | 8.058 | -25 ms | him, held to 11.30 |

No source twice in a row. The highlight is used three times, from three different takes.

Caption: Salah. The go-ahead. Watch the one-two, then him.
#football #footballedit #fyp #worldcup #salah

## F1 — I get it v2

`grok/2026-10-26-i-get-it-v2.mp4` — 1280x720, 30 fps, 10.90 s, 27.0 MB.
`grok/2026-10-26-i-get-it-v2-yt.mp4` — 1080x1920 Short, 50 fps, 10.90 s, 27.3 MB. Title I GET IT / MAX VERSTAPPEN.
`grok/2026-10-26-i-get-it-v2-corners.jpg` — top-left and bottom-left of every shot. The small F1 logo, or bodywork. No name tag, no lap, no replay word.

v1's wide finish lines (Bahrain, the Singapore hold) are gone. The donut opener stays. After that, his car fills the frame, and the last shot is him.

Sound **#105**. https://www.tiktok.com/@v33stappen/video/7697654217405779214
Clean. Stamps stay at 0.48 / 2.80 / 5.34 / 7.36. White, white, gold, white. The third is the gold one. No blur, no streak.

- 2023 Abu Dhabi #1 donuts, formula1.com. Smoke from 2.20 (the hook, 3.34 s — this is the wide one, on purpose). Arms up in the car from 12.60. Him, arms up, from 18.30, the last 1.00 s. These are the season-finale donuts, not the race the title was decided in.
- Singapore onboard, formula1.com, Brightcove 1878860497628040753. Source 9.55–10.95, still his car (the cut to the next driver is at 11.34). The "MAX VERSTAPPEN" lower-third is cropped off the bottom 110 px and scaled back, about 1.18x. A track gantry reads SINGAPORE for a moment as he drives under it. That is the circuit, not a bug.
- 2022 Abu Dhabi cockpit, formula1.com. Source 10.10–12.52, before the aerial at 12.62. The car fills it. "MAX VERSTAPPEN" on the nose is the livery.

All kept 1280x720, 1:1 apart from that one crop. No source twice in a row. The 2023 film is used three times, three different takes.

Script: `engine/grok_i_get_it_v2.py`

Cuts measured on the 50 fps master against the wav. One frame is 20 ms. The detector sees three of the four cuts. The two cockpits are close enough that the fourth (7.48) stays under the bar. It is a hard concat on the hit. The three it sees are early.

| edit | what |
|---|---|
| 3.340 | his onboard, name tag cropped |
| 4.740 | arms up in the #1 |
| 7.480 | 2022 cockpit |
| 9.900 | him, 1.00 s, held to 10.90 |

Opens at 0.00 on the smoke.

Caption: I get it. The smoke, then the car, then him.
#f1 #formula1 #f1edit #fyp #verstappen

## CAR — one colour v2

`grok/2026-10-26-one-colour-v2.mp4` — 1920x1080, 30 fps, 10.88 s, 26.2 MB.
`grok/2026-10-26-one-colour-v2-yt.mp4` — 1080x1920 Short, 25 fps, 10.88 s, 23.3 MB. No title.
`grok/2026-10-26-one-colour-v2-corners.jpg` — top-left and bottom-left of every shot, 100% of the 4K. Paint, sky, tarmac. No type.

One car, one red. It is a Guards Red 911 GT3 S/C, the April 2026 newsroom walkaround, not a Paint-to-Sample one-off. Said plainly. The brief asked for a special colour. The films that are actually a rare colour (Formosa, the jade, the gold) do not have fifteen clean detail takes. Formosa (328485) is the one already posted, and it is a drive, so it is not used. This film is the one that has the N17 grammar: the side, then the parts, then the side again.

https://newstv.porsche.com/porschevideos/newstv.porsche.com_332698_en.mp4
3840x2160, 25 fps, downscaled to 1920x1080. No crop, no upscale.

22 cuts. The side profile is the anchor, three times, from the same tracking take (44.30, 45.15, 45.80). The rest are different details: rear, wheel, lamp, mirror, the blade, the paint, the wheel again with a hand, the scoop, the exhaust, the tail lamp, the light bar, the diffuser, the mirror, the wheel from inside, the door card, the gear lever, the column, hands on the wheel, a hand on the deck. Walter Röhrl is in this film. He is not the shot. A hand on the paint is in a few of them, because that is the walkaround. No title card.

Dark, cool grade. No text.

Sound **#104**, 0.00–10.88 only. The explicit line ("fuck your man") is at 11.00 and is not in this cut.
https://www.tiktok.com/@igvfte/video/7679940726808907040
https://vm.tiktok.com/ZN8Swd3bT/

Script: `engine/grok_one_colour_v2.py`

Cuts measured on the 25 fps master against the wav. One frame is 40 ms. 19 of 21 cuts clear the detector (two details are too similar for it). All 19 are inside one frame. Three sit a few milliseconds after the hit the detector chose, still inside that frame, and early of the hit they were snapped to.

Caption: Guards Red. One car. Count the cuts.
#carsoftiktok #caredit #fyp #porsche #911

## MOVIE — Hard times

`grok/2026-10-27-hard-times.mp4` — 1920x1080, 30 fps, 21.60 s, 25.6 MB. TikTok.
`grok/2026-10-27-hard-times-yt.mp4` — 1080x1920 Short, 30 fps, 21.60 s, 25.4 MB. Title: HARD TIMES / GAS IN THE TANK.

Direction: hard times hit. He still has gas in the tank.

Not a copy of @kam_cuts. His clips, his sound, his watermark and his blur are not in this. Same shape only: a person talks, then the punches, then a person talks. Three films for the punches, a fourth for the answer. Length is the chorus, not his 50 s.

Sound **#139** Hard Times, Paramore. Chorus only, 22 s file, this cut uses 0–20.5 of it. Clean. "Hard" starts at 1.11 s, after "tank". The song ducks under both spoken lines. No 60 fps file: the trailers are 23.976 and 24. YouTube is the Short of this 30 fps master.

Script: `engine/grok_hard_times.py`

Sources, official trailers, 1920x1080, letterbox kept, no crop, no upscale:
- Creed III — Damien, "I still got gas in the tank." Then the ring, the beach, the counter, the tree.
- The Equalizer 3 — the punches and the knee.
- John Wick: Chapter 4 — one fight, one take.
- The Batman — Catwoman, "If we don't stand up, no one will."

Shot list (edit time → source time): 0.00→51.80 GAS IN THE TANK, 1.43→35.48, 3.67→113.30, 4.43→46.53, 5.67→109.40, 7.93→62.16, 8.90→119.70, 10.93→139.41, 11.93→86.16, 13.43→114.28, 14.93→105.86, 16.93→49.48 ROCK BOTTOM, 19.43→62.15 IF WE DON'T / STAND UP / NO ONE WILL.

12 cuts. One frame is 33 ms. Worst early is 23 ms (the tree). Two cuts sit 5 ms after the hit. Nothing is a frame late. Each punch is a different take. The first frame of each punch is the contact.

Caption: Hard times. He still has gas in the tank.
#movie #movieedit #fyp #creed #johnwick

Not scheduled.

## MOVIE — I'm feeling tremendous

`grok/2026-10-27-tremendous.mp4` — 1920x1080, 30 fps, 17.50 s, 26.8 MB. TikTok.
`grok/2026-10-27-tremendous-yt.mp4` — 1080x1920 Short, 30 fps, 17.50 s, 26.5 MB. Title: FEELING / TREMENDOUS.

Direction: he's that guy. The hits say it.

The last cut put the words in the middle of the punch, in pieces, on a song that wasn't the one moving. This one uses the sound that is moving (sound **#155**, "I'm feeling tremendous", from Verified by Your Favorite Martian). The line sits top-left, small, white, like a watermark. It is the whole sentence being sung. It is not a stamp over the fist.

No movie voice. The song is the voice. Punches on the drum, plus a walk, a room, and a stare so it isn't only fists. It ends on the stare while the last line finishes ("a crowd carries me on their shoulders"), then it stops. The file does not include the bar before this clip.

Script: `engine/grok_tremendous.py`

Sources, official trailers, 1920x1080, letterbox kept:
- Creed III — the face, the stare, the ring, the beach, the tree, the room.
- The Equalizer 3 — the punches.
- John Wick: Chapter 4 — the walk.

14 cuts. One frame is 33 ms. Worst early is 25 ms. One cut sits 2 ms after the hit. Nothing is a frame late.

Caption: I'm feeling tremendous.
#movie #movieedit #fyp #animeedit #foryou

Not scheduled.

## MOVIE — Not a hero anymore (#157)

`grok/2026-10-27-not-a-hero.mp4` — 1920x1080, 30 fps, 24.40 s, 27.8 MB. TikTok.
`grok/2026-10-27-not-a-hero-yt.mp4` — 1080x1920 Short, 30 fps, 24.40 s, 26.7 MB. Title: NOT A HERO / ANYMORE.

Direction: he says he is not a hero anymore. Then the hits. Then Ken says he is going to win it all.

Sound **#157** `157_original_sound_official_quality` — the keny4580 dance, 112 BPM, 25.3 s. Clean. Whisper with VAD found no speech. Without VAD it hallucinated "Thank you" across the whole file. Spectrogram is kick, snare and bass, no voice. The T2/T3/T4 reference audios were not used.

Script: `engine/grok_157_not_a_hero.py`

Official IMDb 1080p trailers, letterbox kept, pixels 1:1 (no upscale):
- VisionQuest — the open line, Ultron's beam, Vision's beam, the explosion.
- Street Fighter — Ken's punch, the glove, the flame kick, Chun-Li, the canvas, the flying kick, the green kick, the ground punch, and "I'm going to win it all."
- Spider-Man: Brand New Day — the fist, the blast, the fall, the collision, the web, the stare.
- Avengers: Doomsday — Doom's punch, Doom's face, the group punch.

Spoken lines only, see-through, centre 40% up, in the speaker's colour (Vision gold, Ken red). Song dipped ~10 dB under the lines and ~5 dB for 0.25 s under each hit, with ~0.5 s of that shot's own audio. One frame is 33 ms. Every contact is on the snapped drum, and every snap is inside one frame of the transient.

Not scheduled.


