# Biomedical & Pharmaceutical examples

These are small, synthetic, runnable QUBO examples for exploration. They are not production-validated industry solvers.

Run from the SDK repository root after installing the package:

```bash
python examples/02_medical/01_biomedical_pharmaceutical/01_staff_shift_assignment.py
```

For a compatible FPGA, add `--backend n512 --port /dev/ttyUSB0` or the appropriate N=1024 backend/port.

## Examples
- `01_staff_shift_assignment.py`
- `02_research_option_selection.py`

All examples default to the CPU `mock_exact` backend (maximum 24 variables). See `docs/EXAMPLE_CATALOG.md` for modelling boundaries.
