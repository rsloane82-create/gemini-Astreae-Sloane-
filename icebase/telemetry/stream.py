import json
from collections.abc import Iterable

from icebase.telemetry.types import TelemetryFrame


def to_json_lines(frames: Iterable[TelemetryFrame]) -> str:
    return "\n".join(json.dumps(frame.to_dict(), sort_keys=True) for frame in frames)
