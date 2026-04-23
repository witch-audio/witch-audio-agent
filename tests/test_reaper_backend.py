import pytest


class FakeAdapter:
    def __init__(self):
        self.selected_track = None
        self.inserted_fx = []
        self.playing = False
        self.saved = False
        self.created_tracks = []
        self.deleted_tracks = []
        self.fx_param_sets = []
        self.added_items = []
        self.added_midi_items = []
        self.inserted_media = []
        self.markers = []
        self.regions = []
        self.renders = []
        self.actions = []
        self.named_actions = []

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
            TrackInfo(index=1, name="DUT main", guid="guid-2", fx_count=1),
        ]

    def select_track_by_name(self, name):
        self.selected_track = name
        from integrations.reaper.models import TrackInfo

        return TrackInfo(index=1, name=name, guid="guid-2", selected=True, fx_count=1)

    def list_track_fx(self, track_name):
        from integrations.reaper.models import FXInfo

        return [FXInfo(index=0, name=f"FX on {track_name}", enabled=True)]

    def insert_fx(self, track_name, fx_name):
        self.inserted_fx.append((track_name, fx_name))
        from integrations.reaper.models import FXInfo

        return FXInfo(index=1, name=fx_name, enabled=True)

    def play(self):
        self.playing = True
        return {"playing": True}

    def stop(self):
        self.playing = False
        return {"playing": False}

    def save_project(self):
        self.saved = True
        return {"saved": True, "path": "/tmp/test.RPP"}

    def create_track(self, name, index=None):
        self.created_tracks.append((name, index))
        from integrations.reaper.models import TrackInfo

        return TrackInfo(index=2 if index is None else index, name=name, guid="guid-3", selected=False, fx_count=0)

    def delete_track(self, track_name):
        self.deleted_tracks.append(track_name)
        return {"deleted": True, "track_name": track_name}

    def set_fx_param(self, track_name, fx_name, param_index, normalized_value):
        self.fx_param_sets.append((track_name, fx_name, param_index, normalized_value))
        return {
            "track_name": track_name,
            "fx_name": fx_name,
            "param_index": param_index,
            "param_name": "Wet",
            "normalized_value": normalized_value,
        }

    def add_item(self, track_name, start, end):
        self.added_items.append((track_name, start, end))
        from integrations.reaper.models import ItemInfo

        return ItemInfo(index=0, track_name=track_name, position=start, length=end - start, item_type="empty")

    def add_midi_item(self, track_name, start, end, quantize=False):
        self.added_midi_items.append((track_name, start, end, quantize))
        from integrations.reaper.models import ItemInfo

        return ItemInfo(index=1, track_name=track_name, position=start, length=end - start, item_type="midi")

    def insert_media(self, track_name, file_path, mode=0):
        self.inserted_media.append((track_name, file_path, mode))
        from integrations.reaper.models import ItemInfo

        return ItemInfo(index=2, track_name=track_name, position=0.0, length=1.0, item_type="media", source_path=file_path)

    def add_marker(self, position, name=""):
        self.markers.append((position, name))
        from integrations.reaper.models import MarkerInfo

        return MarkerInfo(index=1, name=name, position=position)

    def add_region(self, start, end, name=""):
        self.regions.append((start, end, name))
        from integrations.reaper.models import RegionInfo

        return RegionInfo(index=1, name=name, start=start, end=end)

    def render_project(self, action_id=None, command_id=None, output_directory=None, output_pattern=None):
        payload = {
            "action_id": action_id,
            "command_id": command_id,
            "output_directory": output_directory,
            "output_pattern": output_pattern,
        }
        self.renders.append(payload)
        return {"rendered": True, **payload}

    def run_action(self, action_id):
        self.actions.append(action_id)
        return {"ok": True, "action_id": action_id}

    def run_named_action(self, command_id):
        self.named_actions.append(command_id)
        return {"ok": True, "command_id": command_id}


class FailingAdapter:
    def health(self):
        raise RuntimeError("boom")


