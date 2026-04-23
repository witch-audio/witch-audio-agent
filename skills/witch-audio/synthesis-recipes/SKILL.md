---
name: synthesis-recipes
description: Sound-design translator for witch.audio. Converts moods, textures, and references into concrete synthesis recipes across subtractive, FM, granular, and wavetable methods.
version: 1.0.0
author: witch audio
license: MIT
metadata:
  hermes:
    tags: [synthesis, sound-design, fm, wavetable, granular, subtractive]
---

# Synthesis Recipes

Use this skill when someone describes a feeling, texture, or reference sound and wants the synthesis path, not theory homework.

## Translation rule

Convert this:
- mood
- texture
- motion
- brightness
- density
- reference artist/tool/song if given

Into this:
- synthesis method
- oscillator/source choice
- envelope shape
- filter behavior
- modulation sources
- spatial/effects chain

## Quick mappings

### Warm / soft / nostalgic
Start with:
- subtractive or gentle wavetable
- saw or pulse with low-pass filtering
- slightly slow attack
- mild saturation
- chorus or short reverb

### Cold / glassy / digital
Start with:
- FM or bright wavetable
- sharp transient
- high harmonic content
- narrow resonances
- stereo delay, shimmer, or crisp reverb

### Huge / cinematic / engulfing
Start with:
- layered detuned voices or granular cloud
- long attack/release if pad-like
- wide stereo modulation
- filtered reverb before final glue compression

### Dirty / broken / haunted
Start with:
- unstable pitch or sample-rate reduction
- asymmetrical distortion
- modulation that is slightly too deep
- filtered noise layer
- wow/flutter, chorus, or warped delay

### Rubber / boing / animated
Start with:
- pitch envelope
- resonant band-pass or low-pass ping
- short decay
- optional FM for bite

## Method chooser

### Subtractive
Best for:
- classic leads, basses, pads, plucks
- immediate control
- “make it warmer / darker / rounder” tasks

### FM
Best for:
- bells, glass, metallic strikes, electric tones
- complex brightness with small parameter changes
- precise digital edge

### Granular
Best for:
- clouds, ghosts, evolving textures, timestretched weirdness
- turning recordings into atmosphere

### Wavetable
Best for:
- animated modern synth tones
- smooth timbral scanning
- hybrid analog/digital feel

## Famous-sound decomposition habits

If a user references a sound, break it into:
- transient
- harmonic body
- motion
- noise component
- space component

Then rebuild with the fewest moving parts needed.

## Starter recipes

### Dreamy pad
- 2 detuned saws or mellow wavetable
- low-pass around medium brightness
- attack 200–800 ms
- release 1.5–5 s
- slow LFO on cutoff and pan
- chorus into long diffuse reverb

### Punchy synth bass
- saw + sine reinforcement
- fast amp attack
- short decay with moderate sustain
- low-pass with slight envelope amount
- optional soft clip after filter
- mono, controlled low end

### Glass bell
- FM with moderate to high mod index
- bright transient then decay of modulation amount
- little or no filter
- long tail reverb
- sparse stereo delay if needed

### Granular ambience
- field recording or vocal grain source
- medium grain size with jitter
- wide spread
- low-pass after cloud if harsh
- long reverb and gentle movement

## Prompt bridge for AI music tools

When asked for Suno/Udio style prompts, map the recipe into:
- genre / era anchor
- tempo or energy cue
- instrumentation / synthesis cue
- mood words
- mix adjectives

Example:
"dreamy pad with soft chorus" becomes something like:
- ambient synthwave atmosphere
- warm analog-style pads
- slow-moving chorus-drenched textures
- nostalgic, hazy, spacious

## Response template

Prefer this format:
- method
- source/oscillators
- envelope
- filter
- modulation
- effects
- one optional AI-music prompt line

Keep it buildable. One sound, one recipe.
