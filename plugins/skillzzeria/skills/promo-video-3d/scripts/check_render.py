#!/usr/bin/env python3
"""Automatic checks on a rendered video (needs ffmpeg/ffprobe on PATH; no Python deps).

  python3 check_render.py out/video.mp4 [--lufs -14] [--tp -1]     (also works on an audio-only file)

Reports: duration of each stream, isolated black frames (a black frame between two non-black ones —
the classic symptom of a 3D post-processing pass not being ready), integrated loudness and true peak.
Exit code 1 if black flashes are found or the audio is outside the targets (±2 LU, TP above limit).
"""
import argparse
import re
import subprocess
import sys

ap = argparse.ArgumentParser()
ap.add_argument('video')
ap.add_argument('--lufs', type=float, default=-14.0)
ap.add_argument('--tp', type=float, default=-1.0)
a = ap.parse_args()
bad = False

probe = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'stream=codec_type,duration', '-of', 'csv=p=0', a.video],
                       capture_output=True, text=True, check=True).stdout.split()
print('streams:', ', '.join(probe))

if any(s.startswith('video') for s in probe):
    raw = subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', a.video, '-vf', 'scale=16:9,format=gray', '-f', 'rawvideo', '-'],
                         capture_output=True, check=True).stdout
    n = 16 * 9
    means = [sum(raw[i * n:(i + 1) * n]) / n for i in range(len(raw) // n)]
    flashes = [i for i in range(1, len(means) - 1) if means[i] < 2 and means[i - 1] > 8 and means[i + 1] > 8]
    print(f'frames: {len(means)}  isolated black frames: {flashes or "none"}')
    bad |= bool(flashes)

if any(s.startswith('audio') for s in probe):
    out = subprocess.run(['ffmpeg', '-hide_banner', '-i', a.video, '-af', 'ebur128=framelog=quiet:peak=true', '-f', 'null', '-'],
                         capture_output=True, text=True).stderr
    i_m = re.findall(r'I:\s+(-?[\d.]+) LUFS', out)
    p_m = re.findall(r'Peak:\s+(-?[\d.]+) dBFS', out)
    if i_m and p_m:
        lufs, tp = float(i_m[-1]), float(p_m[-1])
        ok = abs(lufs - a.lufs) <= 2 and tp <= a.tp
        print(f'loudness: {lufs} LUFS (target {a.lufs}±2)  true peak: {tp} dBFS (max {a.tp})  {"ok" if ok else "OUT OF TARGET"}')
        bad |= not ok
else:
    print('no audio stream')
sys.exit(1 if bad else 0)
