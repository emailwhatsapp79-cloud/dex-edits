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

## 8. Where the original clips come from
- Movies: official trailers in 1080p from IMDb (GraphQL `video.playbackURLs`), studio press sites.
- F1: formula1.com videos (Brightcove player, account 6057949432001) - race highlights and "crosses the line".
- Cars: brand newsrooms (Porsche newstv, Bugatti newsroom) - press films, often 4K.
- Football: official club / league TikTok accounts (single videos download fine).
- Skip any moment with burned-in subtitles or a channel's big caption; check every chosen span.
