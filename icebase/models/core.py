from dataclasses import dataclass


@dataclass
class CoreState:
    temperature_k: float
    output_w: float


def update_core_temperature(core: CoreState, net_heat_j: float, heat_capacity_j_per_k: float) -> None:
    core.temperature_k += net_heat_j / heat_capacity_j_per_k
