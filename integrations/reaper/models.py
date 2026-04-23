from dataclasses import asdict, dataclass
from typing import Optional


@dataclass(slots=True)
class ProjectInfo:
    path: str
    name: str
    is_dirty: bool = False
    sample_rate: Optional[float] = None
    bpm: Optional[float] = None

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(slots=True)
class TrackInfo:
    index: int
    name: str
    guid: str = ""
    selected: bool = False
    muted: bool = False
    solo: bool = False
    armed: bool = False
    fx_count: int = 0

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(slots=True)
class FXInfo:
    index: int
    name: str
    enabled: bool = True

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(slots=True)
class ItemInfo:
    index: int
    track_name: str
    position: float
    length: float
    item_type: str
    source_path: str = ""

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(slots=True)
class MarkerInfo:
    index: int
    name: str
    position: float

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(slots=True)
class RegionInfo:
    index: int
    name: str
    start: float
    end: float

    def to_dict(self) -> dict:
        return asdict(self)
