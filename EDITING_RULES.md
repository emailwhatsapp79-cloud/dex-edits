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
