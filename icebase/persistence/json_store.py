import json
from pathlib import Path
from typing import Iterable

from icebase.telemetry.types import TelemetryFrame


def write_json(path: Path, frames: Iterable[TelemetryFrame]) -> None:
    payload = [frame.to_dict() for frame in frames]
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def write_jsonl(path: Path, frames: Iterable[TelemetryFrame]) -> None:
    with path.open("w", encoding="utf-8") as output:
        for index, frame in enumerate(frames):
            if index:
                output.write("\n")
            output.write(json.dumps(frame.to_dict(), sort_keys=True))
