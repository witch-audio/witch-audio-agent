# REAPER-First MCP Control Implementation Plan

> **For Hermes:** Use subagent-driven-development skill to implement this plan task-by-task.

**Goal:** Give witch.audio a real REAPER-first control path by adding a local stdio MCP server and thin REAPER bridge that expose safe semantic DAW actions instead of raw pixel control.

**Architecture:** Build a small REAPER integration layer in Python, then expose only curated high-value actions through a FastMCP server. Use `reapy-boost` as the primary control backend when available, keep action names semantic and narrow, and leave OSC/UI fallback for later phases.

**Tech Stack:** Python, FastMCP (`mcp.server.fastmcp.FastMCP`), `reapy-boost`, Hermes native MCP client, REAPER/ReaScript, `scripts/run_tests.sh`.

---

## Scope for v1

Ship only safe, high-confidence actions:
- app / backend health
- current project info
- list tracks
- select track by exact name
- list FX on track
- insert FX by exact name
- play / stop
- save project

Do not ship in v1:
- arbitrary code execution inside REAPER
- freeform item editing
- plugin GUI automation
- destructive bulk actions
- generic “run any action id” tool

---

## Proposed files

**Create:**
- `integrations/reaper/__init__.py`
- `integrations/reaper/backend.py`
- `integrations/reaper/models.py`
- `integrations/reaper/errors.py`
- `integrations/reaper_mcp.py`
- `tests/test_reaper_backend.py`
- `tests/test_reaper_mcp.py`
- `website/docs/guides/reaper-agent-control.md`

**Modify later if needed:**
- `pyproject.toml` or dependency file that declares optional extras
- `skills/witch-audio/reaper-agent-control/SKILL.md`
- `website/docs/reference/skills-catalog.md`

---

## Design rules

1. REAPER is semantic target first, UI target second.
2. MCP tools must be narrow verbs with validation.
3. Tool names must be stable and obvious.
4. Backend logic must be testable without live REAPER.
5. Live REAPER integration tests can come later; unit tests first.
6. If `reapy-boost` missing or REAPER unavailable, return clear structured errors.

---

## MCP tool surface for v1

Expose these MCP tools only:
- `reaper_health`
- `reaper_get_project_info`
- `reaper_list_tracks`
- `reaper_select_track`
- `reaper_list_track_fx`
- `reaper_insert_fx`
- `reaper_play`
- `reaper_stop`
- `reaper_save_project`

Each tool should:
- validate inputs
- return structured JSON-ish dicts
- include exact project / track / fx context in errors

---

## Task 1: Create REAPER data models and error types

**Objective:** Create a tiny typed core so the backend and MCP layer share one vocabulary.

**Files:**
- Create: `integrations/reaper/models.py`
- Create: `integrations/reaper/errors.py`
- Create: `integrations/reaper/__init__.py`
- Test: `tests/test_reaper_backend.py`

**Step 1: Write failing tests for the shared types**

Add tests for:
- `TrackInfo` shape
- `ProjectInfo` shape
- `FXInfo` shape
- custom exceptions like `ReaperUnavailableError`, `TrackNotFoundError`, `FXInsertError`

**Step 2: Run test to verify failure**

Run:
`source venv/bin/activate && scripts/run_tests.sh tests/test_reaper_backend.py -v`

Expected:
- fail because module/files do not exist yet

**Step 3: Write minimal models/errors**

Implement small dataclasses or typed containers only.
No backend logic yet.

Suggested fields:
- `ProjectInfo(path, name, is_dirty, sample_rate, bpm)`
- `TrackInfo(index, name, guid, selected, muted, solo, armed, fx_count)`
- `FXInfo(index, name, enabled)`

**Step 4: Run test to verify pass**

Run:
`source venv/bin/activate && scripts/run_tests.sh tests/test_reaper_backend.py -v`

Expected:
- tests for basic shapes pass

**Step 5: Commit**

`git add integrations/reaper models/errors tests && git commit -m "feat: add reaper integration models"`

---

## Task 2: Build backend interface with no live REAPER dependency in tests

**Objective:** Create a backend class with an injectable adapter so most logic can be unit-tested.

**Files:**
- Create: `integrations/reaper/backend.py`
- Modify: `integrations/reaper/__init__.py`
- Test: `tests/test_reaper_backend.py`

