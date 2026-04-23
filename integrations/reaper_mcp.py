from __future__ import annotations

import json
import sys
from dataclasses import asdict, is_dataclass
from typing import Any, Optional

from integrations.reaper import ReaperBackend

_MCP_SERVER_AVAILABLE = False
try:
    from mcp.server.fastmcp import FastMCP

    _MCP_SERVER_AVAILABLE = True
except ImportError:
    FastMCP = None  # type: ignore[assignment]


def create_reaper_mcp_server(backend: Optional[ReaperBackend] = None) -> "FastMCP":
    if not _MCP_SERVER_AVAILABLE:
        raise ImportError(
            "REAPER MCP server requires the 'mcp' package. "
            f"Install with: {sys.executable} -m pip install 'mcp'"
        )

    active_backend = backend or ReaperBackend()
    mcp = FastMCP(
        "reaper",
        instructions=(
            "REAPER control bridge for witch.audio. Use these tools for narrow, "
            "semantic DAW control against the current REAPER session."
        ),
    )

    @mcp.tool()
    def reaper_health() -> str:
        """Check whether the REAPER backend is available and connected."""
        return _dump(active_backend.health())

    @mcp.tool()
    def reaper_get_project_info() -> str:
        """Return info about the current REAPER project."""
        return _dump({"project": active_backend.get_project_info()})

    @mcp.tool()
    def reaper_list_tracks() -> str:
        """List tracks in the current REAPER project."""
        tracks = active_backend.list_tracks()
        return _dump({"count": len(tracks), "tracks": tracks})

    @mcp.tool()
    def reaper_select_track(track_name: str) -> str:
        """Select one REAPER track by exact name."""
        return _dump({"track": active_backend.select_track_by_name(track_name)})

    @mcp.tool()
    def reaper_list_track_fx(track_name: str) -> str:
        """List FX on one REAPER track by exact name."""
        fx = active_backend.list_track_fx(track_name)
        return _dump({"track_name": track_name, "count": len(fx), "fx": fx})

    @mcp.tool()
    def reaper_insert_fx(track_name: str, fx_name: str) -> str:
        """Insert one FX on one REAPER track by exact name."""
        return _dump({"track_name": track_name, "fx": active_backend.insert_fx(track_name, fx_name)})

    @mcp.tool()
    def reaper_create_track(name: str, index: Optional[int] = None) -> str:
        """Create one REAPER track, optionally at a specific index."""
        return _dump({"track": active_backend.create_track(name, index=index)})

    @mcp.tool()
    def reaper_delete_track(track_name: str) -> str:
        """Delete one REAPER track by exact name."""
        return _dump(active_backend.delete_track(track_name))

    @mcp.tool()
    def reaper_set_fx_param(track_name: str, fx_name: str, param_index: int, normalized_value: float) -> str:
        """Set one FX parameter by track name, FX name, param index, and normalized value."""
        return _dump(active_backend.set_fx_param(track_name, fx_name, param_index, normalized_value))

    @mcp.tool()
    def reaper_add_item(track_name: str, start: float, end: float) -> str:
        """Add one empty media item to one REAPER track."""
        return _dump({"item": active_backend.add_item(track_name, start, end)})

    @mcp.tool()
    def reaper_add_midi_item(track_name: str, start: float, end: float, quantize: bool = False) -> str:
        """Add one empty MIDI item to one REAPER track."""
        return _dump({"item": active_backend.add_midi_item(track_name, start, end, quantize=quantize)})

    @mcp.tool()
    def reaper_insert_media(track_name: str, file_path: str, mode: int = 0) -> str:
        """Insert one media file onto one REAPER track."""
        return _dump({"item": active_backend.insert_media(track_name, file_path, mode=mode)})

    @mcp.tool()
    def reaper_add_marker(position: float, name: str = "") -> str:
        """Add one REAPER marker at a given position."""
        return _dump({"marker": active_backend.add_marker(position, name=name)})

    @mcp.tool()
    def reaper_add_region(start: float, end: float, name: str = "") -> str:
        """Add one REAPER region from start to end."""
        return _dump({"region": active_backend.add_region(start, end, name=name)})

    @mcp.tool()
    def reaper_render_project(
        action_id: Optional[int] = None,
        command_id: Optional[str] = None,
        output_directory: Optional[str] = None,
        output_pattern: Optional[str] = None,
    ) -> str:
        """Run one REAPER render action, optionally overriding output directory and pattern."""
        return _dump(
            active_backend.render_project(
                action_id=action_id,
                command_id=command_id,
                output_directory=output_directory,
                output_pattern=output_pattern,
            )
        )

    @mcp.tool()
    def reaper_run_action(action_id: int) -> str:
        """Run one REAPER action by numeric action ID."""
        return _dump(active_backend.run_action(action_id))

    @mcp.tool()
    def reaper_run_named_action(command_id: str) -> str:
        """Run one REAPER named command, custom action, or extension action."""
        return _dump(active_backend.run_named_action(command_id))

    @mcp.tool()
    def reaper_play() -> str:
        """Start REAPER transport."""
        return _dump(active_backend.play())

    @mcp.tool()
    def reaper_stop() -> str:
        """Stop REAPER transport."""
        return _dump(active_backend.stop())

    @mcp.tool()
    def reaper_save_project() -> str:
        """Save the current REAPER project."""
        return _dump(active_backend.save_project())

    return mcp


def run_reaper_mcp_server() -> None:
    server = create_reaper_mcp_server()
    server.run()


def _serialize(value: Any) -> Any:
    if is_dataclass(value):
        return asdict(value)
    if isinstance(value, list):
        return [_serialize(item) for item in value]
    if isinstance(value, dict):
        return {key: _serialize(val) for key, val in value.items()}
    return value


def _dump(payload: Any) -> str:
    return json.dumps(_serialize(payload), indent=2)


if __name__ == "__main__":
    run_reaper_mcp_server()
