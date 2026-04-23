import asyncio
import json

import pytest


class FakeBackend:
    def health(self):
        return {"available": True, "backend": "fake", "details": "ok"}

    def get_project_info(self):
        from integrations.reaper.models import ProjectInfo

        return ProjectInfo(
            path="/tmp/test.RPP",
            name="test.RPP",
            is_dirty=False,
            sample_rate=48000.0,
            bpm=120.0,
        )

    def list_tracks(self):
        from integrations.reaper.models import TrackInfo

        return [
            TrackInfo(index=0, name="SRC drums", guid="guid-1", fx_count=0),
            TrackInfo(index=1, name="DUT main", guid="guid-2", selected=True, fx_count=1),
        ]

    def select_track_by_name(self, track_name):
        from integrations.reaper.models import TrackInfo

        return TrackInfo(index=1, name=track_name, guid="guid-2", selected=True, fx_count=1)

    def list_track_fx(self, track_name):
        from integrations.reaper.models import FXInfo

        return [FXInfo(index=0, name=f"FX on {track_name}", enabled=True)]

    def insert_fx(self, track_name, fx_name):
        from integrations.reaper.models import FXInfo

        return FXInfo(index=1, name=fx_name, enabled=True)

    def play(self):
        return {"playing": True}

    def stop(self):
        return {"playing": False}

    def save_project(self):
        return {"saved": True, "path": "/tmp/test.RPP"}

    def create_track(self, name, index=None):
        from integrations.reaper.models import TrackInfo

        return TrackInfo(index=2 if index is None else index, name=name, guid="guid-3", selected=False, fx_count=0)

    def delete_track(self, track_name):
        return {"deleted": True, "track_name": track_name}

    def set_fx_param(self, track_name, fx_name, param_index, normalized_value):
        return {
            "track_name": track_name,
            "fx_name": fx_name,
            "param_index": param_index,
            "param_name": "Wet",
            "normalized_value": normalized_value,
        }

    def add_item(self, track_name, start, end):
        from integrations.reaper.models import ItemInfo

        return ItemInfo(index=0, track_name=track_name, position=start, length=end - start, item_type="empty")

    def add_midi_item(self, track_name, start, end, quantize=False):
        from integrations.reaper.models import ItemInfo

        return ItemInfo(index=1, track_name=track_name, position=start, length=end - start, item_type="midi")

    def insert_media(self, track_name, file_path, mode=0):
        from integrations.reaper.models import ItemInfo

        return ItemInfo(index=2, track_name=track_name, position=0.0, length=1.0, item_type="media", source_path=file_path)

    def add_marker(self, position, name=""):
        from integrations.reaper.models import MarkerInfo

        return MarkerInfo(index=1, name=name, position=position)

    def add_region(self, start, end, name=""):
        from integrations.reaper.models import RegionInfo

        return RegionInfo(index=1, name=name, start=start, end=end)

    def render_project(self, action_id=None, command_id=None, output_directory=None, output_pattern=None):
        return {
            "rendered": True,
            "action_id": action_id,
            "command_id": command_id,
            "output_directory": output_directory,
            "output_pattern": output_pattern,
        }

    def run_action(self, action_id):
        return {"ok": True, "action_id": action_id}

    def run_named_action(self, command_id):
        return {"ok": True, "command_id": command_id}


@pytest.fixture
def event_loop():
    loop = asyncio.new_event_loop()
    previous = None
    try:
        previous = asyncio.get_event_loop_policy().get_event_loop()
    except RuntimeError:
        previous = None
    asyncio.set_event_loop(loop)
    yield loop
    loop.close()
    asyncio.set_event_loop(previous)


@pytest.fixture
def reaper_mcp_server():
    pytest.importorskip("mcp", reason="MCP SDK not installed")
    from integrations.reaper_mcp import create_reaper_mcp_server

    return create_reaper_mcp_server(backend=FakeBackend())


def _run_tool(server, name, args=None):
    result = asyncio.get_event_loop().run_until_complete(
        server._tool_manager.call_tool(name, args or {})
    )
    return json.loads(result) if isinstance(result, str) else result


class TestToolRegistration:
    def test_expected_tools_registered(self, reaper_mcp_server, event_loop):
        tools = reaper_mcp_server._tool_manager.list_tools()
        tool_names = {tool.name for tool in tools}

        assert tool_names == {
            "reaper_health",
            "reaper_get_project_info",
            "reaper_list_tracks",
            "reaper_select_track",
            "reaper_list_track_fx",
            "reaper_insert_fx",
            "reaper_create_track",
            "reaper_delete_track",
            "reaper_set_fx_param",
            "reaper_add_item",
            "reaper_add_midi_item",
            "reaper_insert_media",
            "reaper_add_marker",
            "reaper_add_region",
            "reaper_render_project",
            "reaper_run_action",
            "reaper_run_named_action",
            "reaper_play",
            "reaper_stop",
            "reaper_save_project",
        }

    def test_tools_have_descriptions(self, reaper_mcp_server, event_loop):
        for tool in reaper_mcp_server._tool_manager.list_tools():
            assert tool.description


