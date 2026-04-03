---
name: audio-dsp
description: Practical audio DSP skill for witch.audio. Covers filters, oscillators, effects, signal flow, artifact diagnosis, and implementation heuristics for audio programmers.
version: 1.0.0
author: witch audio
license: MIT
metadata:
  hermes:
    tags: [audio, dsp, filters, synthesis, plugins, debugging]
---

# Audio DSP

Use this skill when the task involves audio engines, plugin internals, signal flow, artifact diagnosis, or turning a sound description into implementation choices.

## Default posture

Diagnose before prescribing.

First ask or infer:
- sample rate
- block size / buffer size
- mono or stereo path
- where modulation happens
- where nonlinearity happens
- whether the bug is constant, transient, or parameter-dependent

## Core mental model

A DSP bug usually lives in one of six places:
1. source generation
2. parameter smoothing
3. time-domain state
4. nonlinear stage
5. feedback path
6. output gain / mix staging

Trace the signal in that order.

## Filters

### Good default choices
- transparent utility EQ / tone shaping: biquad
- synth low-pass with character: ladder-style or ZDF/TPT filter
- steep cleanup: cascaded biquads
- DC cleanup: one-pole high-pass around 20 Hz or lower

### Common filter bugs
- zipper noise from unsmoothed cutoff/Q
- instability when resonance is modulated too fast
- denormals in low-level tails
- coefficient recalculation every sample without need
- wrong sample-rate normalization after host rate change
- gain jumps when switching filter mode

### Fast checks
- sweep cutoff with high resonance at 44.1k and 96k
- automate cutoff with a square-ish host automation lane
- feed impulse, sine, white noise
- verify bypass null or near-null if intended

## Oscillators

### Pick the right approach
- simplest / dirty prototype: naive oscillator
- musical production oscillator: band-limited or polyBLEP/polyBLAMP
- memory-heavy but efficient: wavetable with mip levels
- highly modulated shapes: differentiated polynomial / BLEP-style correction

### Common oscillator bugs
- aliasing above midrange pitches
- phase reset clicks on note-on
- drift between stereo channels when unintended
- wavetable interpolation noise
- DC offset in asymmetric shapes

### Rules of thumb
- if it bends, syncs, or distorts, aliasing gets worse fast
- hard sync + FM + distortion needs a more careful anti-aliasing story
- oversample around nonlinear stages before oversampling the whole synth

## Effects

### Delay / chorus / flanger
- smooth delay-time changes or crossfade taps
- guard against interpolation artifacts
- clamp feedback below instability unless chaos is intentional
- expect clicks when modulated delay reads jump discontinuously

### Reverb
- debug in this order: predelay, early reflections, diffusion, decay, damping, wet gain
- if tails ring oddly, inspect feedback matrix and damping filters
- if stereo field collapses, inspect channel correlation in late field

### Distortion / saturation
- add pre/post gain controls
- remove DC before heavy waveshaping
- oversample around the nonlinear block when aliasing matters
- match loudness when comparing dry/wet or modes

## Parameter smoothing

If a parameter can move while audio runs, assume it needs smoothing.

Good smoothing candidates:
- gain
- cutoff
- resonance
- delay time
- pan
- wet/dry mix
- oscillator pitch when driven by UI or automation

Not every modulated signal should be smoothed the same way:
- UI gestures: slower smoothing is okay
- host automation: medium and predictable
- audio-rate modulation: do not replace with slow smoothing; use a DSP-safe modulation path

## Artifact diagnosis map

### Clicks / pops
Likely causes:
- discontinuity in waveform or buffer boundaries
- note on/off envelope jump
- delay-time jump
- bypass switch discontinuity
- resetting state mid-buffer

### Aliasing
Likely causes:
- naive oscillator at high frequency
- distortion without oversampling
- hard sync / FM with insufficient band-limiting

### Mud / loss of clarity
Likely causes:
- too much low-mid buildup
- wet signal without pre-EQ
- chorus/reverb widening without mono sanity checks
- nonlinear stage generating excessive low-order harmonics

### Thin / hollow / phasey
Likely causes:
- polarity issue
- dry/wet latency mismatch
- stereo decorrelation too aggressive
- comb filtering from duplicated paths

### CPU spikes
Likely causes:
- coefficient recalculation too often
- allocations in audio thread
- logging on audio thread
- denormals
- oversampling too broadly

## Audio-thread rules

Never do these on the realtime thread if avoidable:
- heap allocation
- file IO
- locks that can block
- network calls
- verbose logging
- expensive object creation per block

## Debug workflow

1. Reproduce with the smallest possible patch.
2. Test sine, impulse, silence, white noise.
3. Disable modules one by one.
4. Inspect automation and smoothing.
5. Compare 44.1k vs 48k vs 96k.
6. Test extreme parameter values.
7. Check denormals, clipping, DC, and feedback stability.

## Output style

When helping, prefer:
- likely root cause
- exact subsystem to inspect
- minimal fix
- verification step

Keep it practical. Less textbook, more signal chain.
