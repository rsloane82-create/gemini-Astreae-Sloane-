from dataclasses import dataclass

from icebase.config.mission import MissionConfig
from icebase.models.control import compute_action
from icebase.models.core import CoreState, update_core_temperature
from icebase.models.environment import orbital_solar_flux
from icebase.models.shell import ShellState, apply_damage, apply_repair
from icebase.models.thermal import conductive_heat_flow_w, radiative_loss_w
from icebase.telemetry.types import EnergyBalance, TelemetryFrame
from icebase.validation import validate_config


@dataclass
class SimulationResult:
    frames: list[TelemetryFrame]


def _alerts(config: MissionConfig, core_temp_k: float, shell_integrity: float) -> list[str]:
    alerts: list[str] = []
    if core_temp_k < config.goals.min_core_temp_k:
        alerts.append("core_collapse")
    if core_temp_k > config.goals.max_core_temp_k:
        alerts.append("overheat")
    if shell_integrity < config.goals.min_shell_integrity:
        alerts.append("shell_breach")
    return alerts


def run_simulation(
    config: MissionConfig,
    *,
    steps: int = 720,
    dt_s: float = 10.0,
    initial_damage_rate: float = 1.5e-5,
) -> SimulationResult:
    validate_config(config)

    core = CoreState(temperature_k=config.core.temperature_k, output_w=config.core.base_output_w)
    shell = ShellState(
        temperature_k=config.shell.temperature_k,
        integrity=max(0.0, min(1.0, config.shell.integrity)),
        damage_factor=max(0.0, min(0.95, 1.0 - config.shell.integrity)),
    )

    frames: list[TelemetryFrame] = []

    for step in range(steps):
        time_s = step * dt_s
        action = compute_action(
            config.control,
            core.temperature_k,
            config.core.min_output_w,
            config.core.max_output_w,
            shell.integrity,
        )
        core.output_w = action.core_output_w

        solar_flux_w_m2 = orbital_solar_flux(config.environment, time_s)
        solar_gain_w = solar_flux_w_m2 * config.shell.area_m2 * 0.65

        conducted_w = conductive_heat_flow_w(
            core.temperature_k,
            shell.temperature_k,
            config.shell.conductivity_w_mk,
            config.shell.area_m2,
            config.shell.thickness_m,
            shell.integrity,
        )
        radiative_loss = radiative_loss_w(
            shell.temperature_k,
            config.environment.space_temp_k,
            config.shell.area_m2,
            config.shell.emissivity,
        )

        core_net_j = (core.output_w - conducted_w) * dt_s
        shell_net_j = (conducted_w + solar_gain_w - radiative_loss) * dt_s

        update_core_temperature(core, core_net_j, config.core.heat_capacity_j_per_k)
        shell.temperature_k += shell_net_j / config.shell.heat_capacity_j_per_k

        degradation_bias = max(0.0, (core.temperature_k - config.control.target_core_temp_k) / 120_000.0)
        apply_damage(shell, initial_damage_rate + degradation_bias, dt_s)
        apply_repair(shell, action.repair_rate, dt_s)

        available_heat = core.output_w + solar_gain_w
        retained_heat = max(0.0, available_heat - radiative_loss)
        retention = max(0.0, min(1.0, retained_heat / max(available_heat, 1.0)))

        alerts = _alerts(config, core.temperature_k, shell.integrity)
        survivability = not alerts and retention >= config.goals.heat_retention_target

        frame = TelemetryFrame(
            step=step,
            time_s=time_s,
            core_temp_k=core.temperature_k,
            shell_temp_k=shell.temperature_k,
            temp_gradient_k=core.temperature_k - shell.temperature_k,
            shell_integrity=shell.integrity,
            heat_retention_ratio=retention,
            survivability=survivability,
            alerts=alerts,
            energy_balance=EnergyBalance(
                core_output_w=core.output_w,
                conducted_core_to_shell_w=conducted_w,
                solar_gain_w=solar_gain_w,
                radiative_loss_w=radiative_loss,
            ),
        )
        frames.append(frame)

    return SimulationResult(frames=frames)