**Step 1: Write failing tests for backend interface**

Add tests for methods:
- `health()`
- `get_project_info()`
- `list_tracks()`
- `select_track_by_name(name)`
- `list_track_fx(track_name)`
- `insert_fx(track_name, fx_name)`
- `play()`
- `stop()`
- `save_project()`

Mock the adapter layer.
Do not require live REAPER.

**Step 2: Run tests to verify failure**

Run:
`source venv/bin/activate && scripts/run_tests.sh tests/test_reaper_backend.py -v`

Expected:
- fail because backend methods are missing

**Step 3: Implement backend skeleton**

Recommended structure:
- `ReaperBackend` class
- private `_adapter` field
- adapter methods wrapped with friendly exceptions
- exact-name matching for track selection in v1

**Step 4: Run tests to verify pass**

Run same command.

**Step 5: Commit**

`git add integrations/reaper/backend.py tests/test_reaper_backend.py && git commit -m "feat: add reaper backend interface"`

---

## Task 3: Add real `reapy-boost` adapter path

**Objective:** Connect the backend to real REAPER through `reapy-boost`, while keeping failure mode clean when dependency or app is absent.

**Files:**
- Modify: `integrations/reaper/backend.py`
- Modify: dependency declaration file (`pyproject.toml` if present)
- Test: `tests/test_reaper_backend.py`

**Step 1: Inspect current dependency declaration**

Find where repo declares optional/runtime Python deps.
Use the real project file before editing.

**Step 2: Write failing tests for import/failure handling**

Add tests for:
- backend reports unavailable when `reapy` import fails
- backend wraps connection failure in `ReaperUnavailableError`

**Step 3: Implement adapter**

Adapter should:
- import `reapy` lazily
- avoid import-time hard failure for all Hermes users
- keep connection logic inside methods or adapter init
- translate raw exceptions into repo-local exceptions

**Step 4: Run tests**

Run:
`source venv/bin/activate && scripts/run_tests.sh tests/test_reaper_backend.py -v`

Expected:
- unit tests pass without requiring REAPER process

**Step 5: Commit**

`git add integrations/reaper/backend.py tests/test_reaper_backend.py pyproject.toml && git commit -m "feat: add reapy-backed reaper adapter"`

---

## Task 4: Create stdio MCP server for REAPER

**Objective:** Expose curated backend methods as MCP tools using the same FastMCP pattern Hermes already uses in `mcp_serve.py`.

**Files:**
- Create: `integrations/reaper_mcp.py`
- Test: `tests/test_reaper_mcp.py`

**Step 1: Write failing tests for MCP tool registration**

Add tests that assert the server exposes exactly these tool names:
- `reaper_health`
- `reaper_get_project_info`
- `reaper_list_tracks`
- `reaper_select_track`
- `reaper_list_track_fx`
- `reaper_insert_fx`
- `reaper_play`
- `reaper_stop`
- `reaper_save_project`

Mock backend methods.

**Step 2: Run test to verify failure**

Run:
`source venv/bin/activate && scripts/run_tests.sh tests/test_reaper_mcp.py -v`

Expected:
- fail because server file does not exist yet

**Step 3: Implement FastMCP server**

Pattern reference:
- `mcp_serve.py`

Implementation rules:
- one backend instance
- one tool per semantic action
- explicit typed parameters
- never expose arbitrary script execution
- return small structured payloads

**Step 4: Run tests to verify pass**

Run same command.

**Step 5: Commit**

`git add integrations/reaper_mcp.py tests/test_reaper_mcp.py && git commit -m "feat: add reaper mcp server"`

---

## Task 5: Add a local manual launch recipe and Hermes config example

**Objective:** Make the first usable path obvious for a developer machine.

**Files:**
- Create: `website/docs/guides/reaper-agent-control.md`
- Modify: `skills/witch-audio/reaper-agent-control/SKILL.md`

**Step 1: Document manual server launch**

Include example:

```yaml
mcp_servers:
  reaper:
    command: "python"
    args: ["/absolute/path/to/repo/integrations/reaper_mcp.py"]
    timeout: 30
    connect_timeout: 15
```

If repo prefers `uv run` or `python -m`, document that instead after inspection.

**Step 2: Document prerequisites**

Include:
- REAPER installed and running
- `reapy-boost` installed
- REAPER scripting access configured if needed
- tiny known test project ready

