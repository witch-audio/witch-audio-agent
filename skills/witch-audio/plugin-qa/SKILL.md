---
name: plugin-qa
description: Audio plugin QA skill for witch.audio. Covers fast repro workflows, artifact hunting, edge-case testing, and compact bug reporting for plugins and audio tools.
version: 1.0.0
author: witch audio
license: MIT
metadata:
  hermes:
    tags: [plugin-qa, audio-testing, juce, vst3, au, bug-reporting]
---

# Plugin QA

Use this skill when testing audio plugins, diagnosing weird host behavior, or building a reproducible QA checklist.

## Testing philosophy

Audio bugs hide in transitions and extremes.
Do not only test the sweet spot.

## Core test matrix

Always vary:
- sample rate: 44.1k / 48k / 96k
- buffer size: small, medium, large
- mono vs stereo
- silence vs sine vs music vs transients
- automation off vs aggressive automation
- fresh session vs restored session

## What to hunt for

### Audible artifacts
- clicks
- pops
- zipper noise
- aliasing
- crackle under modulation
- unexpected distortion
- denormal tail weirdness
- phase collapse in mono

### Product bugs
- parameter resets
- preset recall mismatch
- bypass mismatch
- UI desync with DSP state
- host automation not reflecting correctly
- state corruption after reopen
- crash on scan or unload

## High-value edge cases

Test these on purpose:
- extreme parameter min/max
- rapid automation sweeps
- toggling bypass while signal is active
- sample-rate change while loaded
- transport start/stop loops
- silence into heavy feedback or reverb
- clipping input
- no input / disconnected channels

## Repro workflow

1. Reduce the patch to the smallest failing setup.
2. Note host, OS, plugin format, sample rate, block size.
3. Identify whether the issue is audio-only, UI-only, or both.
4. Check if it happens on init, parameter move, note-on/off, or session restore.
5. Try to make it deterministic.

## Host sanity questions

Always capture:
- host/DAW name and version
- plugin format: VST3 / AU / AAX / standalone
- OS and CPU arch
- exact plugin version/build
- whether issue reproduces in a second host

## Fast checks by bug type

### Click on preset change
Likely causes:
- unsmoothed gain/filter changes
- DSP state reset discontinuity
- delay/reverb buffers not crossfaded or cleared carefully

### Host automation looks wrong
Likely causes:
- APVTS attachment/state sync issue
- parameter normalization mismatch
- UI text/value conversion bug

### CPU spike after silence
Likely causes:
- denormals
- runaway feedback path
- expensive idle processing still active

### Sound changes after reopen
Likely causes:
- incomplete state serialization
- missing non-parameter DSP state restore
- preset version migration issue

## Minimal report format

Use this structure:
- title
- environment
- steps to reproduce
- expected behavior
- actual behavior
- severity
- likely subsystem

## Example bug report

Title: Click when cutoff is automated quickly at high resonance
Environment: Ableton Live 12.1, macOS, AU, 48kHz, 128 samples
Steps:
1. Load plugin on synth track
2. Set resonance to 90%
3. Automate cutoff from 200 Hz to 8 kHz with fast ramps
Expected: smooth sweep
Actual: repeating clicks during steep transitions
Likely subsystem: filter coefficient update / smoothing

## Output style

Prefer:
- one repro recipe
- one likely subsystem
- one fix direction
- one verification pass

Make QA feel like a trap, not a checklist.
