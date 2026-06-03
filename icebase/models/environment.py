import math

from icebase.config.mission import EnvironmentConfig

SOLAR_VARIABILITY_PERIOD_S = 173.0


def orbital_solar_flux(config: EnvironmentConfig, time_s: float) -> float:
    orbital_phase = 2.0 * math.pi * (time_s / config.orbital_period_s)
    orbital_modulation = 0.5 * (1.0 + math.sin(orbital_phase))
    variability = 1.0 + config.radiation_variability * math.sin(time_s / SOLAR_VARIABILITY_PERIOD_S)
    return max(0.0, config.average_solar_flux_w_m2 * orbital_modulation * variability)
