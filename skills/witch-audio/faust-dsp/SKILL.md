---
name: faust-dsp
description: FAUST skill for witch.audio. Covers DSP prototyping, UI parameters, architecture files, export targets, and when to use FAUST versus hand-written C++ or Web Audio code.
version: 1.0.0
author: witch audio
license: MIT
metadata:
  hermes:
    tags: [faust, dsp, audio, prototyping, c++, web-audio]
---

# FAUST DSP

Use this skill when the task involves FAUST, DSP prototyping, quick effect design, or exporting the same DSP idea to multiple targets.

## Why FAUST matters

FAUST is great when you want:
- fast DSP iteration
- portable algorithms
- one signal graph expressed cleanly
- export to plugin, web, standalone, or embedded targets

## Reach for FAUST when

- the algorithm matters more than framework plumbing
- you want to prototype filters/effects quickly
- you may target both native and web later
- the DSP can be described as signal flow cleanly

## Do not force FAUST when

- the hard part is host/framework integration
- the product is mostly custom UI/app logic
- the DSP is tiny and the surrounding system is the real challenge

## Core mental model

Think in:
- signals
- composition
- controls
- architecture/export target

Separate:
- DSP logic
- target-specific wrapper code

## Common building blocks

You will often combine:
- oscillators
- filters
- envelopes
- delays
- waveshapers
- mixers
- routing/composition operators

## UI controls

Use FAUST UI elements for:
- gain
- cutoff
- resonance
- mix
- modulation depths

Be careful with:
- parameter ranges
- units in labels
- defaults that explode feedback or clipping

## Export strategy

Typical paths:
- native plugin prototype
- C++ for JUCE integration
- Web Audio / wasm
- standalone test app

## Good workflow

1. prototype the DSP in FAUST
2. verify sound and parameter behavior
3. export to the right target
4. only then wrap in larger product/UI logic

## Common pitfalls

- clipping because defaults are too hot
- parameter ranges not musical
- forgetting sample-rate dependence
- blaming the DSP when the wrapper/export layer is broken
- making the FAUST graph too clever to debug

## FAUST vs JUCE vs Web Audio

Use FAUST for:
- algorithm prototyping
- reusable DSP cores
- quick experiments

Use JUCE for:
- plugin productization
- host integration
- richer native UI and state management

Use Web Audio for:
- browser-first tools
- fast distribution
- lightweight interactive apps

## Output style

When helping, prefer:
- whether FAUST is the right tool here
- a simple signal-chain sketch
- control names and ranges
- export target recommendation

Prototype fast.
Then decide if it deserves hand-written framework glue.
