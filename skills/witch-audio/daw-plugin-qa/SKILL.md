---
name: daw-plugin-qa
description: DAW-based plugin QA skill for witch.audio. Uses real DAW sessions as test harnesses for plugins and audio apps, with repeatable host-side repro flows and musical stress tests.
version: 1.0.0
author: witch audio
license: MIT
metadata:
  hermes:
    tags: [daw, plugin-qa, ableton, logic, reaper, testing, automation]
---

# DAW Plugin QA

Use this skill when testing plugins or audio programs inside real DAWs.

## Key idea

A DAW is the test bench.
Not just the place you notice the bug.

## What this skill is for

- loading plugins in real hosts
- reproducing scan/load/state bugs
- stress testing automation
- testing musical use, not just sterile lab cases
- comparing host behavior across DAWs

## Good hosts to think about

- Ableton Live
- Logic Pro
- REAPER
- Bitwig
- FL Studio
- Pro Tools if needed

## QA passes inside a DAW

### 1. Load / scan pass
- does the plugin scan
- does it instantiate
- does UI open
- does bypass behave

### 2. Playback pass
- idle silence
- simple loop
- dense musical material
- extreme transient material

### 3. Automation pass
- automate key controls hard
- test ramps and stepped jumps
- toggle bypass while audio is active

### 4. Session pass
- save project
- close DAW
- reopen
- confirm state and sound match

### 5. Host-stress pass
- duplicate tracks
- increase polyphony or instance count
- change sample rate/buffer size

## Best practice

Build tiny dedicated DAW test sessions:
- synth torture session
- delay/reverb tail session
- automation torture session
- silence/denormal session
- session recall session

## Important reality

DAW control is usually host-specific.
If the agent is automating a DAW on a machine, use the platform tools available there:
- terminal
- browser/GUI automation when available
- Apple/macOS automation on Mac

So this skill should think in reproducible DAW workflows, not assume magical DAW APIs.

## Included workflow assets

- `templates/host-qa-session-checklist.md`
- `templates/plugin-bug-report.md`

Use them to keep host-side QA consistent.

## Output style

Prefer:
- host
- exact repro session setup
- what to automate
- expected vs actual
- likely subsystem

Make the DAW part of the method.
