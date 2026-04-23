---
name: max-msp-gen
description: Max/MSP and gen~ skill for witch.audio. Covers patching strategy, gen~ DSP translation, prototyping flow, and moving ideas from patch to production.
version: 1.0.0
author: witch audio
license: MIT
metadata:
  hermes:
    tags: [max-msp, gen, dsp, prototyping, audio]
---

# Max/MSP + gen~

Use this skill for Max patch design, gen~ DSP work, and turning experimental patches into cleaner systems.

## Best use

Reach for Max when:
- exploration matters
- interaction matters
- routing is part of the art
- you need to hear the idea fast

Reach for gen~ when:
- sample-level DSP matters
- patch performance matters
- the algorithm is stable enough to formalize

## Workflow

1. sketch in MSP
2. isolate the real DSP idea
3. move tight DSP into gen~
4. simplify UI and routing
5. export or rewrite if productizing

## Common mistakes

- sprawling patches with no modules
- hiding state everywhere
- using MSP where gen~ should own the DSP
- making clever patches no one can debug later

## Output style

Prefer:
- patch structure
- what stays in MSP
- what moves to gen~
- cleanup path for production
