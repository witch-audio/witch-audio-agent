from __future__ import annotations

import importlib
from pathlib import Path
from typing import Any, Optional

from .errors import FXInsertError, ReaperUnavailableError, TrackNotFoundError
from .models import FXInfo, ItemInfo, MarkerInfo, ProjectInfo, RegionInfo, TrackInfo


class _ReapyAdapter:
    """Best-effort live adapter for REAPER via reapy/reapy_boost."""

    def __init__(self) -> None:
        last_error = None
        for module_name in ("reapy", "reapy_boost"):
            try:
                self._reapy = importlib.import_module(module_name)
                self._backend_name = module_name
                break
            except ModuleNotFoundError as exc:
                last_error = exc
                continue
            except Exception as exc:
                raise ReaperUnavailableError(f"Failed to import {module_name} backend: {exc}") from exc
        else:
            raise ReaperUnavailableError(
                "reapy dependency missing. Install reapy-boost / reapy to enable REAPER control."
            ) from last_error

        self._api = getattr(self._reapy, "reascript_api", None)

    def _current_project(self) -> Any:
        try:
            if hasattr(self._reapy, "Project"):
                return self._reapy.Project()
        except Exception as exc:
            raise ReaperUnavailableError(f"Failed to connect to REAPER: {exc}") from exc
        raise ReaperUnavailableError("reapy backend loaded but no supported Project entrypoint was found")

    def health(self) -> dict:
        project = self._current_project()
        name = getattr(project, "name", None) or Path(str(getattr(project, "path", "") or "untitled")).name
        return {
            "available": True,
            "backend": getattr(self, "_backend_name", "reapy"),
            "details": f"connected to {name}",
        }

    def get_project_info(self) -> ProjectInfo:
        project = self._current_project()
        path = _project_path(project)
        name = getattr(project, "name", None) or (Path(path).name if path else "")
        return ProjectInfo(
            path=path,
            name=name,
            is_dirty=bool(getattr(project, "has_unsaved_changes", False) or getattr(project, "dirty", False)),
            sample_rate=_safe_float(getattr(project, "sample_rate", None)),
            bpm=_safe_float(getattr(project, "bpm", None) or getattr(project, "tempo", None)),
        )

    def list_tracks(self) -> list[TrackInfo]:
        project = self._current_project()
        tracks = list(getattr(project, "tracks", []) or [])
        return [_track_to_info(index, track) for index, track in enumerate(tracks)]

    def select_track_by_name(self, name: str) -> TrackInfo:
        tracks = self.list_tracks()
        for track in tracks:
            if track.name == name:
                live_track = self._get_live_track_by_index(track.index)
                if hasattr(live_track, "make_only_selected_track"):
                    live_track.make_only_selected_track()
                elif hasattr(live_track, "select"):
                    project = self._current_project()
                    if hasattr(project, "unselect_all_tracks"):
                        project.unselect_all_tracks()
                    live_track.select()
                return TrackInfo(**{**track.to_dict(), "selected": True})
        raise TrackNotFoundError(f"Track not found: {name}")

    def list_track_fx(self, track_name: str) -> list[FXInfo]:
        live_track = self._get_live_track_by_name(track_name)
        fx_list = list(getattr(live_track, "fxs", None) or getattr(live_track, "fx", []) or [])
        return [_fx_to_info(index, fx) for index, fx in enumerate(fx_list)]

    def insert_fx(self, track_name: str, fx_name: str) -> FXInfo:
        live_track = self._get_live_track_by_name(track_name)
        try:
            if hasattr(live_track, "add_fx"):
                fx = live_track.add_fx(fx_name)
            else:
                raise FXInsertError("Track backend has no add_fx method")
        except Exception as exc:
            raise FXInsertError(f"Failed to insert FX '{fx_name}' on '{track_name}': {exc}") from exc
        fx_list = list(getattr(live_track, "fxs", None) or getattr(live_track, "fx", []) or [])
        return _fx_to_info(len(fx_list) - 1, fx)

    def create_track(self, name: str, index: Optional[int] = None) -> TrackInfo:
        project = self._current_project()
        insert_index = project.n_tracks if index is None else index
        track = project.add_track(index=insert_index, name=name)
        return _track_to_info(insert_index, track)

    def delete_track(self, track_name: str) -> dict:
        track = self._get_live_track_by_name(track_name)
        if not hasattr(track, "delete"):
            raise ReaperUnavailableError("Current backend cannot delete tracks")
        track.delete()
        return {"deleted": True, "track_name": track_name}

    def set_fx_param(self, track_name: str, fx_name: str, param_index: int, normalized_value: float) -> dict:
        track = self._get_live_track_by_name(track_name)
        fx_index, fx = self._get_live_fx_by_name(track, fx_name)
        api = self._require_api()
        api.TrackFX_SetParamNormalized(track.id, fx_index, param_index, normalized_value)
        param_name = api.TrackFX_GetParamName(track.id, fx_index, param_index, "", 2048)[4]
        current_value = api.TrackFX_GetParamNormalized(track.id, fx_index, param_index)
        return {
            "track_name": track_name,
            "fx_name": getattr(fx, "name", fx_name),
            "param_index": param_index,
            "param_name": param_name,
            "normalized_value": current_value,
        }

    def add_item(self, track_name: str, start: float, end: float) -> ItemInfo:
        track = self._get_live_track_by_name(track_name)
        item = track.add_item(start=start, end=end)
        return self._item_to_info(track, item, item_type="empty")

    def add_midi_item(self, track_name: str, start: float, end: float, quantize: bool = False) -> ItemInfo:
        track = self._get_live_track_by_name(track_name)
        item = track.add_midi_item(start=start, end=end, quantize=quantize)
        return self._item_to_info(track, item, item_type="midi")

    def insert_media(self, track_name: str, file_path: str, mode: int = 0) -> ItemInfo:
        project = self._current_project()
        track = self._get_live_track_by_name(track_name)
        api = self._require_api()
        if hasattr(project, "unselect_all_tracks"):
            project.unselect_all_tracks()
        if hasattr(track, "make_only_selected_track"):
            track.make_only_selected_track()
        elif hasattr(track, "select"):
            track.select()
        context = project.make_current_project() if hasattr(project, "make_current_project") else _nullcontext()
        with context:
            result = api.InsertMedia(file_path, mode)
        if result == 0:
            raise ReaperUnavailableError(f"Failed to insert media: {file_path}")
        track = self._get_live_track_by_name(track_name)
        items = list(getattr(track, "items", []) or [])
        if not items:
            raise ReaperUnavailableError(f"Media insert reported success but no item was found on '{track_name}'")
        return self._item_to_info(track, items[-1], item_type="media", source_path=file_path)

    def add_marker(self, position: float, name: str = "") -> MarkerInfo:
        project = self._current_project()
        marker = project.add_marker(position=position, name=name)
        return MarkerInfo(
            index=int(_safe_getattr(marker, "index", -1)),
            name=str(_safe_getattr(marker, "name", name)),
            position=float(_safe_getattr(marker, "position", position) or position),
        )

    def add_region(self, start: float, end: float, name: str = "") -> RegionInfo:
        project = self._current_project()
        region = project.add_region(start=start, end=end, name=name)
        return RegionInfo(
            index=int(_safe_getattr(region, "index", -1)),
            name=str(_safe_getattr(region, "name", name)),
            start=float(_safe_getattr(region, "start", start) or start),
            end=float(_safe_getattr(region, "end", end) or end),
        )

    def render_project(
        self,
        action_id: Optional[int] = None,
        command_id: Optional[str] = None,
        output_directory: Optional[str] = None,
        output_pattern: Optional[str] = None,
    ) -> dict:
        project = self._current_project()
        api = self._require_api()
        if output_directory is not None:
            api.GetSetProjectInfo_String(project.id, "RENDER_FILE", output_directory, True)
        if output_pattern is not None:
            api.GetSetProjectInfo_String(project.id, "RENDER_PATTERN", output_pattern, True)
        if command_id:
            self.run_named_action(command_id)
        elif action_id is not None:
            self.run_action(action_id)
        else:
            raise ReaperUnavailableError("render_project requires action_id or command_id")
        return {
            "rendered": True,
            "action_id": action_id,
            "command_id": command_id,
            "output_directory": output_directory,
            "output_pattern": output_pattern,
        }

    def run_action(self, action_id: int) -> dict:
        project = self._current_project()
        if hasattr(project, "perform_action"):
            project.perform_action(action_id)
        else:
            raise ReaperUnavailableError("Current backend cannot run numeric actions")
        return {"ok": True, "action_id": action_id}

    def run_named_action(self, command_id: str) -> dict:
        api = self._require_api()
        action_id = int(api.NamedCommandLookup(command_id))
        if action_id <= 0:
            raise ReaperUnavailableError(f"Named REAPER action not found: {command_id}")
        self.run_action(action_id)
        return {"ok": True, "command_id": command_id, "action_id": action_id}

    def play(self) -> dict:
        project = self._current_project()
        if hasattr(project, "play"):
            project.play()
        else:
            raise ReaperUnavailableError("Current backend cannot start transport")
        return {"playing": True}

    def stop(self) -> dict:
        project = self._current_project()
        if hasattr(project, "stop"):
            project.stop()
        else:
            raise ReaperUnavailableError("Current backend cannot stop transport")
        return {"playing": False}

    def save_project(self) -> dict:
        project = self._current_project()
        if hasattr(project, "save"):
            project.save()
        else:
            raise ReaperUnavailableError("Current backend cannot save project")
        path = _project_path(project)
        return {"saved": True, "path": path}

    def _get_live_track_by_index(self, index: int) -> Any:
        project = self._current_project()
        tracks = list(getattr(project, "tracks", []) or [])
        try:
            return tracks[index]
        except IndexError as exc:
            raise TrackNotFoundError(f"Track index not found: {index}") from exc

    def _get_live_track_by_name(self, name: str) -> Any:
        project = self._current_project()
        tracks = list(getattr(project, "tracks", []) or [])
        for track in tracks:
            if str(getattr(track, "name", "")) == name:
                return track
        raise TrackNotFoundError(f"Track not found: {name}")

    def _get_live_fx_by_name(self, track: Any, fx_name: str) -> tuple[int, Any]:
        fx_list = list(getattr(track, "fxs", None) or getattr(track, "fx", []) or [])
        for index, fx in enumerate(fx_list):
            if str(getattr(fx, "name", "")) == fx_name:
                return index, fx
        raise FXInsertError(f"FX not found on '{track.name}': {fx_name}")

    def _item_to_info(self, track: Any, item: Any, item_type: str, source_path: str = "") -> ItemInfo:
        items = list(getattr(track, "items", []) or [])
        item_id = getattr(item, "id", None)
        index = next((i for i, candidate in enumerate(items) if getattr(candidate, "id", None) == item_id), len(items) - 1)
        return ItemInfo(
            index=max(index, 0),
            track_name=str(getattr(track, "name", "")),
            position=float(getattr(item, "position", 0.0) or 0.0),
            length=float(getattr(item, "length", 0.0) or 0.0),
            item_type=item_type,
            source_path=source_path,
        )

    def _require_api(self) -> Any:
        if self._api is None:
            raise ReaperUnavailableError("reascript_api is unavailable in the current REAPER backend")
        return self._api


