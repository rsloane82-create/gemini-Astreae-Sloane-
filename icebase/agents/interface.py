from dataclasses import dataclass

from icebase.telemetry.stream import to_json_lines
from icebase.telemetry.types import TelemetryFrame


@dataclass
class AgentTelemetryInterface:
    frames: list[TelemetryFrame]

    def latest_payload(self) -> dict:
        return self.frames[-1].to_dict() if self.frames else {}

    def stream_payload(self) -> str:
        return to_json_lines(self.frames)
