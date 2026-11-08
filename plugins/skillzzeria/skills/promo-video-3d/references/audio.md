# Audio

You can't listen. Everything here is designed to be **measured** instead: the timeline guarantees sync, the scripts report loudness and voice-to-music ratio, and you tell the user what to judge by ear.

## Voice-over with ElevenLabs (what shipped)
1. **Script first, exact text.** Short phrases, one idea each, written to be said, not read (e.g. "Sábado, 19 h. Faltan dos. ¿Cómo se encuentran? … Dejá de buscar jugadores. Empezá a jugar."). 14 phrases filled 40 s.
2. **Voice**: a native speaker of the audience's accent from the voice library. For rioplatense, "Chelo – Young, Publicity and Characters" (`SxiIZdPt3fsiAenlubTX`) worked. Use the newest model (`eleven_v4` at the time) and **direction tags** per section: `[calm, confident, intimate]` for the hook, `[energetic, punchy]` for the action words. Generate the whole script as **one take** so the delivery has continuity, then cut it.
3. **Getting the file**: the ElevenLabs MCP/API can generate it, but its download domain (`elevenlabsusercontent.com`) may be blocked from a sandbox. Then ask the user to download the MP3 and attach it. The MCP transcription with timestamps is a useful reference for where each phrase falls.
4. **Cut per phrase**: `scripts/split_vo.py vo_raw.mp3 public/vo --phrases 14 --tempo 1.07`. It uses `silencedetect` (−40 dB, 60 ms), keeps the N−1 longest pauses as boundaries, adds 35 ms pre-roll / 70 ms post-roll, speeds up 7% with `atempo` (pitch kept: "sped up a little" sounds more like an ad), fades 8 ms in / 30 ms out, and writes 48 kHz mono `pNN.wav` + `durations.json`.
5. **Place each phrase** in `timeline.ts` as a start time (`VO = [{id:'p01', s:0.70}, …]`), and play them as separate `<Sequence from={…}><Audio src={staticFile('vo/p01.wav')} /></Sequence>`. Separate files let you nudge one phrase onto a beat without re-cutting the take. Check that `start + duration` never runs into the next phrase.
6. Treat the voice like the lead: the music leaves room (pad and kick under it, nothing melodic in the voice's range while it speaks), and the big hit comes **between** phrases, never under one.

Earlier finding, still true: local TTS (Piper `es_AR-daniela-high`) generated in seconds and timed well, but was judged unclear and cheap. Use it only as a timing guide track before the real voice exists. If you ever must keep a weak voice: per-line RMS normalization, high-pass 110 Hz, presence boost 2.2–5.5 kHz, compressor (−20 dB, 3:1), music ducked ~16 dB with look-ahead. Measure voice-over-music per line: **≥ 12 dB** is the floor for a room.

## SFX
Short and dry, nothing long or soft (the user's explicit ask, and it matches the "Apple-style" brief). Synthesized in numpy:
- `click()`: band-passed noise + high ping + small thump. The hero click.
- `tap()`, `tick()` for every finger tap on the phone UI.
- `tok()`: a bounce with a falling pitch, tuned per object type. Export the simulation's real contacts (frame, ball type, impact speed) to `bounces.json` and place one `tok` per contact, scaled by speed: 143 bounces, all in sync for free.
- `impact()`: the main click + a short sub on the hero hit.
Every SFX sits on the exact frame of its event, read from `timeline.ts` or the exported JSON, never typed by hand.

## Music synthesized on the grid (free, no licences)
`scripts/synth.py` has the instruments (kick, clap, hats, saw bass, supersaw pads, plucks, risers, whooshes, impacts, crash, sub boom) as numpy functions; `t(beat)` converts beats to samples at 120 BPM. An arrangement file (see `scripts/music_example.py`) places them by **scene**, using the same beat numbers as the timeline.

Patterns that worked:
- **Tension intro**: ticking hats (waiting), soft sub pulse, impacts on each slam, riser into a **hard silence** before the reveal.
- **The click**: half a second of total silence (28.0–28.5 s in the ad), then the hit exactly on the click frame. The most effective moment in the narrated spot.
- **Drop** when the product appears: impact + crash, 4-on-the-floor, clap on 2 & 4, offbeat open hats, bass on the off-8ths, sidechain pump (`1 - 0.6·exp(-t/0.09)` after each kick).
- **A melodic hook** (2-bar motif, supersaw lead + dotted-8th echo) on the drops, only where there's no voice.
- **Event → sound map**: landing → kick + boom; spin → 0.6-beat whoosh ending on the beat; pop-out → two high plucks; collision → impact + sub boom + long crash + the product's own UI sound placed so its peak lands on the hit.

## Swapping in a licensed track (Artlist, Pixabay…)
The synthesized music is a **temp track** when the user plans to license one. When the track arrives:
1. Find its downbeat/hit and align it so the "square hit" lands on the click frame (`CLICK / fps` seconds). Trim or loop at bar boundaries of the track's own BPM, not the temp grid's.
2. Mix with the existing VO and SFX stems, then normalize.
3. **Re-mux, don't re-render**: `ffmpeg -i master.mp4 -i mix.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 320k master-v2.mp4`.

## Stems and mastering
- Keep stems: `stem_VO.wav`, `stem_SFX.wav`, `stem_MUSIC.wav` (48 kHz stereo, full length, starting at 0). Any later change re-mixes in seconds.
- Master: sum → `loudnorm=I=-14:TP=-1:LRA=11` (two-pass if you have time). Target **−14 LUFS integrated, true peak ≤ −1 dBFS**; `scripts/check_render.py` measures it. An early music-only attempt landed at −7 LUFS / +1.8 dBTP, so always measure.
- With synthesized music only: `tanh` soft clip → normalize → `alimiter=limit=0.8` also works.

## Audio in Remotion
Two valid setups:
- **Mixed outside** (music-only intro): one `mix.wav` at the composition root. Simplest timeline, and you measure the final file.
- **VO inside, rest outside** (narrated ad): VO phrases as `<Audio>` sequences for timing work in the studio; render the video `--muted` and mux the final stem mix with ffmpeg. Pass `audio` as a composition prop so stills and layer renders skip it.
