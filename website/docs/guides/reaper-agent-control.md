---
sidebar_position: 7
title: "REAPER Agent Control"
description: "Run the local REAPER MCP bridge, connect it to witch.audio, and use narrow semantic tools for DAW control."
---

# REAPER Agent Control

This guide shows how to connect witch.audio to a local REAPER session through MCP.

Goal:
- run a small local REAPER MCP server
- let witch.audio discover it as native tools
- use semantic REAPER actions instead of blind UI clicking

## What exists now

Current skeleton server lives here:

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

These are intentionally narrow.
Small verbs first. Bigger surface later.

## Prerequisites

Need all of these:

- REAPER installed
- REAPER running with a known project open
- this repo checked out locally
- MCP support installed for witch.audio
- Python environment for this repo
- `reapy` / `reapy-boost` installed when you want live backend control

## Install MCP support

If MCP extra not installed yet:

```bash
cd /Users/witchaudio/Developer/github-personal/witch-audio-agent
.venv/bin/python -m pip install -e ".[mcp]"
```

If using the repo venv directly, also make sure `mcp` import works:

```bash
cd /Users/witchaudio/Developer/github-personal/witch-audio-agent
.venv/bin/python -c "import mcp; print('mcp ok')"
```

## Install REAPER Python bridge

Live backend currently expects a `reapy`-compatible module.
Install one before trying real REAPER control:

```bash
cd /Users/witchaudio/Developer/github-personal/witch-audio-agent
.venv/bin/python -m pip install reapy-boost
```

Then verify import:

```bash
cd /Users/witchaudio/Developer/github-personal/witch-audio-agent
.venv/bin/python -c "import reapy; print('reapy ok')"
```

If this fails, `reaper_health` will report backend unavailable.

## Start the REAPER MCP server manually

From repo root:

```bash
cd /Users/witchaudio/Developer/github-personal/witch-audio-agent
.venv/bin/python integrations/reaper_mcp.py
```

This runs a local stdio MCP server.
Keep that process alive while witch.audio uses REAPER tools.

## Add server to witch.audio config

Edit `~/.hermes/config.yaml`.
Add a local stdio MCP server entry:

```yaml
mcp_servers:
  reaper:
    command: "/Users/witchaudio/Developer/github-personal/witch-audio-agent/.venv/bin/python"
    args:
      - "/Users/witchaudio/Developer/github-personal/witch-audio-agent/integrations/reaper_mcp.py"
    timeout: 30
    connect_timeout: 15
```

Notes:
- use absolute paths
- keep timeouts small at first
- if your repo uses another venv path, swap it in

## Restart witch.audio

After config change, restart the agent so MCP discovery runs again.

At startup witch.audio should discover the `reaper_*` tools from the local MCP server.

## Good first prompts

Use tiny known REAPER harness projects.
Good first prompts:

```text
Tell me whether the REAPER backend is healthy.
```

```text
List tracks in the current REAPER project.
```

```text
Select track DUT main.
```

```text
Insert ReaEQ on track DUT main.
```

```text
Play, then stop.
```

## Recommended harness posture

Do not test this on a giant music session first.
Use tiny dedicated `.rpp` files.

Good harness names:
- `00-plugin-load`
- `01-playback-basic`
- `02-automation-clicks`
- `03-recall-reopen`
- `04-render-check`

Best shape:
- one question per project
- exact track names
- exact FX slots
- exact verification after every action

## Troubleshooting

### `reaper_health` says backend unavailable

Most likely:
- REAPER not running
- `reapy` not installed
- REAPER Python bridge not reachable

Check:

```bash
cd /Users/witchaudio/Developer/github-personal/witch-audio-agent
.venv/bin/python -c "import reapy; print('reapy ok')"
```

### witch.audio does not see REAPER tools

Check:
- `mcp_servers.reaper` exists in `~/.hermes/config.yaml`
- absolute paths are correct
- server process starts without crashing
- witch.audio restarted after config change

### Track selection fails

Current v1 behavior uses exact track-name matching.
If the track is named `DUT main`, ask for `DUT main`.
Not `dut`, not `main`, not fuzzy.

### FX insert fails

Current v1 behavior expects an exact plugin name the backend can resolve.
Start with stock REAPER FX like `ReaEQ`.

## Current limitations

This is first skeleton only.
Not final REAPER control stack.

Current limits:
- no arbitrary action execution
- no item editing
- no render tools yet
- no parameter write tools yet
- no OSC bridge yet
- no UI fallback bridge yet

That is intentional.
Ship narrow. Expand after real use.

## Next expansion ideas

Natural next tools:
- `reaper_set_fx_param`
- `reaper_render_project`
- `reaper_add_marker`
- `reaper_list_regions`
- `reaper_run_named_action`

Only add after the small core feels solid.

## Bottom line

REAPER is first serious DAW control target for witch.audio.
Use MCP bridge.
Use semantic tools.
Use tiny harness sessions.
Trust state readback more than vibes.