class ReaperBackend:
    def __init__(self, adapter: Optional[Any] = None) -> None:
        self._adapter = adapter

    def _get_adapter(self) -> Any:
        if self._adapter is None:
            self._adapter = _ReapyAdapter()
        return self._adapter

    def health(self) -> dict:
        try:
            return self._get_adapter().health()
        except Exception as exc:
            return {
                "available": False,
                "backend": "reapy",
                "details": str(exc),
            }

    def get_project_info(self) -> ProjectInfo:
        return self._get_adapter().get_project_info()

    def list_tracks(self) -> list[TrackInfo]:
        return self._get_adapter().list_tracks()

    def select_track_by_name(self, name: str) -> TrackInfo:
        return self._get_adapter().select_track_by_name(name)

    def list_track_fx(self, track_name: str) -> list[FXInfo]:
        return self._get_adapter().list_track_fx(track_name)

    def insert_fx(self, track_name: str, fx_name: str) -> FXInfo:
        return self._get_adapter().insert_fx(track_name, fx_name)

    def create_track(self, name: str, index: Optional[int] = None) -> TrackInfo:
        return self._get_adapter().create_track(name, index=index)

    def delete_track(self, track_name: str) -> dict:
        return self._get_adapter().delete_track(track_name)

    def set_fx_param(self, track_name: str, fx_name: str, param_index: int, normalized_value: float) -> dict:
        return self._get_adapter().set_fx_param(track_name, fx_name, param_index, normalized_value)

    def add_item(self, track_name: str, start: float, end: float) -> ItemInfo:
        return self._get_adapter().add_item(track_name, start, end)

    def add_midi_item(self, track_name: str, start: float, end: float, quantize: bool = False) -> ItemInfo:
        return self._get_adapter().add_midi_item(track_name, start, end, quantize=quantize)

    def insert_media(self, track_name: str, file_path: str, mode: int = 0) -> ItemInfo:
        return self._get_adapter().insert_media(track_name, file_path, mode=mode)

    def add_marker(self, position: float, name: str = "") -> MarkerInfo:
        return self._get_adapter().add_marker(position, name=name)

    def add_region(self, start: float, end: float, name: str = "") -> RegionInfo:
        return self._get_adapter().add_region(start, end, name=name)

    def render_project(
        self,
        action_id: Optional[int] = None,
        command_id: Optional[str] = None,
        output_directory: Optional[str] = None,
        output_pattern: Optional[str] = None,
    ) -> dict:
        return self._get_adapter().render_project(
            action_id=action_id,
            command_id=command_id,
            output_directory=output_directory,
            output_pattern=output_pattern,
        )

    def run_action(self, action_id: int) -> dict:
        return self._get_adapter().run_action(action_id)

    def run_named_action(self, command_id: str) -> dict:
        return self._get_adapter().run_named_action(command_id)

    def play(self) -> dict:
        return self._get_adapter().play()

    def stop(self) -> dict:
        return self._get_adapter().stop()

    def save_project(self) -> dict:
        return self._get_adapter().save_project()