**Step 3: Document first prompts**

Examples:
- “List REAPER tracks in current project.”
- “Insert ReaEQ on track DUT main.”
- “Play for a smoke check, then stop.”

**Step 4: Update skill**

Add concrete MCP launch/config section to `skills/witch-audio/reaper-agent-control/SKILL.md`.

**Step 5: Commit**

`git add website/docs/guides/reaper-agent-control.md skills/witch-audio/reaper-agent-control/SKILL.md && git commit -m "docs: add reaper agent control guide"`

---

## Task 6: Add negative-case tests and safety guards

**Objective:** Prove the server fails safely and predictably.

**Files:**
- Modify: `tests/test_reaper_backend.py`
- Modify: `tests/test_reaper_mcp.py`

**Step 1: Add failing tests for negative cases**

Cover:
- REAPER unavailable
- unknown track name
- FX insertion failure
- empty project path on save edge case
- duplicate track names in v1 returns clear error or first-match policy explicitly

**Step 2: Run tests to verify failure**

Run:
`source venv/bin/activate && scripts/run_tests.sh tests/test_reaper_backend.py tests/test_reaper_mcp.py -v`

**Step 3: Implement minimal fixes**

Prefer explicit errors over silent fallback.

**Step 4: Run tests to verify pass**

Use same command.

**Step 5: Commit**

`git add tests/test_reaper_backend.py tests/test_reaper_mcp.py integrations/reaper && git commit -m "test: harden reaper mcp safety cases"`

---

## Task 7: Add one end-to-end smoke path with mocks

**Objective:** Prove the end-user workflow shape without requiring live REAPER in CI.

**Files:**
- Modify: `tests/test_reaper_mcp.py`

**Step 1: Write failing smoke test**

Flow:
1. `reaper_health`
2. `reaper_list_tracks`
3. `reaper_insert_fx(track_name="DUT main", fx_name="ReaEQ")`
4. `reaper_play`
5. `reaper_stop`

Mock backend responses.
Assert payload shapes stay stable.

**Step 2: Run tests**

Run:
`source venv/bin/activate && scripts/run_tests.sh tests/test_reaper_mcp.py -v`

**Step 3: Fix payload mismatches**

Keep response keys simple and stable.

**Step 4: Run tests to verify pass**

Same command.

**Step 5: Commit**

`git add tests/test_reaper_mcp.py integrations/reaper_mcp.py && git commit -m "test: add reaper mcp smoke flow"`

---

## Task 8: Manual verification on real machine

**Objective:** Prove the stack works against local REAPER and a tiny harness project.

**Files:**
- No code required unless bug found

**Step 1: Start REAPER with a tiny harness project**

Use one of the dedicated harness projects.
Prefer exact known track names.

**Step 2: Start MCP server manually**

Example:
`source venv/bin/activate && python integrations/reaper_mcp.py`

Use real launch command once implementation picks final entrypoint.

**Step 3: Connect Hermes to local MCP server**

Add local `mcp_servers.reaper` config in `~/.hermes/config.yaml`.

**Step 4: Run real prompts**

Test prompts:
- “Tell me whether REAPER backend is healthy.”
- “List tracks in current project.”
- “Select track DUT main.”
- “Insert ReaEQ on DUT main.”
- “Play, then stop.”

**Step 5: Log bugs found**

If any live issue appears, create follow-up tasks before expanding scope.

---

## Verification checklist

Implementation done when all true:
- unit tests pass with `scripts/run_tests.sh`
- MCP server starts locally
- Hermes can discover REAPER tools through MCP
- current project and track listing work on a real session
- exact-name track selection works
- one plugin insert works on a known track
- play/stop works
- docs and skill explain setup clearly

---

## Nice next steps after v1

Do later, not now:
- `reaper_set_fx_param`
- `reaper_render_project`
- marker / region tools
- OSC realtime bridge
- js_ReaScriptAPI fallback for dialog handling
- Ableton and Logic adapters using same semantic tool philosophy

---

## Notes for implementation

- Follow `mcp_serve.py` for FastMCP server style.
- Keep REAPER integration isolated from Hermes core so non-audio users do not pay complexity tax.
- Prefer optional dependency loading.
- Keep tool payloads small enough for agent use.
- No arbitrary command execution through MCP.
