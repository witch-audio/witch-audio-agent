---
name: reaper-workflows
description: REAPER workflow skill for witch.audio. Covers repeatable test projects, routing sanity, render checks, plugin QA, and practical engineering workflows inside REAPER.
version: 1.0.0
author: witch audio
license: MIT
metadata:
  hermes:
    tags: [reaper, daw, routing, plugin-qa, rendering]
---

# REAPER Workflows

Use this skill when the user is in REAPER.

## Why REAPER is great here

REAPER is excellent as a test lab.
It is lightweight, scriptable, and very good for repeatable render/recall workflows.

## Best uses

- plugin load and automation tests
- routing and channel-count tests
- render comparison passes
- stress projects with many instances
- utility engineering workflows

## Good REAPER project harnesses

- multichannel routing test
- automation torture test
- silence/denormal test
- render/null test
- recall/reopen test

## REAPER-specific habits

- keep tiny dedicated `.rpp` test projects
- name tracks and FX slots precisely
- save render outputs beside the test project
- use REAPER as the lab even if the user composes elsewhere

## Included workflow assets

- `templates/reaper-plugin-harness-checklist.md`
- `scripts/setup_reaper_harness.py`

Use them to create a repeatable REAPER lab instead of improvising tests.

## Output style

Prefer:
- exact REAPER project harness
- exact routing or FX slot to inspect
- exact render check
- one next debugging move