def _safe_float(value: Any) -> Optional[float]:
    if value is None or value == "":
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _project_path(project: Any) -> str:
    path = str(getattr(project, "path", "") or "")
    name = str(getattr(project, "name", "") or "")
    if path and name and not path.endswith(name):
        return str(Path(path) / name)
    return path


def _track_to_info(index: int, track: Any) -> TrackInfo:
    fx_list = list(getattr(track, "fxs", None) or getattr(track, "fx", []) or [])
    return TrackInfo(
        index=index,
        name=str(getattr(track, "name", "")),
        guid=str(getattr(track, "GUID", None) or getattr(track, "guid", "") or ""),
        selected=_safe_bool_attr(track, "selected", fallback_method="is_selected"),
        muted=_safe_bool_attr(track, "muted", fallback_method="is_muted"),
        solo=_safe_bool_attr(track, "solo", fallback_method="is_solo"),
        armed=_safe_bool_attr(track, "armed", fallback_method="is_armed"),
        fx_count=len(fx_list),
    )


def _fx_to_info(index: int, fx: Any) -> FXInfo:
    return FXInfo(
        index=index,
        name=str(getattr(fx, "name", "")),
        enabled=_safe_bool_attr(fx, "enabled", fallback_attr="is_enabled"),
    )


def _safe_bool_attr(obj: Any, attr: str, fallback_attr: Optional[str] = None, fallback_method: Optional[str] = None) -> bool:
    for name in (attr, fallback_attr, fallback_method):
        if not name:
            continue
        if hasattr(obj, name):
            try:
                value = getattr(obj, name)
                return bool(value() if callable(value) else value)
            except Exception:
                continue
    return False


def _safe_getattr(obj: Any, attr: str, default: Any) -> Any:
    try:
        return getattr(obj, attr)
    except Exception:
        return default


class _nullcontext:
    def __enter__(self):
        return None

    def __exit__(self, exc_type, exc, tb):
        return False
