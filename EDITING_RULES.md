# Editing rules (TikTok edits)

Rules from Desmond's feedback. Follow every one of them on every edit.

## 0. HARD RULE - CLEAR AND SHARP, NO SIGN OF BLUR (Desmond, Oct 15: "every new edit must be clear and sharp")
Nothing is scheduled until it passes ALL of these. A soft edit is not posted - it is rebuilt or replaced.
1. **Sources:** only sharp, recent, official footage (4K press films, official 1080p clips of recent matches/races).
   Measure every source; never re-uploaded compilations of old SD/720p broadcasts. 720p F1 footage is not used full
   screen.
2. **No upscaling over ~1.4x.** Vertical 1080p -> layout `full` at native size; 4K landscape -> `tall`; letterboxed
   1080p film -> `tall` with `pic_h=810` (4:3, a downscale). Never a 9:16 crop of 1080p landscape.
3. **No motion interpolation, no fake slow-mo, no grain, no blur transitions** (zoom/whip/spin), no glitch effects.
   Slow motion only when the source itself is slow-mo (e.g. FIFA super-slow-mo replays).
4. **Check every shot before the full render** (stills at each cut and each key action) and replace any frame that is
   motion smear, crowd smear, out of focus or not the subject.
5. **After the render:** 100% crops of the finished file next to the source - the output must be as sharp as the
   source (the render adds a light sharpen; it must never be softer). Final encode crf 12, watermark pass >= 8 Mbps.
6. **Same check for edits already scheduled** before they go out; below standard -> replace with a new edit.

### TikTok delivery audit (Oct 16) - what viewers actually see
- TikTok re-encodes every upload: 1080p at only ~1.1-2.4 Mbps (H.265) and **540p at ~0.4-1 Mbps**, which phones on mobile
  data play by default. Anything soft in our master becomes "350p-looking" after that.
- Posted edits with genuinely soft shots: Mbappe (the opening close-ups are upscaled crops - the softest shot was the
  HOOK), Yamal #10 (RGB-split glitch effect = smear), Antonelli history (upscaled broadcast pack shot). Never again:
  **the first 2 s must be the sharpest shot in the edit**, and no glitch/RGB-split effects.
- Upload **30 fps**, not 60: TikTok gives each video roughly the same bitrate, so 60 fps halves the bits per frame.
- QC before scheduling: `python3 engine/effres.py videos/<file>.mp4` (effective resolution every 0.5 s) + eyeball every
  flagged frame at 100%. Smooth skin, bokeh and dark frames can read low - the 100% crop decides.

### Captions and hashtags (Desmond, Oct 16)
Every post: short line + **4-5 hashtags**: F1 `#f1 #formula1 #f1edit #fyp #<driver>`, football `#football #footballedit
#fyp #worldcup #<player>`, cars `#carsoftiktok #caredit #fyp #<brand> #<model>`. Give each edit a concept/title worth
sharing (M1 "race week", M2 "the art of camera angles"), not just a statement.

### What works vs what doesn't (Desmond, Oct 17)
- WORKS: Antonelli "20 years old. One race from history." - YouTube 7,004 views / 424 likes / 9 shares / +4 subs in 2 days,
  the channel's best. One driver, one story with stakes in the title, trailer format, real voices.
- NEVER AGAIN: "Top 5" compilations built from mixed broadcast/fan clips (Messi Top 5 = very blurry). A countdown only if
  every clip is official 1080p+ and passes the 100% check - otherwise make a one-story edit instead.

## 1. Every edit needs a direction
An edit is a short story about ONE subject, not random clips put together.
- **Car edit:** one car (or one clear story such as "car A vs car B"). Same car in every shot, same look, same night/day mood. Build it: reveal → details → it moves → payoff.
- **Football edit:** one player and one moment or match. Build-up → the goal or skill → celebration → reaction. Rival shots only as part of that story.
- **Movie edit:** one film or one character arc. The dialogue and the song should say the same thing.
- Before editing, write the direction in one sentence (e.g. "Mbappé's hat-trick night vs City: calm → chaos → king"). If a clip doesn't serve that sentence, cut it.

## 2. The first 3 seconds must hook
- The best shot or strongest line goes in the first frame. Never open on black, slow text, or a weak shot.
- Text or a line people can relate to on screen from frame 0, with motion from frame 1.

