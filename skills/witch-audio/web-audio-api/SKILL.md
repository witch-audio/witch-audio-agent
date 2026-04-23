---
name: web-audio-api
description: Web Audio API skill for witch.audio. Covers AudioContext, routing, AudioWorklet patterns, browser latency gotchas, and fast scaffolds for browser-based audio tools.
version: 1.0.0
author: witch audio
license: MIT
metadata:
  hermes:
    tags: [web-audio, browser-audio, audio-worklet, javascript, typescript]
---

# Web Audio API

Use this skill when building browser-based synths, effects, analyzers, audio toys, or vibe-coded audio products.

## Default stack choices

Pick the simplest thing that will hold up:
- small prototype: Web Audio nodes + light UI
- custom DSP or sample-accurate work: `AudioWorklet`
- legacy fallback only when forced: `ScriptProcessorNode` is old and should not be the plan
- visualization: `AnalyserNode` or a separate data path

## Core graph mental model

Think in three layers:
1. source generation / media input
2. processing graph
3. output + metering + UI reflection

Do not tangle UI state with audio graph state more than needed.

## Fast scaffold

A reliable browser-audio MVP often looks like:
- button to unlock/start `AudioContext`
- one source node or worklet
- gain node for master level
- optional analyser
- tiny state store for parameters

## `AudioContext` realities

Remember:
- browsers often require a user gesture before audio starts
- context can be `suspended` and need `resume()`
- mobile/browser power policies can interrupt behavior
- sample rate is browser/device-dependent

## When to use `AudioWorklet`

Use `AudioWorklet` if you need:
- custom DSP
- low-latency scheduling
- stable per-sample logic
- synthesis beyond stock nodes
- clearer separation from main-thread UI jank

Avoid worklets for trivial node chaining if stock nodes already solve it.

## Browser gotchas

### No sound until button press
Likely autoplay policy. Create or resume context from a click/tap.

### Crackles during UI interaction
Likely main-thread contention, too much message passing, or work happening outside worklet boundaries.

### Timing feels sloppy
Likely relying on JS timers instead of audio clock scheduling.
Use `audioContext.currentTime`, not `setTimeout`, for musical timing.

### Inconsistent behavior across browsers
Check:
- `AudioWorklet` support and registration timing
- Safari quirks around node lifecycle
- sample-rate assumptions
- channel count defaults

## Latency discipline

To keep things responsive:
- push custom DSP into worklets
- keep main-thread rendering light
- batch parameter messages when possible
- use smoothing inside audio code for click-prone params
- avoid frequent graph teardown/rebuild

## Parameter control

Good pattern:
- UI changes local state
- local state updates audio params or posts messages to worklet
- audio side smooths anything click-prone

Params that often need smoothing:
- gain
- filter cutoff
- delay time
- wet/dry mix
- oscillator frequency if driven by coarse UI events

## Useful built-in nodes

Reach for these first:
- `GainNode`
- `BiquadFilterNode`
- `DelayNode`
- `StereoPannerNode`
- `ConvolverNode`
- `DynamicsCompressorNode`
- `AnalyserNode`
- `OscillatorNode`

## Vibe-coding patterns

### Fast audio toy
- one gesture to start audio
- one oscillator or sample source
- 2–4 meaningful controls
- one obvious sound immediately

### Browser effect box
- media input or uploaded file
- dry/wet mix
- one character control
- visual meter or waveform for delight

### Generative ambience tool
- seeded randomness
- slow modulation
- gain safety at output
- one export/share mechanic if productized

## Debug workflow

1. verify context state
2. verify graph connections
3. test with oscillator -> gain -> destination
4. isolate worklet vs UI thread issues
5. test in Chrome and Safari if it matters
6. inspect clipping, denormals, and message spam

## Output style

When helping, prefer:
- the smallest working graph
- exact node/worklet choice
- one likely browser gotcha
- one verification step

Build the instrument first. Make it pretty second.
