---
name: plugin-release-pipeline
description: Plugin release pipeline skill for witch.audio. Covers pre-release checks, packaging, metadata, signing/notarization awareness, versioning, and launch-ready release discipline for audio plugins.
version: 1.0.0
author: witch audio
license: MIT
metadata:
  hermes:
    tags: [plugin-release, audio-plugin, vst3, au, shipping, qa]
---

# Plugin Release Pipeline

Use this skill when the task is getting an audio plugin from “works on my machine” to “safe to ship.”

## Release truth

A plugin is not ready because it sounds good once.
It is ready when it installs cleanly, scans cleanly, restores cleanly, and behaves in real hosts.

## Pre-release checklist

Before release, verify:
- version number updated everywhere needed
- plugin identifiers are stable
- preset/state migration still works
- scan/validation passes
- automation works
- sample-rate changes are safe
- bypass is sane
- uninstall path is understood

## Test matrix

At minimum test:
- two hosts
- common sample rates
- small and large buffers
- open -> save -> reopen session
- preset save/load
- aggressive automation on key parameters

## Packaging mindset

Think in layers:
1. build artifacts
2. plugin metadata
3. installer/package shape
4. signing/notarization where needed
5. release notes and rollback plan

## Common release failures

- changing plugin IDs after beta
- state incompatibility between versions
- validation passes in one host but not another
- installer puts files in wrong location
- missing resources/assets outside dev machine
- signing/notarization forgotten until the end

## Versioning discipline

Ship with:
- semantic or at least predictable versioning
- visible version in plugin/about/build metadata
- release notes that mention breaking preset/state risks

## Metadata sanity

Check:
- manufacturer name
- plugin code / IDs
- supported channel layouts
- plugin format exports
- version strings
- bundle names

## Final QA pass

Do one boring pass right before release:
- fresh install on a clean-ish machine if possible
- host scan
- instantiate
- play audio
- automate key params
- save/reopen project
- remove plugin
- reinstall if needed

## Output style

When helping, prefer:
- exact release blocker list
- what to verify before shipping
- what would be painful to break later
- smallest safe launch path

## Launch bias

For v1:
- ship fewer formats if needed
- keep IDs stable
- write honest release notes
- optimize for trust over breadth

The plugin can grow later.
Broken installs are forever.
