---
name: daw-automation-macos
description: macOS DAW automation skill for witch.audio. Uses Mac-native automation thinking to control DAWs, run repeatable plugin QA flows, bounce tests, and assist music-making on a real workstation.
version: 1.0.0
author: witch audio
license: MIT
metadata:
  hermes:
    tags: [macos, daw, automation, ableton, logic, reaper, qa]
---

# DAW Automation on macOS

Use this skill when witch.audio needs to operate a DAW on a Mac for testing or music-making.

## Core reality

There usually is no clean universal DAW API.
So the workflow is:
- identify the DAW
- identify what can be scripted reliably
- use repeatable UI automation carefully
- keep actions small and check state often

## Best uses

- opening a known test session
- loading a plugin on a known track slot
- running playback/bounce/reopen checks
- exporting stems or renders
- reproducing a bug in a host over and over
- assisting musical workflows with structured step lists

## Strong macOS automation posture

Prefer:
- explicit app focus
- deterministic window/layout assumptions
- one action at a time
- checkpoints after important moves
- saved DAW templates for repeatability

## Great DAW test harness pattern

Build dedicated sessions like:
- plugin-load-test
- automation-torture-test
- silence-denormal-test
- state-recall-test
- bounce-null-test

Then automate those sessions instead of improvising every time.

## Reliability rules

- do not assume the DAW is in the same layout every run
- verify the right app is frontmost
- verify transport state
- verify selected track/device before making destructive changes
- prefer templates over ad-hoc session building

## For QA

A good automated DAW pass on macOS can do:
1. open DAW
2. open a known session
3. insert plugin or load saved chain
4. run playback
5. automate one or two critical parameters
6. save / reopen if needed
7. bounce or record output
8. compare behavior / logs / measurements

## For music-making

Use automation to help with:
- loading templates
- routing instruments/effects
- bouncing stems
- exporting versions
- repetitive arrangement prep

Not everything should be automated.
Use it where repetition steals energy.

## Included workflow asset

- `references/repeatable-daw-harness.md`

Use it to design stable DAW templates before automating anything fragile.

## Output style

Prefer:
- exact DAW
- exact session/template
- exact automation goal
- likely fragile step
- verification checkpoint

The goal is not “control the DAW magically.”
The goal is repeatable workstation rituals.
