from concurrent.futures import ThreadPoolExecutor
from time import perf_counter

from icebase.config.mission import MissionConfig
from icebase.engine.simulator import SimulationResult, run_simulation


def profile_run(config: MissionConfig, steps: int, dt_s: float) -> tuple[SimulationResult, float]:
    start = perf_counter()
    result = run_simulation(config, steps=steps, dt_s=dt_s)
    elapsed_s = perf_counter() - start
    return result, elapsed_s


def run_batch(configs: dict[str, MissionConfig], steps: int, dt_s: float, max_workers: int = 4) -> dict[str, SimulationResult]:
    items = list(configs.items())
    results: dict[str, SimulationResult] = {}

    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        future_map = {
            pool.submit(run_simulation, config, steps=steps, dt_s=dt_s): name
            for name, config in items
        }
        for future, name in ((future, future_map[future]) for future in future_map):
            results[name] = future.result()

    return results
