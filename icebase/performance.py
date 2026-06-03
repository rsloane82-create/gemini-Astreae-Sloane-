from concurrent.futures import ThreadPoolExecutor, as_completed
from os import cpu_count
from time import perf_counter

from icebase.config.mission import MissionConfig
from icebase.engine.simulator import SimulationResult, run_simulation


def profile_run(config: MissionConfig, steps: int, dt_seconds: float) -> tuple[SimulationResult, float]:
    start = perf_counter()
    result = run_simulation(config, steps=steps, dt_seconds=dt_seconds)
    elapsed_s = perf_counter() - start
    return result, elapsed_s


def run_batch(
    configs: dict[str, MissionConfig],
    steps: int,
    dt_seconds: float,
    max_workers: int | None = None,
) -> dict[str, SimulationResult]:
    items = list(configs.items())
    results: dict[str, SimulationResult] = {}
    worker_count = max_workers or max(1, min(len(items), (cpu_count() or 1)))

    with ThreadPoolExecutor(max_workers=worker_count) as pool:
        future_map = {
            pool.submit(run_simulation, config, steps=steps, dt_seconds=dt_seconds): name
            for name, config in items
        }
        for future in as_completed(future_map):
            name = future_map[future]
            results[name] = future.result()

    return results
