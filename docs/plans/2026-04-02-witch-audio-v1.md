# witch.audio V1 Implementation Plan

> For Hermes: implement this as a soul fork, not a deep engine fork. Keep upstream merge friction low.

Goal: ship a working witch.audio fork that feels distinct on first launch while preserving Hermes engine compatibility.

Architecture: keep internal Hermes modules largely intact, expose `witch` as the public CLI, preload witch.audio identity via startup skills, and add domain skill packs for audio programming and vibe coding. Favor additive changes over internal renames so upstream updates stay easy.

Tech stack: Python, setuptools, Hermes CLI/runtime, markdown skills, pytest.

---

## Phase 1: Packaging and startup identity

1. Fix packaging metadata in `pyproject.toml` so the project installs cleanly.
2. Make default CLI/runtime config point to `gpt-5.4` via `openai-codex`.
3. Add default startup skill config so `witch-audio-identity` loads automatically.
4. Keep internal Hermes module names where practical; prefer public rebrand over deep source rename.

## Phase 2: Core witch.audio skill pack

1. Keep `skills/witch-audio/witch-audio-identity/SKILL.md` as the soul file.
2. Add core v1 domain skills:
   - `audio-dsp`
   - `juce-plugin-dev`
   - `web-audio-api`
   - `synthesis-recipes`
   - `vibe-coding`
3. Make each skill practical: heuristics, workflows, common bugs, and copy-ready patterns.

## Phase 3: Docs and positioning

1. Keep README focused on who witch.audio is for.
2. Explain that witch.audio is Hermes engine + audio soul.
3. Document quick start around `witch auth add openai-codex` and `witch`.

## Phase 4: Verification

1. Add regression tests for project metadata and startup skill defaults.
2. Run targeted pytest for metadata/config tests.
3. Smoke test local install path after packaging fixes.

## Notes

- Avoid a full internal rename from `hermes_*` to `witch_*` in v1.
- Prefer compatibility, personality, and domain depth first.
- Web app, plugin integrations, and public distribution can land after the local CLI feels undeniable.
