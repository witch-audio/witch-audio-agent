---
name: ableton-agent-control
description: Ableton Live control skill for witch.audio. Uses AbletonOSC, Max for Live, Live Object Model, and MIDI Remote Scripts to give an agent structured Live control without depending on blind UI clicks.
version: 1.0.0
author: witch audio
license: MIT
metadata:
  hermes:
    tags: [ableton, live, daw, automation, agent-control, max-for-live, osc, mcp, macos]
    related_skills: [witch-audio-identity, ableton-live-workflows, daw-automation-macos]
---

# Ableton Agent Control

Use this skill when witch.audio needs real control over Ableton Live.

## Core reality

Live is controllable.
But clean control usually needs a bridge.
Best paths are:
- AbletonOSC
- Max for Live device
- Live Object Model
- MIDI Remote Scripts

Do not default to screen automation if a bridge can do job.

## Preferred control stack

1. Existing network bridge
   - AbletonOSC

2. Native in-Live bridge
   - Max for Live device using Live API / Live Object Model

3. Control-surface layer
   - MIDI Remote Scripts / control surface framework

4. Virtual MIDI fallback
   - for mapped transport and parameter control

5. UI fallback
   - only for dialogs, browser weirdness, or unsupported plugin windows

## Best tooling

### AbletonOSC

Community OSC bridge for Live.
Use for:
- transport
- tracks
- clips
- scenes
- devices
- parameters
- state queries

Why it matters:
- fastest path to a useful external agent bridge
- speaks network messages cleanly
- avoids rebuilding basics first

Repo:
- https://github.com/ideoforms/AbletonOSC

### Max for Live Live Object Model

Native object model inside Live.
Use for:
- song state
- track and clip traversal
- device and parameter inspection
- deeper structured control than MIDI alone

Docs:
- https://docs.cycling74.com/max8/vignettes/live_object_model
- https://docs.cycling74.com/max8/vignettes/live_api_overview
- https://docs.cycling74.com/apiref/js/liveapi/

### MIDI Remote Scripts / control surfaces

Python-based integration layer inside Live.
Use for:
- resident controller bridge
- session navigation
- device bank control
- transport and mixer control
- virtual controller tricks

Refs:
- https://help.ableton.com/hc/en-us/articles/209774285-Using-Control-Surfaces
- https://github.com/gluon/AbletonLive11_MIDIRemoteScripts
- https://github.com/Ableton/control-surface

## Best agent tasks

Great Live agent jobs:
- launch known scene
- arm exact track
- set tempo
- load exact set or template
- tweak mapped device parameter
- duplicate clip
- export a loop
- inspect device chain on a known track

Bad early jobs:
- searching browser freely with no deterministic naming
- editing giant live set with unstable track order
- pixel-driving plugin GUIs as main workflow

## Recommended architecture

Preferred architecture:
- local MCP server
- Live backend = AbletonOSC first
- M4L bridge second for deeper state
- virtual MIDI for mapped actions
- UI fallback only after semantic routes fail

Good tool surface:
- `ableton_get_set_info`
- `ableton_list_tracks`
- `ableton_arm_track`
- `ableton_launch_scene`
- `ableton_launch_clip`
- `ableton_list_devices`
- `ableton_set_device_param`
- `ableton_set_tempo`
- `ableton_export_audio`

Keep tools small and explicit.
Do not hand model a giant unstructured “control Live” hammer.

## Golden workflow

1. Verify Live open and target set loaded.
2. Confirm exact track / scene / clip identifiers.
3. Perform one action.
4. Read state back.
5. Continue only if state matches.

Example:
- confirm `Bass` track exists
- confirm device slot 1 is `Auto Filter`
- set cutoff
- read value back

## Good first capability set

Start with:
- set alive check
- list tracks
- arm track by exact name
- launch scene by index
- stop transport
- set tempo
- list devices on track
- set one mapped parameter
- export with known preset or manual recipe

Add browser actions much later.

## Harness posture

Use tiny deterministic `.als` sets.
Good harnesses:
- transport-smoke
- clip-launch-smoke
- device-param-smoke
- automation-stress
- save-reopen
- export-check

One question per set.
No chaotic all-in-one production file.

## Reliability rules

- prefer exact track names
- separate Session View from Arrangement assumptions
- keep fixed device slots in test sets
- verify armed state after arm command
- verify launched clip really changed state
- treat export preset and file path as explicit inputs

## Virtual MIDI use

Virtual MIDI useful when:
- mapped macro knobs already exist
- agent only needs a small fixed control surface
- Live API bridge not ready yet

Virtual MIDI weak when:
- agent needs semantic state
- agent must inspect track/device graph
- mappings drift between sets

## When to use UI fallback

Only for:
- file dialogs
- browser operations not exposed in bridge
- plugin GUI-only actions
- setup/install steps

Even then:
- focus Live
- verify view
- perform one move
- verify changed state semantically if possible

## Output style

Prefer:
- exact set
- exact track
- exact scene / clip / device
- exact parameter
- exact verification step

Example:
- Set: `automation-stress.als`
- Track: `Lead`
- Device: `Auto Filter`
- Param: `Frequency`
- Verify: parameter reads back expected normalized value

## Bottom line

Live needs bridge.
Bridge first.
Pixels last.
AbletonOSC fastest start.
M4L deepest path.
