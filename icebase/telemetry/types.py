from dataclasses import asdict, dataclass
from typing import Any


@dataclass
class EnergyBalance:
    core_output_w: float
    conducted_core_to_shell_w: float
    solar_gain_w: float
    radiative_loss_w: float


@dataclass
class TelemetryFrame:
    step: int
    time_s: float
    core_temp_k: float
    shell_temp_k: float
    temp_gradient_k: float
    shell_integrity: float
    heat_retention_ratio: float
    survivability: bool
    alerts: list[str]
    energy_balance: EnergyBalance

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["schema_version"] = "icebase.telemetry.v1"
        return payload
