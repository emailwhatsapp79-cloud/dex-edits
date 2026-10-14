# Editing rules (TikTok edits)

Rules from Desmond's feedback. Follow every one of them on every edit.

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

## 8. Where the original clips come from
- Movies: official trailers in 1080p from IMDb (GraphQL `video.playbackURLs`), studio press sites.
- F1: formula1.com videos (Brightcove player, account 6057949432001) - race highlights and "crosses the line".
- Cars: brand newsrooms (Porsche newstv, Bugatti newsroom) - press films, often 4K.
- Football: official club / league TikTok accounts (single videos download fine).
- Skip any moment with burned-in subtitles or a channel's big caption; check every chosen span.
