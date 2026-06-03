from dataclasses import dataclass

from icebase.config.mission import ControlConfig


@dataclass
class ControlAction:
    core_output_w: float
    repair_rate: float


def compute_action(
    config: ControlConfig,
    core_temp_k: float,
    min_output_w: float,
    max_output_w: float,
    shell_integrity: float,
) -> ControlAction:
    error = config.target_core_temp_k - core_temp_k
    output_w = max(min_output_w, min(max_output_w, min_output_w + config.kp_output * error))
    repair_rate = max(0.0, config.kp_repair * (1.0 - shell_integrity))
    return ControlAction(core_output_w=output_w, repair_rate=repair_rate)
