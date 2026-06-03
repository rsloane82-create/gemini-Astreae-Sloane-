import json
from pathlib import Path
from typing import Iterable

from icebase.telemetry.types import TelemetryFrame


def write_json(path: Path, frames: Iterable[TelemetryFrame]) -> None:
    payload = [frame.to_dict() for frame in frames]
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def write_jsonl(path: Path, frames: Iterable[TelemetryFrame]) -> None:
    lines = [json.dumps(frame.to_dict(), sort_keys=True) for frame in frames]
    path.write_text("\n".join(lines), encoding="utf-8")
