---
name: rnbo
description: RNBO skill for witch.audio. Covers portable patch design, export targets, parameter discipline, and getting musical logic from Max into apps and devices.
version: 1.0.0
author: witch audio
license: MIT
metadata:
  hermes:
    tags: [rnbo, max, export, web-audio, plugin]
---

# RNBO

Use this skill when building something in RNBO or planning to export patch logic into apps, plugins, or web tools.

## Best use

RNBO is strongest when you want:
- one musical core
- multiple deployment targets
- interactive systems moved beyond Max

## Design rules

- keep the exported core clean
- define parameters early
- avoid patch chaos before export
- separate musical logic from target-specific UI

## Common problems

- export works but controls feel wrong
- parameter names/ranges are not product-ready
- patch depends too much on Max-only assumptions

## Output style

Prefer:
- export target recommendation
- parameter cleanup
- what to simplify before export
- what wrapper code still belongs outside RNBO
