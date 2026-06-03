from icebase.telemetry.types import TelemetryFrame


def summarize(frames: list[TelemetryFrame]) -> str:
    if not frames:
        return "No telemetry frames produced."

    first = frames[0]
    last = frames[-1]
    survivors = sum(1 for frame in frames if frame.survivability)
    retention_avg = sum(frame.heat_retention_ratio for frame in frames) / len(frames)

    return (
        "Icebase Mission Summary\n"
        f"- Steps: {len(frames)}\n"
        f"- Time range: {first.time_s:.1f}s -> {last.time_s:.1f}s\n"
        f"- Core temperature: {first.core_temp_k:.2f}K -> {last.core_temp_k:.2f}K\n"
        f"- Shell temperature: {first.shell_temp_k:.2f}K -> {last.shell_temp_k:.2f}K\n"
        f"- Final shell integrity: {last.shell_integrity:.3f}\n"
        f"- Average heat retention: {retention_avg:.3f}\n"
        f"- Survivability frames: {survivors}/{len(frames)}"
    )
