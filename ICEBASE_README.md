# Icebase: Ice Shell + Firebase Heat Core

## Mission

The mission is to preserve a heat core (`Firebase`) inside an ice shell in space
through controlled thermal balance.

Measurable goals:

- **Stability:** keep core temperature within a safe range
- **Heat retention:** keep enough useful heat inside the system
- **Survivability:** maintain shell integrity and avoid collapse/overheat states

## Domain split

- `icebase/models/thermal.py` — heat transfer and radiation math
- `icebase/models/shell.py` — shell integrity, damage, and repair
- `icebase/models/core.py` — core state and temperature updates
- `icebase/models/environment.py` — orbital sun exposure and deep-space cold
- `icebase/models/control.py` — dynamic control strategy

## Scalable project structure

- `icebase/engine/` — simulation engine
- `icebase/config/` — mission and parameter configuration
- `icebase/visualization/` — text summary output
- `icebase/persistence/` — JSON and JSONL exporters
- `icebase/agents/` — interface for other service agents
- `icebase/telemetry/` — standardized telemetry schema/stream

## First executable milestone

Run baseline simulation:

```bash
python3 run_icebase.py --scenario baseline --steps 720 --time-step 10
```

## Progressive realism included

- Orbital cycle effects
- Radiation variability
- Shell damage and active repair
- Dynamic control of core output and repair rate

## Shared outputs for service agents

Telemetry schema (`icebase.telemetry.v1`) includes:

- temperature gradient
- energy balance
- shell integrity
- alert states (`core_collapse`, `shell_breach`, `overheat`)

## Safety and validation gates

- Config sanity checks in `icebase/validation.py`
- Reproducible scenarios in `icebase/scenarios.py`:
  - `core_collapse`
  - `shell_breach`
  - `overheat`
  - `orbital_stress`

## Scaling path

- Parallel scenario batches (`--batch`)
- Runtime profiling (`--profile`)
- JSON/JSONL telemetry export for downstream agents

## Plain language

**Ice shell preserves heat core through controlled thermal balance.**
