"""Synth instruments on a beat grid, in numpy (needs numpy + scipy). Import from your arrangement script.

    import sys; sys.path.insert(0, '<skill-dir>/scripts'); from synth import *
    N = int(TOTAL_BEATS * BEAT_S * SR) + SR
    drums, music, fx = np.zeros(N), np.zeros(N), np.zeros(N)
    add(fx, t(16), impact(0.9))          # an impact exactly on beat 16
    ...
    write_wav('public/audio/music.wav', master(drums * .8 + music * sidechain(N, kicks) + fx * .8))

Everything is placed with t(beat) → sample index, using the same beat numbers as the video's timing.ts.
Change BPM/BEAT_S here if the video uses another tempo.
"""
import subprocess
import wave

import numpy as np
from scipy import signal

SR = 48000
BPM = 120
BEAT_S = 60 / BPM
rng = np.random.default_rng(7)


def t(beat):
    return int(round(beat * BEAT_S * SR))


def hz(note):
    return 440.0 * 2 ** ((note - 69) / 12)


def env_exp(n, tau):
    return np.exp(-np.arange(n) / (tau * SR))


def sos_filter(x, kind, freq, order=2):
    sos = signal.butter(order, freq, btype=kind, fs=SR, output='sos')
    return signal.sosfilt(sos, x)


def add(buf, start, x, gain=1.0):
    if start >= len(buf):
        return
    end = min(len(buf), start + len(x))
    buf[start:end] += x[: end - start] * gain


def saw(freq, n, detune=0.0):
    ph = np.cumsum(np.full(n, freq * (1 + detune) / SR)) + rng.random()
    return 2 * (ph % 1) - 1


# ---------- instrumentos ----------

def kick(level=1.0):
    n = int(0.42 * SR)
    f = 45 + 110 * env_exp(n, 0.035)
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * env_exp(n, 0.16)
    click = sos_filter(rng.standard_normal(n), 'highpass', 2500) * env_exp(n, 0.004) * 0.35
    return np.tanh((body + click) * 1.6) * level


def clap(level=1.0):
    n = int(0.3 * SR)
    noise = sos_filter(rng.standard_normal(n), 'bandpass', [900, 6000])
    e = np.zeros(n)
    for off in (0, 0.011, 0.022):
        s = int(off * SR)
        e[s:] += env_exp(n - s, 0.012 if off < 0.02 else 0.11)
    tone = np.sin(2 * np.pi * 190 * np.arange(n) / SR) * env_exp(n, 0.05) * 0.4
    return (noise * e * 0.6 + tone) * level


def hat(open_=False, level=1.0):
    n = int((0.25 if open_ else 0.05) * SR)
    x = sos_filter(rng.standard_normal(n), 'highpass', 7500)
    return x * env_exp(n, 0.09 if open_ else 0.012) * level


def crash(level=1.0, dur=2.2):
    n = int(dur * SR)
    x = sos_filter(rng.standard_normal(n), 'highpass', 4000)
    return x * env_exp(n, 0.55) * level


def boom(level=1.0, dur=1.8):
    n = int(dur * SR)
    f = 38 + 40 * env_exp(n, 0.12)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * env_exp(n, 0.55) * level


def impact(level=1.0):
    k = kick(1.0)
    b = boom(0.9)
    c = crash(0.35, 1.6)
    n = max(len(k), len(b), len(c))
    out = np.zeros(n)
    out[: len(k)] += k
    out[: len(b)] += b
    out[: len(c)] += c
    return out * level


def riser(beats, level=1.0, f0=300, f1=9000):
    n = t(beats)
    noise = rng.standard_normal(n)
    out = np.zeros(n)
    block = 1024
    for i in range(0, n, block):
        p = i / n
        fc = f0 * (f1 / f0) ** p
        seg = noise[i : i + block]
        sos = signal.butter(2, [fc * 0.7, min(fc * 1.4, SR / 2 - 100)], btype='bandpass', fs=SR, output='sos')
        out[i : i + block] = signal.sosfilt(sos, seg)
    shape = np.linspace(0, 1, n) ** 2.2
    sweep_f = 110 * (4 ** np.linspace(0, 1, n))
    sweep = np.sin(2 * np.pi * np.cumsum(sweep_f) / SR) * 0.25
    return (out * 0.9 + sweep) * shape * level


def whoosh(beats=1.0, level=1.0):
    return riser(beats, level, 800, 12000)


def pluck(note, level=1.0, dur=0.22):
    n = int(dur * SR)
    x = saw(hz(note), n) + saw(hz(note), n, 0.006)
    x = sos_filter(x, 'lowpass', 3200)
    return x * env_exp(n, 0.07) * level


def bass_note(note, beats, level=1.0):
    n = t(beats)
    x = saw(hz(note), n) * 0.7 + np.sin(2 * np.pi * hz(note) * np.arange(n) / SR)
    x = sos_filter(x, 'lowpass', 420)
    a = np.minimum(1, np.arange(n) / (0.004 * SR))
    r = np.minimum(1, (n - np.arange(n)) / (0.02 * SR))
    return np.tanh(x * 1.4) * a * r * level


