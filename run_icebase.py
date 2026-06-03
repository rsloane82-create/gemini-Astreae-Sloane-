#!/usr/bin/env python3
import argparse
from pathlib import Path

from icebase.agents.interface import AgentTelemetryInterface
from icebase.persistence.json_store import write_json, write_jsonl
from icebase.performance import profile_run, run_batch
from icebase.scenarios import SCENARIOS
from icebase.visualization.text import summarize


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Ice shell around heat core simulation for stability, heat retention, and survivability."
    )
    parser.add_argument("--scenario", default="baseline", choices=sorted(SCENARIOS.keys()))
    parser.add_argument("--steps", type=int, default=720)
    parser.add_argument(
        "--time-step",
        "--dt",
        dest="time_step_seconds",
        type=float,
        default=10.0,
        help="Timestep in seconds",
    )
    parser.add_argument("--json", type=Path, help="Write telemetry JSON array to this path")
    parser.add_argument("--jsonl", type=Path, help="Write telemetry JSON lines to this path")
    parser.add_argument("--stream", action="store_true", help="Print JSONL stream for service agents")
    parser.add_argument("--profile", action="store_true", help="Print wall-clock runtime")
    parser.add_argument(
        "--batch",
        action="store_true",
        help="Run all built-in scenarios in parallel and print summary per scenario",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if args.batch:
        configs = {name: factory() for name, factory in SCENARIOS.items()}
        results = run_batch(configs, steps=args.steps, dt_seconds=args.time_step_seconds)
        for name in sorted(results):
            print(f"\n== Scenario: {name} ==")
            print(summarize(results[name].frames))
        return

    config = SCENARIOS[args.scenario]()
    if args.profile:
        result, elapsed_s = profile_run(config, steps=args.steps, dt_seconds=args.time_step_seconds)
        print(f"Profile: {elapsed_s:.6f}s for {args.steps} steps")
    else:
        result, _ = profile_run(config, steps=args.steps, dt_seconds=args.time_step_seconds)

    frames = result.frames
    print(summarize(frames))

    interface = AgentTelemetryInterface(frames)
    if args.stream:
        print("\n# JSONL stream")
        print(interface.stream_payload())

    if args.json:
        write_json(args.json, frames)
        print(f"\nWrote JSON telemetry to {args.json}")

    if args.jsonl:
        write_jsonl(args.jsonl, frames)
        print(f"Wrote JSONL telemetry to {args.jsonl}")


if __name__ == "__main__":
    main()
