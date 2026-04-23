---
name: audio-unit-testing
description: Audio unit testing skill for witch.audio. Covers deterministic DSP tests, golden files, property checks, null tests, and how to test audio code without pretending ears are optional.
version: 1.0.0
author: witch audio
license: MIT
metadata:
  hermes:
    tags: [audio-testing, unit-tests, dsp, qa, regression]
---

# Audio Unit Testing

Use this skill when writing tests for audio code, DSP blocks, plugins, or analysis pipelines.

## Core rule

Test what can be measured.
Listen to what cannot.
Do both.

## Good test types

- deterministic sample/block outputs
- range and invariants
- no-NaN / no-inf checks
- null tests
- frequency-response tolerances
- state reset behavior
- serialization / restore behavior
- golden reference files where appropriate

## Great candidates for tests

- filters
- envelopes
- modulators
- utility DSP
- file parsers/loaders
- preset/state transforms
- analysis code

## Bad test habits

- overfitting exact floats where tolerance is enough
- testing only happy paths
- ignoring extreme parameter values
- pretending a passing test means good sound

## Included workflow assets

- `scripts/wav_null_test.py`
- `templates/dsp-regression-checklist.md`

Use the script for simple WAV null tests and the checklist for repeatable regression passes.

## Output style

Prefer:
- what to test deterministically
- what needs tolerance
- what still needs listening QA
- one regression test to add next
