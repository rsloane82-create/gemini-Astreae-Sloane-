from dataclasses import dataclass


@dataclass
class ShellState:
    temperature_k: float
    integrity: float
    damage_factor: float = 0.0


def apply_damage(shell: ShellState, damage_rate: float, dt_s: float) -> None:
    shell.damage_factor = min(0.95, max(0.0, shell.damage_factor + damage_rate * dt_s))
    shell.integrity = max(0.0, min(1.0, 1.0 - shell.damage_factor))


def apply_repair(shell: ShellState, repair_rate: float, dt_s: float) -> None:
    shell.damage_factor = min(0.95, max(0.0, shell.damage_factor - repair_rate * dt_s))
    shell.integrity = max(0.0, min(1.0, 1.0 - shell.damage_factor))
