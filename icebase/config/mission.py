from dataclasses import dataclass


@dataclass(frozen=True)
class MissionGoals:
    min_core_temp_k: float = 280.0
    max_core_temp_k: float = 335.0
    min_shell_integrity: float = 0.55
    heat_retention_target: float = 0.35


@dataclass(frozen=True)
class CoreConfig:
    temperature_k: float = 320.0
    heat_capacity_j_per_k: float = 6.0e6
    min_output_w: float = 80_000.0
    base_output_w: float = 250_000.0
    max_output_w: float = 420_000.0


@dataclass(frozen=True)
class ShellConfig:
    temperature_k: float = 260.0
    heat_capacity_j_per_k: float = 3.5e6
    area_m2: float = 500.0
    thickness_m: float = 2.0
    conductivity_w_mk: float = 2.2
    emissivity: float = 0.60
    integrity: float = 1.0


@dataclass(frozen=True)
class EnvironmentConfig:
    space_temp_k: float = 40.0
    average_solar_flux_w_m2: float = 210.0
    orbital_period_s: float = 18_000.0
    radiation_variability: float = 0.10


@dataclass(frozen=True)
class ControlConfig:
    target_core_temp_k: float = 305.0
    kp_output: float = 1500.0
    kp_repair: float = 0.25


@dataclass(frozen=True)
class MissionConfig:
    goals: MissionGoals = MissionGoals()
    core: CoreConfig = CoreConfig()
    shell: ShellConfig = ShellConfig()
    environment: EnvironmentConfig = EnvironmentConfig()
    control: ControlConfig = ControlConfig()