def pad(notes, beats, level=1.0, attack=0.6, cutoff=2400):
    n = t(beats)
    x = np.zeros(n)
    for note in notes:
        for d in (-0.008, -0.003, 0.0, 0.004, 0.009):
            x += saw(hz(note), n, d)
    x = sos_filter(x / (len(notes) * 5), 'lowpass', cutoff)
    a = np.minimum(1, np.arange(n) / (attack * SR))
    r = np.minimum(1, (n - np.arange(n)) / (0.4 * SR))
    return x * a * r * level




# ---------- lead + hook ----------
def lead_note(note, beats, level=1.0):
    n = t(beats)
    x = sum(saw(hz(note), n, d) for d in (-0.007, 0.0, 0.006)) / 3
    x = sos_filter(x, 'lowpass', 4200)
    a = np.minimum(1, np.arange(n) / (0.005 * SR))
    e = 0.6 + 0.4 * env_exp(n, 0.12)
    r = np.minimum(1, (n - np.arange(n)) / (0.03 * SR))
    return x * a * e * r * level


# A 2-bar hook in A minor, 8th-note feel: (midi note, beats). Catchiness comes from repeating it on every drop.
MOTIF = [(76, 1), (74, 0.5), (72, 0.5), (69, 1), (72, 0.5), (74, 0.5), (76, 1), (79, 0.5), (76, 0.5), (74, 0.5), (72, 0.5), (69, 1)]


def lead(buf, b0, b1, level=0.22, motif=MOTIF):
    """Play the motif from beat b0 to b1 into buf, with a dotted-8th echo."""
    dry = np.zeros(len(buf))
    bt = b0
    while bt < b1:
        for note, d in motif:
            if bt >= b1:
                break
            add(dry, t(bt), lead_note(note, d * 0.9, level))
            bt += d
    delay = t(0.75)
    echo = np.zeros(len(buf))
    echo[delay:] = dry[:-delay] * 0.3
    echo[2 * delay:] += dry[: -2 * delay] * 0.12
    buf += dry + sos_filter(echo, 'lowpass', 2500)


# Am · F · C · G — (bass root midi, chord notes) per bar
PROG = [(33, [57, 60, 64, 69]), (29, [53, 57, 60, 65]), (36, [55, 60, 64, 67]), (31, [55, 59, 62, 67])]


def groove(drums, music, b0, b1, kicks, claps=True, hats=True, bass=True, pads=True):
    """Four-on-the-floor section from beat b0 to b1. Appends kick sample positions to `kicks` for the sidechain."""
    for bt in np.arange(b0, b1, 1.0):
        add(drums, t(bt), kick())
        kicks.append(t(bt))
        if claps and int(round(bt)) % 2 == 1:
            add(drums, t(bt), clap(0.7))
        if hats:
            add(drums, t(bt + 0.5), hat(True, 0.26))
            for s in (0.25, 0.75):
                add(drums, t(bt + s), hat(False, 0.15))
        root, _ = PROG[int((bt - b0) // 4) % 4]
        if bass:
            add(music, t(bt + 0.5), bass_note(root + 12, 0.45, 0.55))
            add(music, t(bt + 0.75), bass_note(root + 12, 0.2, 0.3))
    if pads:
        for bar in np.arange(b0, b1, 4.0):
            _, notes = PROG[int((bar - b0) // 4) % 4]
            add(music, t(bar), pad(notes, min(4, b1 - bar), 0.18, attack=0.05))


# ---------- mix helpers ----------
def sidechain(n, kicks, depth=0.6, tau=0.09):
    """Gain curve that ducks the music bus after each kick (the 'pump')."""
    sc = np.ones(n)
    for k in kicks:
        m = min(n - k, int(0.3 * SR))
        if m > 0:
            sc[k:k + m] = np.minimum(sc[k:k + m], 1 - depth * env_exp(m, tau))
    return sc


def silence(buf, b0, b1):
    """Hard gate between two beats (with a short fade-in to the gap): the 'lights out' before a reveal."""
    a, z = t(b0), t(b1)
    buf[a:z] *= np.linspace(1, 0, z - a) ** 3
    buf[max(a, z - int(0.02 * SR)):z] = 0


def load_sound(path):
    """Any audio file → mono float array at SR (via ffmpeg). Use for the product's own UI sounds."""
    raw = subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', str(path), '-ac', '1', '-ar', str(SR), '-f', 's16le', '-'],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.int16).astype(np.float64) / 32768


def master(x, total_beats=None, fade_s=0.8):
    """Trim, fade out, soft-clip and normalize to -1 dBFS sample peak. Then run limit() for loudness."""
    if total_beats:
        x = x[: int(total_beats * BEAT_S * SR)]
    f = int(fade_s * SR)
    x = x.copy()
    x[-f:] *= np.linspace(1, 0, f)
    x = np.tanh(x)
    return x / (np.max(np.abs(x)) + 1e-9) * 0.89


def write_wav(path, x, gain_db=-3.0, limit=0.8):
    """Write stereo 16-bit WAV, then ffmpeg gain + limiter. Measure after: target -14..-12 LUFS, TP <= -1 dBFS."""
    raw = str(path) + '.raw.wav'
    pcm = (np.clip(x, -1, 1) * 32767).astype(np.int16)
    with wave.open(raw, 'wb') as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(np.repeat(pcm[:, None], 2, axis=1).tobytes())
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', raw, '-af',
                    f'volume={gain_db}dB,alimiter=limit={limit}:attack=4:release=80:level=false', str(path)], check=True)
    import os
    os.remove(raw)
