# DAW Plugin QA Session Checklist

Host:
Plugin format:
Plugin version:
OS / CPU:
Sample rate:
Buffer size:
Session file:

## Pass 1 — Scan / Load
- [ ] Plugin scans successfully
- [ ] Plugin instantiates
- [ ] UI opens correctly
- [ ] Bypass works

## Pass 2 — Playback
- [ ] Silence test
- [ ] Drum/transient loop test
- [ ] Dense mix test
- [ ] CPU is stable

## Pass 3 — Automation
- [ ] Automate primary tone control
- [ ] Automate mix/output
- [ ] Bypass toggle during audio
- [ ] No obvious clicks/pops beyond expected behavior

## Pass 4 — State Recall
- [ ] Save session
- [ ] Close host
- [ ] Reopen host/session
- [ ] State and sound match expected result

## Pass 5 — Stress
- [ ] Duplicate instances
- [ ] Change sample rate
- [ ] Change buffer size
- [ ] Extreme parameter sweep

## Notes
Expected:
Actual:
Likely subsystem:
