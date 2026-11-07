#!/usr/bin/env python3
"""Example arrangement for a ~40 s promo: tension intro → reveal → drop with hook → breakdown → climax → CTA drop.

Copy this next to your project (e.g. audio/music.py), edit the beat numbers to match src/timing.ts, run:
    python3 -I audio/music.py out.wav
Needs numpy + scipy (a uv/venv is fine). Every line below places one sound on one beat.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))  # or the skill's scripts/ dir
from synth import *  # noqa: F401,F403

OUT = sys.argv[1] if len(sys.argv) > 1 else 'music.wav'
TOTAL = 80
N = int(TOTAL * BEAT_S * SR) + SR
D, M, FX = np.zeros(N), np.zeros(N), np.zeros(N)  # drums, music (pumped), effects
kicks = []

# 0–12 · pain: ticking hats, soft pulse, an impact on every text slam, riser into a hard silence
for bt in (0, 2, 4, 6):
    add(FX, t(bt), impact(0.55))
for bt in np.arange(0, 8, 0.5):
    add(D, t(bt), hat(False, 0.09))
for bt in np.arange(0, 8, 1.0):
    add(M, t(bt), bass_note(33, 0.35, 0.35))
add(M, t(0), pad([45, 57, 60, 64], 8, 0.14, attack=2.0, cutoff=900))
add(FX, t(8), riser(3.7, 0.5))

# 12–24 · reveal / world: beat comes in, one pluck per thing that lights up
add(FX, t(12), impact(0.5))
groove(D, M, 12, 22, kicks, claps=False)
for bt, note in zip([12.5, 13.5, 14.5, 15.5, 16, 17, 18], [69, 72, 76, 81, 79, 84, 88]):
    add(M, t(bt), pluck(note, 0.3, dur=0.4))
add(FX, t(21), riser(1, 0.5))

# 22–40 · product: the drop + hook; whoosh into every screen change, blips on pop-outs
add(FX, t(22), impact(0.95)); add(FX, t(22), crash(0.5))
groove(D, M, 22, 38, kicks)
lead(M, 22, 38)
for bt in (26, 30, 34):
    add(FX, t(bt - 0.6), whoosh(0.6, 0.35)); add(FX, t(bt), crash(0.22))
for bt in (23, 27, 31, 35):
    add(M, t(bt), pluck(93, 0.22, dur=0.15))

# 38–42 · breakdown, 42–44 · riser, 44 · climax impact (+ the product's own sound if it has one)
add(M, t(38), pad([57, 60, 64, 71], 4, 0.25, attack=0.4, cutoff=1800))
add(FX, t(42), riser(2, 0.6))
add(FX, t(44), impact(1.0)); add(FX, t(44), boom(1.0, 3)); add(FX, t(44), crash(0.6, 3))
# add(FX, t(44) - int(0.6 * SR), load_sound('public/sfx/splash.mp3'), 0.9)  # align the sound's peak to the hit

# 50–53 · near-silent punchline, 53 · CTA drop, 66 · final hit
add(FX, t(50), boom(0.8, 2.5)); add(FX, t(51.5), riser(1.5, 0.6))
add(FX, t(53), impact(1.0)); add(FX, t(53), crash(0.5))
groove(D, M, 53, 66, kicks); lead(M, 53, 66)
add(FX, t(66), impact(1.0)); add(FX, t(66), crash(0.55, 3))

mix = D * 0.8 + M * sidechain(N, kicks) * 0.85 + FX * 0.8
silence(mix, 11.75, 12)  # lights out before the reveal
write_wav(OUT, master(mix, TOTAL))
print('ok →', OUT)