class TestReaperModels:
    def test_project_info_shape(self):
        from integrations.reaper.models import ProjectInfo

        info = ProjectInfo(
            path="/tmp/test.RPP",
            name="test.RPP",
            is_dirty=True,
            sample_rate=44100.0,
            bpm=128.0,
        )

        assert info.path.endswith("test.RPP")
        assert info.is_dirty is True
        assert info.sample_rate == 44100.0
        assert info.bpm == 128.0

    def test_track_info_shape(self):
        from integrations.reaper.models import TrackInfo

        track = TrackInfo(index=2, name="DUT main", guid="abc", selected=True, fx_count=3)

        assert track.index == 2
        assert track.name == "DUT main"
        assert track.selected is True
        assert track.fx_count == 3

    def test_fx_info_shape(self):
        from integrations.reaper.models import FXInfo

        fx = FXInfo(index=0, name="ReaEQ", enabled=True)

        assert fx.name == "ReaEQ"
        assert fx.enabled is True

    def test_item_info_shape(self):
        from integrations.reaper.models import ItemInfo

        item = ItemInfo(index=3, track_name="DUT main", position=1.5, length=2.0, item_type="media", source_path="/tmp/loop.wav")

        assert item.index == 3
        assert item.track_name == "DUT main"
        assert item.position == 1.5
        assert item.length == 2.0
        assert item.item_type == "media"
        assert item.source_path == "/tmp/loop.wav"

    def test_marker_and_region_shapes(self):
        from integrations.reaper.models import MarkerInfo, RegionInfo

        marker = MarkerInfo(index=1, name="Verse", position=8.0)
        region = RegionInfo(index=2, name="Hook", start=16.0, end=24.0)

        assert marker.name == "Verse"
        assert marker.position == 8.0
        assert region.name == "Hook"
        assert region.start == 16.0
        assert region.end == 24.0

    def test_error_types(self):
        from integrations.reaper.errors import FXInsertError, ReaperUnavailableError, TrackNotFoundError

        assert str(ReaperUnavailableError("offline")) == "offline"
        assert str(TrackNotFoundError("missing")) == "missing"
        assert str(FXInsertError("bad fx")) == "bad fx"


