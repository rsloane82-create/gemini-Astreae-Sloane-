STEFAN_BOLTZMANN = 5.670374419e-8
MINIMUM_EFFECTIVE_SHELL_THICKNESS_M = 0.2
MINIMUM_SHELL_INTEGRITY_FACTOR = 0.2


def conductive_heat_flow_w(
    core_temp_k: float,
    shell_temp_k: float,
    conductivity_w_mk: float,
    area_m2: float,
    thickness_m: float,
    integrity: float,
) -> float:
    effective_integrity = max(MINIMUM_SHELL_INTEGRITY_FACTOR, integrity)
    effective_thickness = max(MINIMUM_EFFECTIVE_SHELL_THICKNESS_M, thickness_m * effective_integrity)
    effective_conductivity = conductivity_w_mk * (1.0 + (1.0 - integrity))
    return effective_conductivity * area_m2 * (core_temp_k - shell_temp_k) / effective_thickness


def radiative_loss_w(shell_temp_k: float, space_temp_k: float, area_m2: float, emissivity: float) -> float:
    shell_t4 = max(shell_temp_k, 1.0) ** 4
    space_t4 = max(space_temp_k, 1.0) ** 4
    return emissivity * STEFAN_BOLTZMANN * area_m2 * max(0.0, shell_t4 - space_t4)
