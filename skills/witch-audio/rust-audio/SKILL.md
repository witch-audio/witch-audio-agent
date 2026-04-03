---
name: rust-audio
description: Rust audio skill for witch.audio. Covers realtime-safe Rust patterns, DSP crates, plugin architecture, and where Rust shines for audio tooling.
version: 1.0.0
author: witch audio
license: MIT
metadata:
  hermes:
    tags: [rust, audio, dsp, plugin, realtime]
---

# Rust Audio

Use this skill when building audio tools in Rust, especially where safety and performance both matter.

## Why Rust here

Rust is great for:
- safer systems code
- DSP libraries and CLIs
- audio backends and tooling
- plugin engines where correctness matters

## Same realtime law as C++

No blocking.
No surprise allocation.
No sloppy thread ownership.

## Good focus areas

- offline audio tools
- analysis tools
- DSP libraries
- plugin/runtime cores
- audio data pipelines

## Common mistakes

- fighting ownership instead of simplifying the design
- pretending Rust removes realtime constraints
- over-abstracting hot DSP code

## Output style

Prefer:
- crate/library direction
- thread model
- data ownership model
- safest simple architecture
