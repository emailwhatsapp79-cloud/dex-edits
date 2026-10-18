# Church edit

A vertical worship cut from a memorial / church gathering. Separate from DEX EDITS: no watermark, no car / F1 / football rules. Branch `church-edit` only (not `main`).

## Files

- `church/church-edit.mp4` — 53.5 s, 1080×1920, 30 fps, H.264, AAC 192 kbps stereo, about −13.5 LUFS
- `church/church-teaser.mp4` — 12.3 s, hook + “There is nothing You cannot do” + the scripture card

## Transcript (what is in the edit)

Times are the edit timeline, not the raw phones. Wording was checked against a second Whisper pass (`small.en`, prompted, word timestamps on the exact cuts) and against the line he is quoting. Where the two hearings disagreed, the note is below.

| Edit | Source | Line |
|---|---|---|
| 0:00–0:04 | altar call `1000229777.mp4` 13.90–17.50 | Be ye transformed by the renewing of your mind. |
| 0:04–0:12 | sermon `1000229776.mp4` 215.00–223.80 | The Bible says the natural man cannot receive the things of God, because they are foolishness unto him. They cannot access it. |
| 0:12–0:23 | sermon 238.15–249.10 | The carnal are those who are saved, but not transformed. You can write that. The carnal are those who are saved, not submitted to the Holy Spirit. |
| 0:23–0:35 | worship `1000229774.mp4` 4.05–15.85 | I sing about Your mercy. You were close by, every night and day. |
| 0:35–0:44 | worship 86.70–95.20 | Higher places of Your love. I've seen Your mighty love. Nothing but my love for You. |
| 0:44–0:49 | worship 98.80–104.30 | There is nothing, there is nothing You cannot do. |
| 0:49–0:54 | end card | Romans 12:2 — Be transformed by the renewing of your mind. |

He says “Romans 12, verse 1” on the mic a moment after the hook. That repeat was cut. The line he actually quotes is Romans 12:2, so the card cites 12:2 and does not burn “verse 1”.

On the second carnal sentence he moves from “saved but not transformed” into “we get to the leadership of the Holy Spirit.” The earlier hearing, and the sense of the sermon, is “saved, but not submitted to the leadership of the Holy Spirit.” Captions say submitted. “You can write that” is real and is captioned.

“I've seen Your mighty love” is the hearing of a phrase the first pass rendered as “higher sea of mighty love” / “mind too long”. “Mighty love” is the clear part. “Nothing but my love for You” is the next phrase; the last syllable sits on the cut.

## What was cut

- Almost all of the 5 min 41 s sermon: definitions repeated, the 1 Corinthians 2:14 page-turn, the Jesus-is-God argument, “dangers of walking in carnality,” and the line “your life becomes a consistent misrepresentation of the image of God.” Strong, but it turned the minute into a lecture. The edit keeps three sentences: be transformed, the natural man cannot receive it, the carnal are saved but not submitted.
- The second identical “be ye transformed” and “bow your heads.”
- Opening worship syllables before “I sing about Your mercy,” the “Daddy we thank You” refrain, “when I look around I see Your face,” “I call on You on my knees,” and “one more time.”
- He walks off at the end of the phone clip. That is not in the edit.

## Enhancement

Source is WhatsApp 360×640, ~26 fps, heavy compression.

- Stabilise: `vidstab` (shakiness 5, smoothing 12, max shift 16), borders kept so there are no black edges.
- Light denoise before the upscaler: `hqdn3d=1.4:1.1:2.5:2`. Heavy denoise was avoided so faces would not go plastic.
- AI upscale: **realesr-general-x4v3** (Real-ESRGAN real-footage SRVGG, not `realesr-animevideov3`). 360×640 → 1440×2560, then a slow punch-in (about 1.12–1.36×) and Lanczos down to 1080×1920.
- `RealESRGAN_x4plus` was loaded and checked on a still (weights matched, face looked clean) but it took **~63 s per frame** on this 2-core CPU, which is most of a day for the cut. The general real-footage model was ~3.2 s/frame and did not wax the skin. Frames were checked at 100% on the face before and after the grade. Skin stays soft, not plastic.
- Upscale sample rate 14 fps from the 26 fps source (CPU), then conformed to 30 fps. Motion is a standing preacher and a standing singer, so the dropped frames read as a slight hold, not a stutter montage.
- After the punch-in: light `deband`, gentle `unsharp` 5×5 amount 0.20 (no face-crisp plastic look), gamma 1.055, contrast 1.04, saturation 1.07, warm `colorbalance` (lifted shadows, gold highlights, skin left alone).

## Audio

- Voice: high-pass 85 Hz, `afftdn` (nr 9), light compression 2.3:1, limiter. No heavy de-reverb — the room is part of a live church and stripping it made the voice hollow.
- Under the preaching only: his own guitar from the worship take, low-passed around 620 Hz, quiet, sidechain-ducked by the voice, faded as the song enters. No commercial track.
- The sung section is his live vocal and guitar, same cleanup, no added pad.
- Loudness about −14 LUFS (measured −13.5 integrated, true peak −4.3 dBTP), AAC 192 kbps stereo.

## Suggested caption

Be transformed by the renewing of your mind.
The natural man cannot receive it. Grace can.
There is nothing You cannot do.

#jesus #worship #christiantiktok #fyp #gospel
