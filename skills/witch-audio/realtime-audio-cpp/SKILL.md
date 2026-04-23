---
name: realtime-audio-cpp
description: Realtime audio C++ skill for witch.audio. Covers audio-thread safety, lock-free patterns, buffering, denormals, parameter flow, and performance debugging for native audio engines.
version: 1.0.0
author: witch audio
license: MIT
metadata:
  hermes:
    tags: [c++, realtime-audio, dsp, plugin-dev, performance]
---

# Realtime Audio C++

Use this skill when the task touches native audio engines, plugin internals, lock-free communication, or performance-sensitive DSP code.

## First law

The audio thread is sacred.
No blocking.
No surprise allocation.
No waiting on anybody.

## Never do this on the audio thread

- heap allocation
- file IO
- network IO
- mutexes that can block
- condition-variable waits
- logging in hot paths
- rebuilding large objects every callback

## Safe mental model

Split the system into:
- audio thread: deterministic, fast, boring
- message/UI thread: flexible, slower
- background workers: prep, analysis, loading, rendering, indexing

## Common patterns

### Parameter flow
Use:
- atomics for simple values
- smoothed values for click-prone params
- double-buffered state snapshots for bigger config changes

### Audio/UI communication
Reach for:
- lock-free queues
- ring buffers
- atomic flags
- immutable snapshots swapped at block boundaries

### Resource loading
Do heavy prep off-thread.
Swap in ready-to-use objects at safe boundaries.

## Lock-free guidelines

Good use cases:
- meter data back to UI
- MIDI/event queues
- automation/event transfer
- analysis summaries

Bad use cases:
- trying to make every complex object lock-free
- mutating shared graphs from two threads at once

## Performance checklist

Check these first:
- allocations in callback
- expensive coefficient math every sample
- branchy inner loops
- denormals in tails
- cache-unfriendly buffer access
- oversampling in the wrong place
- UI repaints affecting core engine timing

## Denormals

If CPU spikes appear during silence or fades, suspect denormals.

Typical fixes:
- use platform flush-to-zero / denormals-are-zero controls
- add tiny DC/noise where acceptable
- structure filters and feedback paths carefully

## Buffering rules

Think clearly about:
- interleaved vs non-interleaved layouts
- frame count vs sample count
- channel ownership
- read/write boundaries
- sample-rate changes between preparation and runtime

## Realtime-safe object lifecycle

Prefer:
- preallocate scratch buffers
- object pools when needed
- prepare/reset steps outside the callback
- swapping pointers only when fully valid

## Common bug map

### Random crackles under UI interaction
Likely:
- hidden lock contention
- callback allocation
- parameter storm without smoothing

### Works fine, then glitches after minutes
Likely:
- state leak
- queue growth
- denormals
- background task interfering with shared state

### CPU jumps only at silence
Likely:
- denormals
- weird feedback decay path

### Host automation causes clicks
Likely:
- unsmoothed parameters
- full object rebuilds on automation change

## Good response style

When helping, say:
- what thread owns the problem
- what pattern to replace
- what safe primitive to use instead
- how to verify under load

Keep it practical.
Less textbook.
More callback discipline.
