# REAPER Plugin Harness Checklist

Project file:
Plugin under test:
Format:
Version:
Date:

## Harness setup
- [ ] one track named TEST_SOURCE
- [ ] one FX slot reserved for plugin under test
- [ ] one rendered output folder beside the project
- [ ] sample rate noted
- [ ] buffer size noted

## Passes
- [ ] load / instantiate
- [ ] playback with silence
- [ ] playback with drum/transient loop
- [ ] automate key parameter hard
- [ ] bypass toggle during playback
- [ ] save / close / reopen / verify recall
- [ ] render output for comparison

## Notes
Expected:
Actual:
Likely subsystem:
