---
name: logic-agent-control
description: Logic Pro control skill for witch.audio. Uses Hammerspoon, macOS Accessibility, PyObjC, cliclick, PyXA, and computer-use fallback patterns to operate Logic without pretending it has a deep public DAW scripting API.
version: 1.0.0
author: witch audio
license: MIT
metadata:
  hermes:
    tags: [logic-pro, daw, automation, agent-control, accessibility, macos, hammerspoon, pyobjc]
    related_skills: [witch-audio-identity, logic-pro-workflows, daw-automation-macos]
---

# Logic Agent Control

Use this skill when witch.audio needs to control Logic Pro from an agent.

## Core reality

Logic has weakest public automation surface of the big three here.
Do not pretend Logic has REAPER-style scripting.
Treat Logic as:
- thin AppleScript app
- strong keyboard-command target
- Accessibility target
- menu/dialog automation target
- MIDI/control-surface target when mapped well

## Native scripting truth

Logic exposes only minimal standard AppleScript commands well.
Good for:
- launch
- activate
- open project
- quit

Not good for:
- deep track inspection
- plugin graph introspection
- semantic edit control

So real Logic automation stack is mostly macOS automation.

## Preferred control stack

1. Hammerspoon or PyObjC Accessibility inspection
2. key commands and menu paths
3. cliclick / synthetic input for actuation
4. PyXA for surrounding macOS scripting tasks
5. computer-use fallback for weird UI states or plugin windows

## Best tooling

### Hammerspoon

Best pragmatic local automation layer on macOS.
Use for:
- frontmost app checks
- window focus
- Accessibility tree access
- synthetic key presses
- running AppleScript / JXA

Docs:
- https://www.hammerspoon.org/docs/
- https://www.hammerspoon.org/docs/hs.axuielement.html
- https://www.hammerspoon.org/docs/hs.application.html
- https://www.hammerspoon.org/docs/hs.eventtap.html
- https://www.hammerspoon.org/docs/hs.osascript.html

### PyObjC

Python access to macOS frameworks.
Use for:
- Accessibility APIs
- ScriptingBridge
- native permission checks
- building Python helpers and background daemons

Docs:
- https://pyobjc.readthedocs.io/en/latest/
- https://pyobjc.readthedocs.io/en/latest/apinotes/ApplicationServices.html
- https://pyobjc.readthedocs.io/en/latest/apinotes/ScriptingBridge.html
- https://developer.apple.com/documentation/applicationservices/1462085-axuielementcreateapplication

### cliclick

CLI input primitive.
Use for:
- clicks
- drags
- key combos
- typing
- short repeatable UI actuations

Repo:
- https://github.com/BlueM/cliclick

### PyXA

High-level Python macOS automation.
Use for:
- surrounding app automation
- file and dialog help
- Apple event style tasks around Logic

Repo:
- https://github.com/SKaplanOfficial/PyXA

### Computer-use fallback

Use when AX data weak or custom plugin UI defeats inspection.
Useful refs:
- https://docs.anthropic.com/en/docs/build-with-claude/computer-use
- https://platform.openai.com/docs/guides/tools-computer-use
- https://github.com/microsoft/OmniParser

## Best agent tasks

Great Logic agent jobs:
- open known project template
- trigger known key command
- open mixer / inspector / library
- bounce project or selection with fixed recipe
- create track with repeatable menu path
- save copy and reopen
- verify app state before QA pass

Bad early jobs:
- deep semantic session edits with no UI recipe
- freeform plugin GUI control as main workflow
- assuming UI layout same on every machine

## Recommended architecture

Build small local automation service or MCP server.
Tools should be semantic but backed by UI recipes.

Good tool surface:
- `logic_is_running`
- `logic_open_project`
- `logic_focus`
- `logic_send_key_command`
- `logic_run_menu_path`
- `logic_open_mixer`
- `logic_bounce_project`
- `logic_save_project_copy`
- `logic_capture_ui_state`

Under hood use:
- Hammerspoon or PyObjC for inspect
- cliclick or eventtap for act
- optional screenshot/computer-use fallback for plugin windows

## Golden workflow

1. Verify Logic running.
2. Verify frontmost app.
3. Verify expected window or menu state.
4. Perform one key/menu action.
5. Verify UI changed.
6. Continue.

Never chain many blind UI steps with no checkpoint.

## Good first capability set

Start with:
- app alive check
- activate app
- open exact project path
- trigger exact key command
- open mixer
- bounce using saved recipe
- save and reopen project
- capture screenshot or AX summary for verification

Avoid track graph introspection promises until proven.

## Harness posture

Use tiny dedicated Logic projects.
Good harnesses:
- AU-load-smoke
- automation-jump-test
- bounce-check
- reopen-recall
- menu-path-smoke

Name templates and key commands clearly.
Document menu paths exactly.

## Reliability rules

- keep Logic key command set stable
- prefer keyboard shortcuts over deep mouse travel
- keep window layout deterministic
- verify menu item exists before clicking
- verify bounce dialog state before submit
- fall back to screenshot/computer-use only when AX path weak

## Accessibility posture

Before trying automation:
- verify Accessibility permissions granted
- verify Hammerspoon or Python helper trusted
- verify screen resolution / layout assumptions if clicks used

Permission bugs look like agent bugs.
They are not same thing.

## When to use computer use

Use only for:
- custom plugin GUIs
- popups not exposed cleanly in AX tree
- visual confirmation tasks
- recovery from unexpected modal state

Computer use is rescue layer.
Not main architecture.

## Output style

Prefer:
- exact Logic project
- exact key command or menu path
- exact dialog state to verify
- exact post-action checkpoint

Example:
- Project: `AU-load-smoke.logicx`
- Action: open mixer
- Path: key command `X`
- Verify: mixer window visible and frontmost

## Bottom line

Logic agent control is possible.
But it is macOS automation problem first.
Use inspected UI recipes.
Use key commands hard.
Use computer-use only when needed.
