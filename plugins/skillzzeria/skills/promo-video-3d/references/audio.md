# Audio

You can't listen. Everything here is designed to be **measured** instead: the grid guarantees sync, the scripts report loudness and voice-to-music ratio, and you tell the user what to judge by ear.

## Music synthesized on the grid (free, no licenses)
`scripts/synth.py` has the instruments (kick, clap, hats, saw bass, supersaw pads, plucks, risers, whooshes, impacts, crash, sub boom) as numpy functions; `t(beat)` converts beats to samples at 120 BPM. An arrangement file (see `scripts/music_example.py`) places them by **scene**, using the same beat numbers as `src/timing.ts`.

Patterns that worked:
- **Tension intro**: ticking hats (waiting), soft sub pulse, impacts on each slam, riser into a **hard silence** (gate to 0 for ~¼ beat) before the reveal.
- **Drop** when the product appears: impact + crash, 4-on-the-floor, clap on 2 & 4, offbeat open hats, bass on the off-8ths, sidechain pump on the music bus (`1 - 0.6·exp(-t/0.09)` after each kick).
- **A melodic hook** (2-bar motif, supersaw lead + dotted-8th echo) on the drops: it's what makes it "catchy".
- **Event → sound map**: landing → kick + boom; spin → 0.6-beat whoosh ending on the beat + small crash; pop-out → two high plucks; collision → impact + sub boom + long crash + the product's own UI sound placed so its peak lands on the hit; rain of objects → one soft kick + pluck per landing, read from the **same JSON** the scene uses.
- **Breakdown** (pad only) one bar before a climax, then riser.

Mastering: `tanh` soft clip → normalize → ffmpeg `volume`, `alimiter=limit=0.8`. Target **−14 to −12 LUFS integrated, true peak ≤ −1 dBFS** (`scripts/check_render.py` measures it). The first attempt landed at −7 LUFS / +1.8 dBTP — always measure.

A real track (Pixabay, no-attribution licence) at ~120 BPM usually sounds better than synthesis; the grid makes swapping it trivial. Offer it; the user chooses.

## Voice-over findings
- Local TTS (Piper, `es_AR-daniela-high`, length_scale 0.88) generated in seconds and timed well, but was judged unclear and cheap. Use only as a timing guide track.
- If keeping a voice: per-line RMS normalization, high-pass 110 Hz, +presence (bandpass 2.2–5.5 kHz added at 0.6), compressor (−20 dB, 3:1), music ducked ~16 dB with 100 ms look-ahead plus a 1–4 kHz carve. Measure voice-over-music per line; **≥ 12 dB** is the floor for a room. Before that fix the ratio was 3–11 dB and the voice was buried.
- Best voice: a human on the team recording 3–4 lines on a phone.

## Audio in Remotion
Mix to one WAV and play it with `<Audio src={staticFile('audio/mix.wav')} />` at the composition root. Mixing outside Remotion keeps the timeline simple and lets you measure the final file.
