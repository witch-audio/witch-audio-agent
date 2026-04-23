---
name: logic-pro-workflows
description: Logic Pro workflow skill for witch.audio. Covers plugin validation, session recall checks, bounce workflows, channel strip sanity, and music production help inside Logic.
version: 1.0.0
author: witch audio
license: MIT
metadata:
  hermes:
    tags: [logic-pro, daw, plugin-qa, production, macos]
---

# Logic Pro Workflows

Use this skill when the user is in Logic Pro.

## Best uses

- AU plugin validation
- channel strip and preset checking
- bounce and export sanity
- reopening projects to verify recall
- arrangement and production workflows

## Logic-specific habits

- treat project reopen as a first-class QA step
- test AU behavior in simple, dedicated projects
- keep named channel strips/templates for repeated checks
- verify Smart Controls and automation if the plugin exposes them

## Good Logic test projects

- AU load test
- automation jump test
- session recall test
- bounce/null comparison test

## For production

Use Logic well by:
- starting from a clean template
- separating writing from polish passes
- bouncing references early
- checking stereo image and low end before over-processing

## Output style

Prefer:
- exact Logic project template
- exact channel strip/plugin slot
- exact recall or bounce check
- one clear production move