class TestToolCalls:
    def test_health(self, reaper_mcp_server, event_loop):
        result = _run_tool(reaper_mcp_server, "reaper_health")

        assert result["available"] is True
        assert result["backend"] == "fake"

    def test_get_project_info(self, reaper_mcp_server, event_loop):
        result = _run_tool(reaper_mcp_server, "reaper_get_project_info")

        assert result["project"]["name"] == "test.RPP"
        assert result["project"]["sample_rate"] == 48000.0

    def test_list_tracks(self, reaper_mcp_server, event_loop):
        result = _run_tool(reaper_mcp_server, "reaper_list_tracks")

        assert result["count"] == 2
        assert result["tracks"][1]["name"] == "DUT main"

    def test_select_track(self, reaper_mcp_server, event_loop):
        result = _run_tool(
            reaper_mcp_server,
            "reaper_select_track",
            {"track_name": "DUT main"},
        )

        assert result["track"]["name"] == "DUT main"
        assert result["track"]["selected"] is True

    def test_list_track_fx(self, reaper_mcp_server, event_loop):
        result = _run_tool(
            reaper_mcp_server,
            "reaper_list_track_fx",
            {"track_name": "DUT main"},
        )

        assert result["count"] == 1
        assert result["fx"][0]["name"] == "FX on DUT main"

    def test_insert_fx(self, reaper_mcp_server, event_loop):
        result = _run_tool(
            reaper_mcp_server,
            "reaper_insert_fx",
            {"track_name": "DUT main", "fx_name": "ReaEQ"},
        )

        assert result["fx"]["name"] == "ReaEQ"

    def test_play_and_stop(self, reaper_mcp_server, event_loop):
        play = _run_tool(reaper_mcp_server, "reaper_play")
        stop = _run_tool(reaper_mcp_server, "reaper_stop")

        assert play["playing"] is True
        assert stop["playing"] is False

    def test_create_and_delete_track(self, reaper_mcp_server, event_loop):
        created = _run_tool(
            reaper_mcp_server,
            "reaper_create_track",
            {"name": "Print bus", "index": 2},
        )
        deleted = _run_tool(
            reaper_mcp_server,
            "reaper_delete_track",
            {"track_name": "Print bus"},
        )

        assert created["track"]["name"] == "Print bus"
        assert deleted["deleted"] is True

    def test_set_fx_param(self, reaper_mcp_server, event_loop):
        result = _run_tool(
            reaper_mcp_server,
            "reaper_set_fx_param",
            {"track_name": "DUT main", "fx_name": "ReaEQ", "param_index": 0, "normalized_value": 0.75},
        )

        assert result["param_name"] == "Wet"
        assert result["normalized_value"] == 0.75

    def test_add_items_and_insert_media(self, reaper_mcp_server, event_loop):
        item = _run_tool(
            reaper_mcp_server,
            "reaper_add_item",
            {"track_name": "DUT main", "start": 1.0, "end": 3.5},
        )
        midi = _run_tool(
            reaper_mcp_server,
            "reaper_add_midi_item",
            {"track_name": "DUT main", "start": 4.0, "end": 8.0, "quantize": True},
        )
        media = _run_tool(
            reaper_mcp_server,
            "reaper_insert_media",
            {"track_name": "DUT main", "file_path": "/tmp/loop.wav", "mode": 1},
        )

        assert item["item"]["item_type"] == "empty"
        assert midi["item"]["item_type"] == "midi"
        assert media["item"]["source_path"] == "/tmp/loop.wav"

    def test_markers_regions_render_and_actions(self, reaper_mcp_server, event_loop):
        marker = _run_tool(
            reaper_mcp_server,
            "reaper_add_marker",
            {"position": 12.0, "name": "Verse"},
        )
        region = _run_tool(
            reaper_mcp_server,
            "reaper_add_region",
            {"start": 16.0, "end": 24.0, "name": "Hook"},
        )
        render = _run_tool(
            reaper_mcp_server,
            "reaper_render_project",
            {"action_id": 42230, "output_directory": "/tmp/renders", "output_pattern": "$project"},
        )
        action = _run_tool(
            reaper_mcp_server,
            "reaper_run_action",
            {"action_id": 40044},
        )
        named = _run_tool(
            reaper_mcp_server,
            "reaper_run_named_action",
            {"command_id": "_SWS_TEST"},
        )

        assert marker["marker"]["name"] == "Verse"
        assert region["region"]["name"] == "Hook"
        assert render["rendered"] is True
        assert action["action_id"] == 40044
        assert named["command_id"] == "_SWS_TEST"

    def test_save_project(self, reaper_mcp_server, event_loop):
        result = _run_tool(reaper_mcp_server, "reaper_save_project")

        assert result["saved"] is True
        assert result["path"] == "/tmp/test.RPP"
