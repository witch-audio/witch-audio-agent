---
name: juce-plugin-dev
description: JUCE plugin development skill for witch.audio. Covers project structure, AudioProcessor and Editor patterns, APVTS parameter design, build pitfalls, and plugin debugging workflow.
version: 1.0.0
author: witch audio
license: MIT
metadata:
  hermes:
    tags: [juce, c++, vst3, au, aax, audio-plugin]
---

# JUCE Plugin Development

Use this skill for JUCE plugin architecture, bug fixing, scaffolding, build issues, and release prep.

## Golden rule

Keep the audio thread boring.
The editor can be fancy. The processor should be disciplined.

## Core structure

Typical split:
- `PluginProcessor.*` for DSP, parameters, state, host integration
- `PluginEditor.*` for UI only
- separate DSP classes for synth voices, filters, effects, modulators
- separate parameter layout/helper files once the plugin grows

## Processor responsibilities

The processor should own:
- bus layouts
- `prepareToPlay`
- `releaseResources`
- `processBlock`
- parameter layout
- state serialization
- DSP object lifetime

The editor should not own audio truth.
It can reflect and control state, not define the engine.

## APVTS defaults

Use `AudioProcessorValueTreeState` when you want host automation, preset recall, and a sane bridge between UI and DSP.

Good pattern:
- build all parameters in one `createParameterLayout()` function
- keep stable parameter IDs forever once released
- use normalized ranges carefully
- use attachments in the editor, not manual polling unless needed

### Common APVTS mistakes
- changing parameter IDs after shipping
- reading raw parameter pointers without smoothing where needed
- expensive tree operations in `processBlock`
- using text labels that don’t match actual units or ranges

## `prepareToPlay`

Do here:
- cache sample rate and block size
- reset DSP state
- allocate scratch buffers up front
- prepare oversampling or convolution objects
- reset smoothing ramps

Do not defer critical DSP initialization until first block if you can avoid it.

## `processBlock`

Checklist:
- clear unused output channels
- fetch parameter values once per block where possible
- smooth parameters that can click
- avoid allocation
- avoid locks
- guard denormals
- maintain predictable gain staging

## MIDI / synth notes

For synths:
- keep voice allocation logic deterministic
- decide whether note-on resets oscillator phase
- think about sustain pedal behavior early
- test voice stealing with long releases

## Editor patterns

Good UI defaults:
- one source of truth: APVTS
- use `SliderAttachment`, `ButtonAttachment`, `ComboBoxAttachment`
- throttle expensive repaints
- do not query DSP internals every frame unless needed
- separate look-and-feel styling from control logic

## Build / format targets

Common targets:
- VST3: baseline modern cross-platform target
- AU: needed on macOS logic ecosystem
- AAX: only if you truly need Pro Tools support
- Standalone: useful for debugging and demos

## Common JUCE bugs

### No audio output
Check:
- bus layout
- channel clearing
- plugin enabled / bypass path
- output gain at zero
- synth voice render path not called

### Clicks during automation
Check:
- parameter smoothing
- filter coefficient jumps
- delay-time jumps
- phase reset or envelope discontinuity

### UI works, host automation broken
Check:
- APVTS parameter IDs
- attachment wiring
- state restore functions
- host-visible parameter registration

### CPU too high
Check:
- allocations in `processBlock`
- unnecessary coefficient updates every sample
- expensive repaint timers
- oversampling scope too broad
- debug logging left in hot paths

### Plugin fails validation
Check:
- bus layout consistency
- state serialization robustness
- editor sizing assumptions
- plugin manufacturer/version metadata
- unsupported channel configurations

## Release discipline

Before shipping:
- test 44.1k / 48k / 96k
- test mono, stereo, odd host buffer sizes
- test automation of every exposed parameter
- test preset save/load
- test plugin scan in at least two hosts
- test bypass, sample-rate changes, transport start/stop

## Suggested response style

When helping with JUCE:
1. identify whether the problem is processor, editor, parameters, or build
2. point to the exact class / method to inspect
3. give the smallest safe fix
4. tell how to verify in a host

## Strong defaults for new plugin scaffolds

Reach for:
- APVTS for parameter/state management
- dedicated DSP classes outside `PluginProcessor`
- explicit smoothing objects for gain/filter cutoff/mix
- simple, inspectable signal flow before optimization

If the architecture is unclear, simplify first. Fancy later.
