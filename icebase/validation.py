from icebase.config.mission import MissionConfig


class ValidationError(ValueError):
    pass


def validate_config(config: MissionConfig) -> None:
    if config.core.heat_capacity_j_per_k <= 0:
        raise ValidationError("Core heat capacity must be positive.")
    if config.shell.heat_capacity_j_per_k <= 0:
        raise ValidationError("Shell heat capacity must be positive.")
    if config.shell.area_m2 <= 0 or config.shell.thickness_m <= 0:
        raise ValidationError("Shell area and thickness must be positive.")
    if not 0 <= config.shell.emissivity <= 1:
        raise ValidationError("Shell emissivity must be between 0 and 1.")
    if not 0 <= config.goals.min_shell_integrity <= 1:
        raise ValidationError("Minimum shell integrity must be between 0 and 1.")
    if config.goals.min_core_temp_k >= config.goals.max_core_temp_k:
        raise ValidationError("Core temperature goal bounds are invalid.")