## 3. Understand the song before editing
- Find the tempo, the beat grid, the drop and every word with its timing before choosing clips.
- Calm section before the drop = fewer cuts, clean shots. After the drop = cut on beats/words.
- Lyrics should match what is on screen when they make sense ("on the floor" = pedal to the floor).
- If the sound has SPEECH (commentary, dialogue) or clear lyrics, transcribe every word with its timing first.
  The picture must show what is being said at that moment, and no on-screen text may say something different
  while a voice is talking (lesson from the "Formula Max" edit: the commentator says "handshake between the two
  teammates" - so show the handshake, not unrelated text).
- Lyrics on screen are NOT a default – only when Desmond asks for them (first used on the nature edit
  "A piece of heaven"). WHEN an edit shows lyrics, they LEAD the voice: each word starts appearing ~0.35 s early and is fully visible ~0.2 s before it
  is sung (Desmond: "it should show some ms before the music"). Never show a word after it has been sung.

## 3b. Transitions must land exactly on the beat
- Cut on the real drum hits, not on beat-tracker estimates. Detect kick and snare onsets from the
  percussive part of the track (sample-accurate), and use those times for cuts, flashes and zoom punches.
- Render at 60 fps and snap each cut to the frame where the hit lands (never late; one frame early is fine,
  because the eye reads a cut slightly ahead of the ear).
- Flashes and punches peak on the hit frame itself, not after it.
- After rendering, measure every cut against the audio and report the error. Anything off by more than
  one frame (17 ms) gets fixed before sending.

- Every shot must sit inside ONE continuous take of its source. Professional source films have their own
  cuts every 1-3 s; if a shot runs across one, the viewer sees an extra, off-beat cut. Detect the source's
  cuts first and place each shot inside a clean take (split long shots on a beat, or use slow-mo, if a take
  is too short). Never let a tool silently fall back to an unclean span.
- Voice-over lines must never overlap each other; check the voice timeline before rendering.
- No repeated clips: every shot comes from a DIFFERENT take. Two cuts in a row from the same take look
  like a stutter ("instant repetitive clip"). The render script checks this and refuses to run if a take repeats.

## 3c. Branding
- Every finished edit gets a small "DEX EDITS" wordmark: white at 55% opacity, top centre (inside TikTok's
  safe zone, clear of the side buttons and caption). Our own watermark is fine; never upload a video that
  carries another app's logo (e.g. a TikTok download re-posted to YouTube).

## 4. Not every clip needs heavy effects
- Use heavy effects (flash, shake, RGB split, blur) only on the drop and on key words.
- Let the best shots breathe: clean, slower, minimal effects.

## 5. Quality
- Real video clips, not still photos.
- Vertical 1080x1920, a consistent colour grade across all clips.
- Text must stay readable: when text goes behind the subject, only part of it may be covered.
- Check every frame (contact sheet) before delivering. Send files under 30 MB.

## 6. Sounds
- The song library lives with the edit assets (see `songs/LIBRARY.md` in the assets folder). Re-use from it instead of asking for songs again.

**Trending audio (Desmond, Oct 18):** the sound does NOT have to be one already in `songs/LIBRARY.md`. Grok can search TikTok for what is trending right now and take the audio from there - use it. Still: clean lyrics only (no explicit words in the part used), and write the TikTok link of the sound in NOTES so it gets saved with add_sound.

**Length (Oct 18):** length follows the story and the song phrase, not a target number. Reference hits: 7 s (N16, 514k), 12 s (N17, 2.3M; M26, 30% likes), 20-24 s (M24, M25 - stories/series). Guide: one-shot/detail edits 8-12 s (short = rewatches/loops); a goal = 12-15 s (build-up, strike, net, celebration - under ~8 s cannot tell it); story/race-week/lyric edits 15-25 s. The hook in the first 1-2 s matters more than the length. Never pad with holds to reach a number.

## 7. Styles learned from reference edits
- **"Aura" F1 edit (Formula Max sound):** one long, calm slow-motion intro (no cuts) until the drop, then a cut on
  every snare. On the hits: a white flash, 1-3 photocopy (black/white threshold) frames, colour <-> black-and-white
  strobe every 4 frames, radial zoom blur on the big poses. The strongest hit gets the hero moment (celebration).
- **Cinematic lyric edit (Tokyo Drift "We just pray for cars"):** 2.4:1 letterbox look, very few cuts (one every
  ~2 s, on the downbeat), the song's lyrics as small white subtitles word by word, the key words big and red in
  the centre ("DON'T ... LOVE / PRAY ... CARS"). Every shot matches its lyric (NOS bottle on "centerpiece",
  wheel on "skinny pieces", RX-7 on "I take any lane"). The calm pace is the style - the song carries it.
- **DEX template "BROADCAST / RACE CONTROL" (our own, first used on Max, Oct 16):** a sharp 16:9 TV window
  (no upscaling - the 720p F1 footage stays crisp) on a team-colour background. Above it the driver's name types
  itself one letter per beat during the quiet intro; below it an F1-TV RACE CONTROL box types the story on the
  beats (the text IS the story - no voice in the sound, so nothing to contradict), and a stat counter
  (e.g. 2026 WINS 0 -> 1 -> 2) pops on the drops. One big word over the window for the climax (BACK TO BACK.).
  Engine: `cardedit` layout `broadcast` (`bg`, `win_y`), script `engine/edit_q_max_racecontrol.py`.
- **DEX template "TERRAIN SELECTOR" (911 Dakar, Oct 16):** a history hook in the quiet intro (sepia archive + one
  stamped fact per soft hit: 1984. / PORSCHE WINS THE DAKAR. / 38 YEARS LATER...), the drop slams into the new car
  (THEY BUILT IT AGAIN.), then full-bleed footage grouped by terrain: the terrain word stamps in on its first hit
  (SAND. / GRAVEL. / SNOW.) and a 3-step selector at the bottom moves on. Script `engine/edit_r_dakar.py`.
- **Lesson from the first numbers (Oct 14):** story edits beat "nice car" edits (Antonelli 16 % likes/view, Spa 8 %,
  Taycan 3 %) and views stall at ~250 when the hook is slow. Something must happen in the first second - never a
  6 s calm intro on its own (that is why the Race Control Max edit was dropped before posting).
- **Channel focus (Desmond, Oct 14):** Dex Edits = football + F1 (+ cars). No nature on this account (nature lyric
  edits would go to a separate account). Football and F1 rotate the star every day (Messi, then Ronaldo, then the
  next...; Verstappen, then Hamilton, then Leclerc...) - never the same person two days running. Group edits
  (free-kick specialists, the whole grid) are fine in between.
- **Burned-in names/captions in source clips:** blur or avoid them when they name one person in a group edit or
  carry another account's caption (edit S blurs the caption band of shot 0).
- **Types of edits to rotate (Desmond, Oct 14) - not only goals / not only wins:**
  football: goals, tackles & last-ditch blocks, skills & nutmegs, saves, free-kicks, "Top 5" countdowns (face strip
  on top, real commentary, name tag on the player); F1: overtakes, starts, wheel-to-wheel fights, saves & near
  misses, pit stops, rain, onboards, "Top 5" countdowns. One star per day for player edits (rotate).
- **DEX template "COUNTDOWN" (Messi Top 5, Oct 17):** teaser of #1 first (WAIT FOR #1.) as the hook, then #5 -> #1;
  every item keeps its own commentary/crowd audio (loudness-matched), header NAME / TOP 5 with five rank chips, the rank
  pops big, a caption bar names the moment, celebration after each goal. Engine: `engine/countdown.py`.
- **SHARPNESS (found Oct 14 - posts looked blurry):** never motion-interpolate real-speed shots (minterpolate smeared
  every frame: sharpness 875 -> 11 on one F1 shot); only slow-mo shots are interpolated now. Grain is 1/4 of before
  (grain turns to mush in TikTok's ~1.3 Mbps encode). Never upscale 720p more than ~1.2x: for 720p broadcast footage use
  layout `window` (the 16:9 picture at 1080x608 = a downscale, over its own blur or black). Dark cinema grades need a
  shadow lift for phones (edit W: gamma 0.68).

- **SOURCE SHARPNESS GATE (Desmond, Oct 15 - "the edit is blurry", "even the posted ones"):** the blur was mostly the
  SOURCES: re-uploaded TikTok compilations of 2016-18 broadcasts are already upscaled (Laplacian sharpness 10-25), while
  official clips of recent matches (@fifaworldcup pitch-side camera, @foxsports broadcast) score 250-500. Measure every
  source (median Laplacian variance of the grey frame) and never use one under ~100 for a hero shot; a sharp shot next
  to a soft one makes the soft one look worse. Vertical 1080x1920 sources go in layout `full` at native size (no blur
  bands - they read as "blurry" on a phone); crop burned-in captions with `active`, keeping upscale under ~1.4x.
- **ONE STORY, NOT A PILE OF CLIPS (Desmond, Oct 15 - "doesn't make sense"):** AD mixed 9 sources from 4 eras and 3
  clubs, half the shots were wide shots where he is a dot, some did not even show Ronaldo. Pick ONE event or
  tournament, every shot must show the star or the direct reaction to him (net, fans, bench), wide play only when the
  ball is going in. Check the stills of every shot (`edit.py <t> <t> ...`) before the full render: a frame that is
  motion blur, a crowd smear or someone else gets replaced.

- **TRAILER FORMAT (Desmond, Oct 15):** like a movie trailer for a player/driver: their REAL voice (radio, interview,
  commentator) with the picture of what is being said, then a boom into the action with the real sound, music under
  everything and ducked under each voice line, the key word landing ON the drop (edit AJ: "...Grand Prix" = drop).
  Music must be instrumental (check with ASR first - song #23 has a commentator in its intro). Ends on the real crowd/
  celebration audio of the final shot (picture = sound).

- **VOICE / LYRIC HOOKS (Batch I, Oct 15):** open on the strongest voice line - on black with the words appearing as
  they are said (I2), or on the speaker's face (I3) - or start cold on the climax (Verstappen trailer v3). For a sung
  song, stamp each lyric word big on its own cut (I1). Never open on a static, voiceless shot.
- **NOT TOO ZOOMED (Desmond, Oct 14):** a 9:16 crop of a 16:9 film shows only 32 % of the width - cars get cut and it
  looks zoomed. For landscape sources use layout `tall` (3:4 picture, 75 % more width, over its own blur); 9:16 full
  only for vertical sources or close-ups.
- **FULL SCREEN by default (Desmond, Oct 14):** the picture fills the whole 9:16 frame. Window/card/black-frame layouts
  only when the source is too low-res to crop (720p broadcast) - and then prefer finding a better source.

- **LIGHT EDITS (Desmond, Oct 14, batch H):** many of the best edits have NO on-screen text, no effects, 5-20 cuts and
  just beautiful sharp full-screen footage (14M views with 5 cuts). Alternate: story edits (text) and light edits
  (no text). Footage quality decides: 4K sources cropped to 9:16 (a downscale) or native vertical 1080p.
- **CAPTIONS SHORT:** one line, max 2-3 hashtags, sometimes none ("my little baby", "this is peak life").

- **LENGTH + A REAL ENDING (Desmond, Oct 15):** 10-14 s edits "look like the edit is not complete". Aim 20-25 s.
  TikTok sounds are short: play them twice with `engine/songloop.py` (cut out on one strong hit, back in on another,
  so the join is invisible) and END on a phrase with a 1-1.2 s audio fade + a slow last shot + fade to black.
  Never stop the sound mid-word.

- **FULL SONGS, STARTING AT THE GOOD PART (Desmond, Oct 15):** use the full song (`engine/fullsong.py`, songs/FULL.md)
  instead of repeating a short TikTok sound - but never from the song's slow start: begin a few beats before the part
  people wait for (the build right before the drop / where the TikTok clip sits) and end where the song itself
  finishes a section (energy falls away) with a ~1 s fade. Looping (`songloop.py`) only when no full song exists.
- **ACTION ON THE BEAT, not just the cut (Desmond, Oct 15: "nothing matches the beat"):** find the exact source frame
  of each key action (foot on ball, ball in the net, keeper beaten, celebration landing) and set the shot's source
  start so that frame lands ON a hit: src = event_time - (hit - shot_start). Biggest action on the drop, the others on
  the strongest accents; quiet faces during the build. (Ronaldo edit AD: volley on the drop, net on 24.32, keeper
  beaten on 26.82, the SIU on 29.33.)

### SINGLE-CAR SPOTTING (L1 GT2 RS, 23% like rate; H2, H8)
For the CAR slot this is the format that wins on TikTok. One car, one location, nothing else:
1. Open on a sharp macro detail (headlight, wing), NOT a wide shot.
2. Hold a low, ground-level shot of the empty street until the car **drives into the frame** and stops on its hero 3/4.
   That arrival is the payoff, so let it run for 2-4 s.
3. Then one detail per cut, every 2 beats (~1 s): mirror, crest, wing, interior/shifter, badge. Finish on the hero front.
4. No text, no effects, a soft warm grade, and a caption that is just the car's name.
Sources must be sharp single-car footage of ONE car (press films/newsrooms or official clips). Never mix two cars or
two locations into a spotting edit.

## 8. Where the original clips come from
- Movies: official trailers in 1080p from IMDb (GraphQL `video.playbackURLs`), studio press sites.
- F1: formula1.com videos (Brightcove player, account 6057949432001) - race highlights and "crosses the line".
- Cars: brand newsrooms (Porsche newstv, Bugatti newsroom) - press films, often 4K.
- Football: official club / league TikTok accounts (single videos download fine).
- Skip any moment with burned-in subtitles or a channel's big caption; check every chosen span.

## Pixels 1:1 (Desmond, Oct 17 - "why can't you get clean shots like that", ref M6 1.1M views)
- The cleanest viral edits never crop a narrow 9:16 slice out of a 16:9 clip. Either upload HORIZONTAL (16:9, the
  whole frame, at the source's native size) or build vertical edits ONLY from native-vertical sources
  (official @f1 / team / club TikToks at 1080x1920).
- formula1.com (Brightcove) gives 1280x720 max -> use it full-frame horizontal at 1280x720 or as a 'window' band;
  never 'tall'/'full' crops of it.
- Never mix: one edit = one orientation, one source quality.
- **DEFAULT FORMAT FROM OCT 17 (Desmond, after "The greatest show"): "all videos from now on should be like that".**
  Every new edit is HORIZONTAL 16:9 at the source's native size (engine/wideedit.py): 1920x1080 from 1080p/4K
  sources (press films, trailers, Tesla 4K), 1280x720 from formula1.com. No crops, no upscale, words centred,
  light grade, DEX EDITS mark. Already-scheduled vertical posts stay as they are (no re-renders unless asked).
- **Clarity first, orientation second (Desmond, Oct 17, ref N5):** horizontal is not the point - CLEAR is. Use the
  orientation the source was filmed in, at native size, in good light. Vertical native (1080x1920 phone/TikTok) and
  horizontal native (1080p/4K films) are both fine; crops/upscales are not.
- **YouTube is scheduled SEPARATELY from TikTok (Oct 17):** YouTube only makes vertical/square uploads Shorts - a 16:9
  upload becomes a normal video (no Shorts feed, other compression). Horizontal edits: TikTok gets the 16:9 file,
  YouTube gets `engine/ytshort.py` (16:9 band on black 1080x1920 + title, no crop, no blur) as its own post.
- **Frame rate per platform (Desmond, Oct 17: "YouTube looks blurry since 30 fps, views dropped"):** TikTok streams at a
  fixed bitrate, so 30 fps = more detail per frame. YouTube does the opposite - 60 fps uploads get a higher bitrate tier.
  So: TikTok post = 30 fps file, YouTube post = 60 fps file (brand(..., fps=60)) when the edit was made at 60.
  All Oct 17-23 posts with a 60 fps master were split this way (YouTube media = the pre-conversion files at commit 520a9e3).
  formula1.com highlights are 50 fps -> the YouTube master is rendered at 50 (DEX_FPS=50 python3 engine/edit_<x>.py render,
  then engine/ytshort.py <in> <out> '<title>' 50). Any source at 50/60 fps = YouTube gets 50/60.
- **RACE-WEEK FORMULA (refs M6 1.1M, M15 300k):** commentator line "The <X> Grand Prix is underway!" word-by-word over
  the CITY (skyline, aerial, landmarks) -> event title card (track name/logo, city, ROUND n, dates) -> track action on a
  local/trending song -> end on the opening shot (loop). Horizontal native, posted early in race week.
- **SIDEWAYS FORMAT (refs M2, M10, M12, M17 - @f1edits.ae, 131k-1.1M, 24-26% likes every time):** 16:9 footage rotated
  90 degrees inside a 1080x1920 file. The viewer turns the phone and gets the whole picture full-screen at native size;
  the platforms still treat it as vertical (TikTok For You + YouTube Shorts, one file for both). Best for F1 edits from
  horizontal footage. Grade follows the song (summer pop = bright/saturated, moody song = dark).

