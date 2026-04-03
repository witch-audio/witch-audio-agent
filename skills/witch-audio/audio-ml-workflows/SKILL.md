---
name: audio-ml-workflows
description: Audio ML workflow skill for witch.audio. Covers practical pipelines for tagging, separation, transcription, embedding, generation, and evaluation of audio models and tools.
version: 1.0.0
author: witch audio
license: MIT
metadata:
  hermes:
    tags: [audio-ml, embeddings, transcription, separation, tagging, evaluation]
---

# Audio ML Workflows

Use this skill when building or evaluating AI systems that touch audio.

## Useful pipeline types

- transcription
- tagging / classification
- source separation
- similarity / embeddings
- generation
- restoration / enhancement
- retrieval

## Good workflow

1. define the audio task clearly
2. define input/output shape
3. choose evaluation before overbuilding
4. build the smallest repeatable pipeline
5. test with ugly real-world data, not only perfect clips

## Common mistakes

- ignoring sample rate / channel / duration normalization
- mixing training and evaluation distributions carelessly
- no human listening pass
- measuring only one metric
- forgetting latency/runtime constraints for product use

## Evaluation ideas

Depending on task, use:
- WER / CER for speech
- precision/recall/F1 for tags
- SDR-like separation metrics
- retrieval hit rate / ranking metrics
- human listening panels
- runtime / memory / latency budgets

## Product reality

For audio ML products, the winning system is often not the fanciest model.
It is the one with:
- good preprocessing
- predictable outputs
- decent latency
- clear failure modes
- useful UX around the model

## Output style

Prefer:
- task framing
- pipeline outline
- data normalization needs
- evaluation plan
- deployment constraint