class TestReaperBackend:
    def test_health_uses_adapter(self):
        from integrations.reaper.backend import ReaperBackend

        backend = ReaperBackend(adapter=FakeAdapter())

        result = backend.health()

        assert result["available"] is True
        assert result["backend"] == "fake"

    def test_health_wraps_failures(self):
        from integrations.reaper.backend import ReaperBackend

        backend = ReaperBackend(adapter=FailingAdapter())

        result = backend.health()

        assert result["available"] is False
        assert "boom" in result["details"]

    def test_get_project_info(self):
        from integrations.reaper.backend import ReaperBackend

        backend = ReaperBackend(adapter=FakeAdapter())

        info = backend.get_project_info()

        assert info.name == "test.RPP"
        assert info.sample_rate == 48000.0

    def test_list_tracks(self):
        from integrations.reaper.backend import ReaperBackend

        backend = ReaperBackend(adapter=FakeAdapter())

        tracks = backend.list_tracks()

        assert [t.name for t in tracks] == ["SRC drums", "DUT main"]

    def test_select_track_by_name(self):
        from integrations.reaper.backend import ReaperBackend

        adapter = FakeAdapter()
        backend = ReaperBackend(adapter=adapter)

        track = backend.select_track_by_name("DUT main")

        assert adapter.selected_track == "DUT main"
        assert track.selected is True

    def test_list_track_fx(self):
        from integrations.reaper.backend import ReaperBackend

        backend = ReaperBackend(adapter=FakeAdapter())

        fx = backend.list_track_fx("DUT main")

        assert fx[0].name == "FX on DUT main"

    def test_insert_fx(self):
        from integrations.reaper.backend import ReaperBackend

        adapter = FakeAdapter()
        backend = ReaperBackend(adapter=adapter)

        fx = backend.insert_fx("DUT main", "ReaEQ")

        assert adapter.inserted_fx == [("DUT main", "ReaEQ")]
        assert fx.name == "ReaEQ"

    def test_play_and_stop(self):
        from integrations.reaper.backend import ReaperBackend

        adapter = FakeAdapter()
        backend = ReaperBackend(adapter=adapter)

        play = backend.play()
        stop = backend.stop()

        assert play["playing"] is True
        assert stop["playing"] is False

    def test_save_project(self):
        from integrations.reaper.backend import ReaperBackend

        adapter = FakeAdapter()
        backend = ReaperBackend(adapter=adapter)

        result = backend.save_project()

        assert adapter.saved is True
        assert result["saved"] is True

    def test_create_and_delete_track(self):
        from integrations.reaper.backend import ReaperBackend

        adapter = FakeAdapter()
        backend = ReaperBackend(adapter=adapter)

        created = backend.create_track("Print bus", index=2)
        deleted = backend.delete_track("Print bus")

        assert adapter.created_tracks == [("Print bus", 2)]
        assert created.name == "Print bus"
        assert deleted == {"deleted": True, "track_name": "Print bus"}

    def test_set_fx_param(self):
        from integrations.reaper.backend import ReaperBackend

        adapter = FakeAdapter()
        backend = ReaperBackend(adapter=adapter)

        result = backend.set_fx_param("DUT main", "ReaEQ", 0, 0.75)

        assert adapter.fx_param_sets == [("DUT main", "ReaEQ", 0, 0.75)]
        assert result["normalized_value"] == 0.75

    def test_add_item_and_midi_item(self):
        from integrations.reaper.backend import ReaperBackend

        adapter = FakeAdapter()
        backend = ReaperBackend(adapter=adapter)

        item = backend.add_item("DUT main", 1.0, 3.5)
        midi = backend.add_midi_item("DUT main", 4.0, 8.0, quantize=True)

        assert adapter.added_items == [("DUT main", 1.0, 3.5)]
        assert adapter.added_midi_items == [("DUT main", 4.0, 8.0, True)]
        assert item.item_type == "empty"
        assert midi.item_type == "midi"

    def test_insert_media(self):
        from integrations.reaper.backend import ReaperBackend

        adapter = FakeAdapter()
        backend = ReaperBackend(adapter=adapter)

        result = backend.insert_media("DUT main", "/tmp/loop.wav", mode=1)

        assert adapter.inserted_media == [("DUT main", "/tmp/loop.wav", 1)]
        assert result.source_path == "/tmp/loop.wav"

    def test_add_marker_and_region(self):
        from integrations.reaper.backend import ReaperBackend

        adapter = FakeAdapter()
        backend = ReaperBackend(adapter=adapter)

        marker = backend.add_marker(12.0, "Verse")
        region = backend.add_region(16.0, 24.0, "Hook")

        assert adapter.markers == [(12.0, "Verse")]
        assert adapter.regions == [(16.0, 24.0, "Hook")]
        assert marker.name == "Verse"
        assert region.name == "Hook"

    def test_render_project_and_actions(self):
        from integrations.reaper.backend import ReaperBackend

        adapter = FakeAdapter()
        backend = ReaperBackend(adapter=adapter)

        render = backend.render_project(action_id=42230, output_directory="/tmp/renders", output_pattern="$project")
        action = backend.run_action(40044)
        named = backend.run_named_action("_SWS_TEST")

        assert adapter.renders == [{
            "action_id": 42230,
            "command_id": None,
            "output_directory": "/tmp/renders",
            "output_pattern": "$project",
        }]
        assert render["rendered"] is True
        assert adapter.actions == [40044]
        assert adapter.named_actions == ["_SWS_TEST"]
        assert action["action_id"] == 40044
        assert named["command_id"] == "_SWS_TEST"

    def test_real_backend_uses_reapy_boost_when_reapy_missing(self, monkeypatch):
        import importlib
        from integrations.reaper.backend import ReaperBackend

        real_import = importlib.import_module

        def fake_import(name, package=None):
            if name == "reapy":
                raise ModuleNotFoundError("No module named 'reapy'")
            return real_import(name, package)

        monkeypatch.setattr(importlib, "import_module", fake_import)

        backend = ReaperBackend()
        result = backend.health()

        assert result["available"] is True
        assert result["backend"] == "reapy_boost"

    def test_missing_dependency_raises_for_live_calls(self, monkeypatch):
        import importlib
        from integrations.reaper.backend import ReaperBackend
        from integrations.reaper.errors import ReaperUnavailableError

        real_import = importlib.import_module

        def fake_import(name, package=None):
            if name in {"reapy", "reapy_boost"}:
                raise ModuleNotFoundError(f"No module named '{name}'")
            return real_import(name, package)

        monkeypatch.setattr(importlib, "import_module", fake_import)

        backend = ReaperBackend()

        with pytest.raises(ReaperUnavailableError, match="reapy"):
            backend.list_tracks()

    def test_real_backend_falls_back_to_reapy_boost_import(self, monkeypatch):
        import importlib
        from integrations.reaper.backend import ReaperBackend

        class FakeProject:
            path = "/tmp/live.RPP"
            name = "live.RPP"
            has_unsaved_changes = False
            sample_rate = 48000
            bpm = 120

        class FakeModule:
            def Project(self):
                return FakeProject()

        real_import = importlib.import_module

        def fake_import(name, package=None):
            if name == "reapy":
                raise ModuleNotFoundError("No module named 'reapy'")
            if name == "reapy_boost":
                return FakeModule()
            return real_import(name, package)

        monkeypatch.setattr(importlib, "import_module", fake_import)

        backend = ReaperBackend()
        result = backend.health()

        assert result["available"] is True
        assert result["backend"] == "reapy_boost"
