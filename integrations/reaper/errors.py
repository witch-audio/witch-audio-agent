class ReaperError(RuntimeError):
    """Base error for REAPER integration failures."""


class ReaperUnavailableError(ReaperError):
    """Raised when REAPER backend or dependency is unavailable."""


class TrackNotFoundError(ReaperError):
    """Raised when an exact track match cannot be found."""


class FXInsertError(ReaperError):
    """Raised when FX insertion fails."""
