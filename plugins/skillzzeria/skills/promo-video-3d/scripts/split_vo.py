#!/usr/bin/env python3
"""Cut one voice-over take (e.g. an ElevenLabs MP3) into one WAV per phrase (needs ffmpeg; no Python deps).

  python3 split_vo.py vo_raw.mp3 public/vo --phrases 14 [--tempo 1.07] [--db -40] [--min-sil 0.06]

Finds the pauses with ffmpeg `silencedetect`, keeps the N-1 longest ones as phrase boundaries (so short
breaths inside a phrase don't split it), and writes p01.wav … pNN.wav: 35 ms pre-roll, 70 ms post-roll,
optional speed-up (`atempo`), 8 ms fade-in / 30 ms fade-out, 48 kHz mono. Also writes durations.json
({id: seconds after tempo}) so the timeline can place each phrase and check it fits before the next one.
If fewer pauses than needed are found, lower --min-sil or raise --db and look at the printed gaps.
"""
import argparse
import json
import os
import re
import subprocess
import sys

ap = argparse.ArgumentParser()
ap.add_argument('src')
ap.add_argument('out_dir')
ap.add_argument('--phrases', type=int, required=True, help='number of phrases in the script')
ap.add_argument('--tempo', type=float, default=1.0, help='speed factor, e.g. 1.07 = 7%% faster, pitch kept')
ap.add_argument('--db', type=float, default=-40.0, help='silence threshold in dB')
ap.add_argument('--min-sil', type=float, default=0.06, help='minimum pause length in seconds')
ap.add_argument('--pre', type=float, default=0.035)
ap.add_argument('--post', type=float, default=0.070)
a = ap.parse_args()

dur = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', a.src],
                           capture_output=True, text=True, check=True).stdout)
log = subprocess.run(['ffmpeg', '-hide_banner', '-i', a.src, '-af', f'silencedetect=noise={a.db}dB:d={a.min_sil}',
                      '-f', 'null', '-'], capture_output=True, text=True).stderr
starts = [float(x) for x in re.findall(r'silence_start: (-?[\d.]+)', log)]
ends = [float(x) for x in re.findall(r'silence_end: ([\d.]+)', log)]
sil = list(zip(starts, ends + [dur] * (len(starts) - len(ends))))

# Leading/trailing silence are not boundaries.
inner = [(s, e) for s, e in sil if s > 0.01 and e < dur - 0.01]
if len(inner) < a.phrases - 1:
    sys.exit(f'found {len(inner)} inner pauses, need {a.phrases - 1}: {[(round(s, 2), round(e, 2)) for s, e in inner]}')
cuts = sorted(sorted(inner, key=lambda p: p[1] - p[0], reverse=True)[:a.phrases - 1])

speech_start = sil[0][1] if sil and sil[0][0] <= 0.01 else 0.0
speech_end = sil[-1][0] if sil and sil[-1][1] >= dur - 0.01 else dur
bounds = [speech_start] + [x for s, e in cuts for x in (s, e)] + [speech_end]
segs = [(bounds[i], bounds[i + 1]) for i in range(0, len(bounds), 2)]

os.makedirs(a.out_dir, exist_ok=True)
durations = {}
for i, (s, e) in enumerate(segs, 1):
    s0, e0 = max(0.0, s - a.pre), min(dur, e + a.post)
    out_len = (e0 - s0) / a.tempo
    pid = f'p{i:02d}'
    af = (f'atempo={a.tempo},' if a.tempo != 1 else '') + \
         f'afade=t=in:d=0.008,afade=t=out:st={max(0, out_len - 0.03):.3f}:d=0.03'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{s0:.3f}', '-to', f'{e0:.3f}', '-i', a.src,
                    '-af', af, '-ar', '48000', '-ac', '1', os.path.join(a.out_dir, f'{pid}.wav')], check=True)
    durations[pid] = round(out_len, 3)
    print(f'{pid}  {s0:6.2f}–{e0:6.2f} s  →  {out_len:.2f} s')

with open(os.path.join(a.out_dir, 'durations.json'), 'w') as f:
    json.dump(durations, f, indent=2)
print(f'{len(segs)} phrases → {a.out_dir}/ (durations.json written)')
