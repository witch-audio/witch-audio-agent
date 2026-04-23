---
name: audio-analysis-measurement
description: Audio analysis and measurement skill for witch.audio. Covers spectrograms, frequency response, loudness, clipping, phase, null tests, and practical debugging measurements for audio tools and plugins.
version: 1.0.0
author: witch audio
license: MIT
metadata:
  hermes:
    tags: [audio-analysis, loudness, phase, spectrogram, measurement, qa]
---

# Audio Analysis and Measurement

Use this skill when the task is to prove what an audio tool is doing, not just guess.

## Core principle

Listen first.
Measure second.
Trust both.

## High-value measurements

Reach for:
- spectrum / spectrogram
- peak and RMS
- LUFS / loudness
- DC offset
- clipping detection
- phase correlation
- stereo width sanity
- null test
- impulse response / frequency response

## When each is useful

### Spectrogram
Best for:
- aliasing
- noisy modulation artifacts
- transient smear
- high-frequency junk

### Loudness / LUFS
Best for:
- comparing modes fairly
- checking level matching
- mastering/export sanity

### Null test
Best for:
- bypass accuracy
- verifying a claimed transparent path
- spotting subtle processing differences

### Phase / correlation
Best for:
- stereo weirdness
- widening collapse in mono
- accidental polarity inversion

### Impulse / frequency response
Best for:
- filters
- EQ curves
- reverb/linear system inspection

## Fast diagnosis map

### Sounds harsher than expected
Measure:
- spectrogram
- high-frequency buildup
- clipping
- aliasing above nonlinear stages

### Sounds smaller in mono
Measure:
- correlation
- polarity
- dry/wet latency mismatch

### Preset A seems better than B
Measure:
- LUFS or RMS first
- then compare tonality

### “Transparent” mode is not transparent
Do:
- null test
- level match first
- compare residual

## Practical test signals

Use these often:
- silence
- impulse
- sine sweep
- fixed sine tones
- white noise / pink noise
- drum loop
- dense mix
- sparse vocal/instrument sample

## Good workflow

1. define what you are trying to prove
2. choose the smallest meaningful signal
3. level match if comparing
4. measure the right domain
5. listen again to confirm interpretation

## Common mistakes

- comparing louder against quieter
- measuring the wrong part of the chain
- using only full-mix music when a sine sweep would reveal more
- trusting one meter without listening
- ignoring sample-rate and block-size context

## Reporting style

Prefer:
- test signal used
- metric observed
- likely implication
- next verification step

Example:
- Signal: 1 kHz sine at -12 dBFS
- Observation: extra sidebands visible after distortion
- Implication: expected harmonic generation plus possible aliasing
- Next step: oversample nonlinear stage and compare residual

Make the invisible obvious.
