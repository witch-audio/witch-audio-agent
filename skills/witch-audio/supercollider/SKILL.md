---
name: supercollider
description: SuperCollider skill for witch.audio. Covers synthesis, pattern systems, live coding structure, server/client mental models, and turning sketchy experiments into usable instruments.
version: 1.0.0
author: witch audio
license: MIT
metadata:
  hermes:
    tags: [supercollider, synthesis, live-coding, patterns, audio]
---

# SuperCollider

Use this skill for SuperCollider synthesis, pattern systems, live coding, and sound-design workflows.

## Core mental model

Think in two worlds:
- language side: structure, patterns, orchestration
- server side: synthdefs, UGens, audio execution

## Best use cases

- experimental instruments
- generative music systems
- fast synthesis ideas
- live coding performance structures

## Common mistakes

- mixing language and server concerns carelessly
- giant messy live-code buffers
- no reusable SynthDefs
- beautiful chaos that cannot be repeated

## Good workflow

1. define a small SynthDef
2. verify sound and controls
3. build a pattern or routine around it
4. refactor repeated logic
5. save the usable pieces

## Output style

Prefer:
- SynthDef idea
- control set
- pattern/routine direction
- what to stabilize for reuse
