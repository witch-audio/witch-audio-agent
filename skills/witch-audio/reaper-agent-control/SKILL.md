---
name: reaper-agent-control
description: REAPER control skill for witch.audio. Turns REAPER into a first-class agent target using ReaScript, reapy-boost, Ultraschall, js_ReaScriptAPI, OSC, and a thin MCP bridge instead of brittle blind clicking.
version: 1.0.0
author: witch audio
license: MIT
metadata:
  hermes:
    tags: [reaper, daw, automation, agent-control, mcp, osc, reascript, macos]
    related_skills: [witch-audio-identity, reaper-workflows, daw-automation-macos, plugin-qa]
---

# REAPER Agent Control

Use this skill when witch.audio needs to control REAPER as a real tool target, not just as a window to click.

## Why REAPER first

REAPER is best DAW for agent control.
It has:
- official ReaScript support
- strong action system
- OSC support
- extension ecosystem
- practical Python bridges

If witch.audio is proving DAW control, start here.

## Preferred control stack

Use highest-reliability layer first.

1. Native project-aware control
   - ReaScript
   - Ultraschall API
   - reapy-boost

2. Extended REAPER control
   - js_ReaScriptAPI / ReaExtensions

3. Network transport
   - OSC

4. UI fallback
   - only for things REAPER APIs cannot express cleanly

Do not start with raw screen clicking if REAPER can do it semantically.

## Best tooling

### ReaScript

Official built-in scripting surface.
Use for:
- track and item operations
- FX chain operations
- transport control
- render actions
- markers / regions / project state

Docs:
- https://www.reaper.fm/sdk/reascript/reascript.php
- https://www.reaper.fm/sdk/reascript/reascripthelp.html

### reapy-boost

Python bridge to REAPER.
Use for:
- local Python tools
- agent-side wrappers
- structured project / track / item / FX access

Repo:
- https://github.com/Levitanus/reapy-boost

### Ultraschall API

High-level Lua helpers on top of REAPER.
Use for:
- richer scripting with less low-level boilerplate
- project and render helpers
- safer workflow recipes

Repo / docs:
- https://github.com/Ultraschall/ultraschall-lua-api-for-reaper
- https://mespotin.uber.space/Ultraschall/US_Api_Introduction_and_Concepts.html

### js_ReaScriptAPI / ReaExtensions

Extended API for windows and UI access.
Use for:
- dialogs
- window state
- menu and focus edge cases
- hybrid API + UI workflows

Repo:
- https://github.com/juliansader/ReaExtensions

### OSC

Official REAPER network control path.
Use for:
- transport
- mixer moves
- mapped parameter control
- external realtime control

Docs:
- https://www.reaper.fm/sdk/osc/osc.php

## Best agent tasks

Great REAPER agent jobs:
- open known project template
- create named tracks
- insert plugin in known slot
- set parameter values from a recipe
- render named pass
- compare recall / reopen behavior
- export stems from known regions
- build repeatable QA passes

Bad first jobs:
- freeform mouse-driving around arbitrary plugin UIs
- guessing hidden modal state
- editing huge messy sessions with no template discipline

## Recommended architecture

Build a thin MCP server in front of REAPER.

Agent tools should look like:
- `reaper_get_project_info`
- `reaper_list_tracks`
- `reaper_select_track`
- `reaper_insert_fx`
- `reaper_set_fx_param`
- `reaper_play`
- `reaper_stop`
- `reaper_render_project`
- `reaper_add_marker`
- `reaper_run_named_action`

Backends can be:
- reapy-boost for structured Python control
- ReaScript for trusted native actions
- OSC for realtime mapped controls

Keep tool names semantic.
Do not expose the whole DAW at first.
Expose stable verbs.

## Golden workflow

1. Verify REAPER running and frontmost when needed.
2. Open known test project or template.
3. Confirm project name and sample rate.
4. Confirm target track name or index.
5. Perform one semantic action.
6. Read back state.
7. Only then continue.

State readback matters.
Action without verification is fake automation.

## Good first capability set

Start with:
- app alive check
- active project path
- list tracks
- select track by exact name
- insert FX by exact plugin name
- set one FX parameter by normalized value
- play / stop / set cursor
- render using a known preset or action
- save project copy

Only add item editing after this works reliably.

## Harness posture

Pair this skill with tiny dedicated `.rpp` test projects.
Good harnesses:
- plugin-load-test
- playback-basic
- automation-clicks
- recall-reopen
- render-check

Use one question per project.
No giant omnibus session.

## Reliability rules

- prefer exact track names over indexes
- prefer known custom actions over menu traversal
- verify plugin inserted before setting params
- verify transport state after play/stop
- save outputs with deterministic filenames
- keep REAPER layout stable when UI fallback used

## MCP design notes

Good pattern:
- one local MCP server process
- Python implementation
- reapy-boost primary backend
- optional shell call or ReaScript dispatch for actions not covered well
- error messages return project, track, FX context

Avoid:
- one tool that accepts arbitrary code from the model
- raw eval surfaces
- giant “do anything” prompt-driven DAW tools

Curated tools beat infinite power.

## Local MCP setup

Current local server entrypoint:
- `integrations/reaper_mcp.py`

Current tool surface:
- `reaper_health`
- `reaper_get_project_info`
- `reaper_list_tracks`
- `reaper_select_track`
- `reaper_list_track_fx`
- `reaper_insert_fx`
- `reaper_play`
- `reaper_stop`
- `reaper_save_project`

Manual launch from repo root:

```bash
cd /Users/witchaudio/Developer/github-personal/witch-audio-agent
.venv/bin/python integrations/reaper_mcp.py
```

Hermes / witch.audio config example:

```yaml
mcp_servers:
  reaper:
    command: "/Users/witchaudio/Developer/github-personal/witch-audio-agent/.venv/bin/python"
    args:
      - "/Users/witchaudio/Developer/github-personal/witch-audio-agent/integrations/reaper_mcp.py"
    timeout: 30
    connect_timeout: 15
```

Live backend note:
- current backend expects a `reapy`-compatible module
- install `reapy-boost` before using live REAPER control
- if import fails, `reaper_health` should report backend unavailable clearly
- live render path currently works through MCP, but `reaper_render_project` may mutate REAPER render settings like output directory and pattern for the active project
- for serious automation, snapshot and restore render settings around the render call or use a dedicated harness project so one test run does not silently change later renders

## When to use UI fallback

Only when needed for:
- plugin windows with no exposed parameter map
- REAPER dialogs not easy to access semantically
- one-off install/config flows

Even then:
- focus app
- locate window
- checkpoint state
- act once
- verify result

## Output style

Prefer:
- exact project
- exact track
- exact FX slot
- exact parameter or action
- exact verification step

Example:
- Project: `02-automation-clicks/source.RPP`
- Track: `DUT main`
- Action: insert `Witch Audio Gain`
- Verify: FX count increased by 1 and slot name matches

## Bottom line

REAPER is not just DAW here.
REAPER is control substrate.
Use semantic tools first.
Use pixels last.
