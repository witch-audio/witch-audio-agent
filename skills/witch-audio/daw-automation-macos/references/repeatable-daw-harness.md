# Repeatable DAW Harness on macOS

Goal: use small, repeatable DAW templates instead of one-off UI guessing.

## Harness folders
- qa-sessions/
- bounce-outputs/
- screenshots/
- notes/

## Recommended session set
- plugin-load-test
- automation-torture-test
- silence-denormal-test
- state-recall-test
- bounce-null-test

## macOS automation posture
- bring the DAW frontmost first
- keep one known screen layout
- name tracks clearly
- save session templates in fixed locations
- verify after every major action

## Minimal repeatable run
1. open target DAW
2. open a known template session
3. confirm expected track/device slot
4. load plugin or saved chain
5. start playback
6. run one automation stress move
7. stop and bounce if needed
8. save notes and artifacts

## Avoid
- changing windows and panels mid-run
- relying on remembered cursor positions
- trying to automate a giant exploratory session

Use boring sessions.
Boring sessions catch real bugs.
