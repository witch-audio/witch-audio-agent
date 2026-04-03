---
name: stem-separation-and-tagging
description: Stem separation and audio tagging skill for witch.audio. Covers practical workflows for splitting mixes, tagging stems, organizing outputs, and validating whether the separated results are actually useful.
version: 1.0.0
author: witch audio
license: MIT
metadata:
  hermes:
    tags: [stems, separation, tagging, organization, audio-ml]
---

# Stem Separation and Tagging

Use this skill when the task involves splitting tracks into stems, labeling them, or turning a messy pile of audio into something searchable and usable.

## Core principle

Separated audio is only useful if the outputs are organized and trustworthy.

## Good workflow

1. normalize input expectations
2. separate into target stems
3. listen for bleed/artifacts
4. tag each output clearly
5. store with stable naming
6. keep provenance back to the source file

## Typical stem groups

- vocals
- drums
- bass
- harmonic / music
- FX / other

Sometimes more useful groups are task-specific.
Do not force five stems if the product only needs two.

## Tagging dimensions

Useful tags include:
- instrument/source
- confidence
- energy
- dry/wet
- clean/noisy
- mono/stereo
- role in arrangement

## Common failures

- vocal bleed left everywhere
- transients smeared in drum stem
- stem labels too vague to search later
- no confidence score or quality note
- filenames with no link back to original asset

## Output style

Prefer:
- target stems
- naming scheme
- quality checks
- what to flag for human review

A messy stem folder is not a workflow.
