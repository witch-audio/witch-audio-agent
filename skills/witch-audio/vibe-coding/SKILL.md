---
name: vibe-coding
description: Vibe-coding skill for witch.audio. Helps turn instincts into shippable app ideas, tight prompts, practical scaffolds, and small launchable tools fast.
version: 1.0.0
author: witch audio
license: MIT
metadata:
  hermes:
    tags: [vibe-coding, prototyping, app-ideas, shipping, ai-tools]
---

# Vibe Coding

Use this skill when the goal is to go from loose instinct to a shippable tool quickly.

## Core belief

Volume is a strategy.
Tiny tools count.
A weird useful thing shipped today beats a perfect thing imagined all week.

## Good vibe-coded products

Best early targets are:
- single painful workflow fixers
- generators with one magical output
- analysis tools with one crisp verdict
- small media toys with a share loop
- niche utilities for a specific subculture

## Bad early targets

Avoid for v1 unless conviction is extreme:
- giant multi-role SaaS dashboards
- marketplaces before supply exists
- deep collaborative systems
- complex auth/billing/admin all at once

## Idea filter

A strong idea usually has:
- one user archetype
- one painful or funny problem
- one sentence of value
- one fast input
- one satisfying output

If it needs a paragraph to explain, compress it.

## Product framing template

Define:
- who it is for
- what tiny pain it removes
- what input they give
- what output they get
- why they would share or come back

## Prompting an AI coder

A good prompt includes:
- exact product goal
- target stack
- first screen / user flow
- constraints for v1
- visual tone
- deploy target

### Minimal scaffold prompt

Build a tiny v1 app called [name].
It is for [user].
It solves [single problem].
User inputs [x].
The app outputs [y].
Use [stack].
Keep it to one page for v1.
No auth unless absolutely necessary.
Make the UI feel [tone].
Ship the smallest working version first.

## Shipping checklist

Before calling it shipped:
- landing page title is clear
- core action works end to end
- empty states are not broken
- mobile is not embarrassing
- one screenshot or demo is easy to make
- domain/deploy path is obvious

## Practical stacks

Reach for:
- Next.js or static web app for distribution-first tools
- Web Audio API for browser audio toys
- JUCE only when native plugin value is real
- simple local JSON / sqlite / Supabase before overbuilding infra

## witch.audio angle

Bias toward tools that combine:
- code
- sound
- taste
- distribution

Examples:
- synth preset describer
- plugin bug reproducer
- stem mood tagger
- audio effect idea generator
- Suno/Udio prompt remixer
- waveform-to-copywriting toy

## Response style

When asked for ideas, prefer:
- title
- what it does
- why it spreads or sells
- shortest build prompt

When asked to choose between ideas, prefer:
- fastest to ship
- clearest user outcome
- strongest distribution hook

Make it concrete. Make it launchable. Then make another.
