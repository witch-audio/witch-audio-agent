#!/usr/bin/env python3
"""Simple WAV null-test helper using Python stdlib.

Usage:
  python wav_null_test.py file_a.wav file_b.wav

Works best on PCM WAV files with matching format.
Prints sample counts, peak diff, rms diff, and a rough verdict.
"""

from __future__ import annotations

import math
import sys
import wave
import audioop
from pathlib import Path


def read_wav(path: Path):
    with wave.open(str(path), 'rb') as wf:
        params = wf.getparams()
        frames = wf.readframes(wf.getnframes())
    return params, frames


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: python wav_null_test.py file_a.wav file_b.wav")
        return 2

    a_path = Path(sys.argv[1])
    b_path = Path(sys.argv[2])

    a_params, a_frames = read_wav(a_path)
    b_params, b_frames = read_wav(b_path)

    if a_params[:4] != b_params[:4]:
        print("format mismatch:")
        print(f"A: {a_params}")
        print(f"B: {b_params}")
        return 1

    width = a_params.sampwidth
    frame_count = min(a_params.nframes, b_params.nframes)
    byte_count = frame_count * a_params.nchannels * width
    a_frames = a_frames[:byte_count]
    b_frames = b_frames[:byte_count]

    diff = audioop.add(a_frames, audioop.mul(b_frames, width, -1.0), width)
    peak = audioop.max(diff, width)
    rms = audioop.rms(diff, width)

    max_possible = float((1 << (8 * width - 1)) - 1)
    peak_dbfs = -999.0 if peak == 0 else 20.0 * math.log10(peak / max_possible)
    rms_dbfs = -999.0 if rms == 0 else 20.0 * math.log10(rms / max_possible)

    print(f"frames_compared: {frame_count}")
    print(f"channels: {a_params.nchannels}")
    print(f"sample_width_bytes: {width}")
    print(f"sample_rate: {a_params.framerate}")
    print(f"peak_diff: {peak} ({peak_dbfs:.2f} dBFS)")
    print(f"rms_diff: {rms} ({rms_dbfs:.2f} dBFS)")

    if peak == 0:
        print("verdict: perfect null")
    elif rms_dbfs < -90:
        print("verdict: extremely close")
    elif rms_dbfs < -60:
        print("verdict: small but audible difference possible")
    else:
        print("verdict: significant difference")

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
