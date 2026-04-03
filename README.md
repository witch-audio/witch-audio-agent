# witch.audio

> the future is agentic. might as well make it fun.

An open-source AI agent at the intersection of code and sound. Forked from [Hermes Agent](https://github.com/NousResearch/hermes-agent) by Nous Research — same engine, different soul.

[![License: MIT](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

---

## What it is

witch.audio is the only agent that speaks both code and sound fluently.

She knows DSP, JUCE, the Web Audio API, synthesis, AI music tools, and vibe coding. She runs anywhere — CLI, Telegram, Discord, a $5 VPS. She remembers things. She improves over time.

Under the hood: persistent cross-session memory, self-improving skills, 40+ tools, multi-platform messaging, cron scheduling. That's all Hermes. The personality, domain depth, and audio superpowers are witch.audio.

---

## Quick start

```bash
# clone
git clone https://github.com/witch-audio/witch-audio-agent
cd witch-audio-agent

# install
python3 -m pip install -e ".[cli]"

# authenticate with OpenAI Codex (opens browser, one-time)
witch auth add openai-codex

# run
witch
```

First launch auto-loads `witch-audio-identity`, so the soul is there by default.

The default CLI skin is also `witch` — dark blue, custom ASCII, midnight theme.

### Smoke test

```bash
witch -q "Say hi in one line and tell me what you know best."
```

---

## Who it's for

- Audio developers working with JUCE, Web Audio API, or DSP code
- Plugin companies that want an agent who already understands their domain
- Vibe coders shipping fast with AI tools
- Music AI enthusiasts building with Suno, Udio, or custom models
- Anyone who wants an agent that doesn't say "certainly!"

---

## Skill packs

Skills are markdown files that give the agent deep knowledge and reusable procedures.

**Core (included)**

| Skill | What it does |
|---|---|
| `witch-audio-identity` | Her soul. Loads first in every session. |
| `audio-dsp` | Filters, oscillators, effects, signal flow, debugging |
| `juce-plugin-dev` | JUCE project structure, AudioProcessor, APVTS, formats |
| `web-audio-api` | AudioContext, worklets, routing, browser patterns |
| `synthesis-recipes` | Feeling → synthesis recipe translator |
| `vibe-coding` | Fast ideation and shipping with AI tools |
| `suno-udio-prompting` | Prompt engineering for AI music tools |
| `plugin-qa` | Automated QA checklist for audio plugins |
| `realtime-audio-cpp` | Audio-thread safety, lock-free patterns, performance |
| `faust-dsp` | DSP prototyping and export workflows with FAUST |
| `audio-analysis-measurement` | Spectrograms, loudness, phase, null tests, measurement |
| `plugin-release-pipeline` | Pre-release checks, packaging, metadata, shipping |
| `audio-ui-ux` | Better controls, meters, parameter naming, plugin UX |
| `max-msp-gen` | Max patching and gen~ production flow |
| `rnbo` | Portable patch/export workflows from Max into products |
| `rust-audio` | Realtime-safe Rust audio architecture and tooling |
| `spatial-audio` | Width, depth, localization, mono-safe spatial design |
| `daw-plugin-qa` | Real DAW sessions as test harnesses for plugins |
| `daw-music-production` | Music-making, arranging, and production help in DAWs |
| `daw-automation-macos` | Mac DAW automation workflows for QA and music tasks |
| `plugin-preset-design` | Preset bank design, naming, coverage, and product thinking |
| `mixing-mastering-assistant` | Mix translation, mastering discipline, finishing moves |
| `audio-ml-workflows` | Practical AI pipelines for transcription, tagging, separation |
| `stem-separation-and-tagging` | Stem splitting, labeling, organization, quality checks |
| `supercollider` | Synthesis, patterns, and live-coded instrument workflows |
| `audio-unit-testing` | Deterministic DSP testing, null tests, regressions |
| `sample-library-tools` | Sample cleanup, naming, tagging, previews, organization |
| `field-recording-workflows` | Capture, annotate, clean, archive, and reuse field recordings |
| `podcast-and-voice-tooling` | Spoken-word cleanup, segmentation, transcript-aware workflows |
| `ableton-live-workflows` | Ableton-specific plugin QA and production workflows |
| `logic-pro-workflows` | Logic-specific AU QA, recall, and production workflows |
| `reaper-workflows` | REAPER-specific routing, render, and plugin test workflows |

---

## Model

Default: OpenAI Codex (`gpt-5.4`) via OAuth. No API key needed — authenticate once with `witch auth add openai-codex`.

Fallback: Anthropic Claude, OpenRouter (200+ models), or anything else Hermes supports.

Switch models with `witch model`.

---

## Platforms

Run witch.audio anywhere Hermes runs:

- Terminal (interactive TUI)
- Telegram
- Discord
- Slack
- WhatsApp / Signal
- Docker / VPS / Modal

---

## Contributing

Skills, bug fixes, and domain knowledge welcome.

The skills system is the easiest entry point — write a `.md` file, open a PR.

---

## License

MIT. Fork it. Ship it. Make it yours.

---

_witch.audio is a fork of [Hermes Agent](https://github.com/NousResearch/hermes-agent) by Nous Research. The engine is theirs. The soul is ours._
