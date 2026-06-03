from dataclasses import replace

from icebase.config.mission import CoreConfig, EnvironmentConfig, MissionConfig, ShellConfig


def baseline() -> MissionConfig:
    return MissionConfig()


def core_collapse() -> MissionConfig:
    config = MissionConfig()
    weak_core = replace(
        config.core,
        temperature_k=275.0,
        min_output_w=5_000.0,
        base_output_w=15_000.0,
        max_output_w=30_000.0,
    )
    return replace(config, core=weak_core)


def shell_breach() -> MissionConfig:
    config = MissionConfig()
    return replace(config, shell=replace(config.shell, integrity=0.38, thickness_m=1.0))


def overheat() -> MissionConfig:
    config = MissionConfig()
    hot_core = replace(config.core, base_output_w=390_000.0, max_output_w=460_000.0, temperature_k=345.0)
    hot_env = replace(config.environment, average_solar_flux_w_m2=260.0)
    return replace(config, core=hot_core, environment=hot_env)


def orbital_stress() -> MissionConfig:
    config = MissionConfig()
    stressed_env = replace(config.environment, orbital_period_s=12_000.0, radiation_variability=0.35)
    stressed_shell = replace(config.shell, conductivity_w_mk=2.8)
    return replace(config, environment=stressed_env, shell=stressed_shell)


SCENARIOS = {
    "baseline": baseline,
    "core_collapse": core_collapse,
    "shell_breach": shell_breach,
    "overheat": overheat,
    "orbital_stress": orbital_stress,
}
