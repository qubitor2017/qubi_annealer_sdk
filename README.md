# Qubitor SDK 1.1.0 — Developer Preview

**Host-side Python SDK for Qubitor FPGA optimisation hardware.**

The SDK lets developers construct supported binary optimisation models, represent them as QUBO / PUBO / Ising models, submit QUBO instances to a compatible Qubitor FPGA over UART, and retrieve candidate solutions.

> **Hardware is sold and supplied separately by Qubitor.** This repository contains host-side SDK software only. It does not contain FPGA RTL, XDC constraints, Vivado projects, FPGA bitstreams, firmware source, or confidential hardware implementation files. A compatible programmed Qubitor device is required for hardware execution.

## What's included

- Python package `qubitor`
- Binary model builder for linear and quadratic objectives and equality constraints.
- QUBO and Ising model representations and conversion.
- PUBO representation with host-side Rosenberg quadratization to QUBO.
- N=512 dense and N=1024 sparse UART host adapters.
- Small exact mock backend for local tests (up to 24 variables; not a hardware-performance benchmark).
- Max-Cut formulation and decoder.
- Historical `qubif_sdk` compatibility shim for the older Max-Cut demo.
- Examples, tests and host-side documentation.

## Not included

- FPGA RTL, XDC, Vivado projects or bitstreams.
- Ramanujan, Euler, AI_EULER or the Qubitor research-agent framework.
- A general MILP/MIQP solver, unrestricted symbolic mathematics engine, or production formal verification system.

## Install from GitHub

```bash
git clone https://github.com/qubitor2017/qubitor-sdk.git
cd qubitor-sdk
python -m venv .venv

# Linux / macOS
source .venv/bin/activate

# Windows PowerShell
# .venv\Scripts\Activate.ps1

python -m pip install --upgrade pip
python -m pip install -e '.[serial]'
```

Use `python -m pip install -e .` if you only want the CPU-only model tools and do not need UART hardware communication. The `serial` extra installs `pyserial`.

## Quick start: QUBO on CPU

```python
import qubitor

Q = [
    [-1.0, -1.0],
    [-1.0, -1.0],
]
model = qubitor.from_qubo(Q)
result = qubitor.solve(model, backend="mock_exact")

print("bits:", result.solution)
print("energy:", result.objective)
print("status:", result.status)
```

The mock backend exhaustively enumerates small models and is limited to 24 variables. It is intended for examples and correctness checks, not performance claims.

## Quick start: Max-Cut

```python
from qubitor import build_maxcut, decode_maxcut, solve

edges = [(0, 1), (1, 2), (2, 3), (3, 0), (0, 2)]
qubo = build_maxcut(edges, n_nodes=4)
result = solve(qubo, backend="mock_exact")

print("cut value:", decode_maxcut(result.solution, edges))
```

Run the included example:

```bash
python examples/maxcut_demo.py --backend mock_exact
```

## Connect a Qubitor FPGA

Hardware execution must be explicitly selected; the default backend is the local `mock_exact` backend.

```python
import qubitor

qubo = qubitor.from_qubo({
    (0, 0): -2.0,
    (0, 1): -1.0,
    (1, 0): -1.0,
    (1, 1): -1.0,
}, n=2)

result = qubitor.solve(
    qubo,
    backend="n512",          # or "n1024"
    port="/dev/ttyUSB0",     # Windows example: "COM4"
    scale=1.0,
    cooling=1,
    seed=0xACE12026,
    max_wait=120.0,
    timeout=3.0,
)
print(result.solution, result.objective, result.status)
```

The N=512 and N=1024 adapters use different memory layouts and protocol variants. The SDK does not auto-detect the connected board or verify which bitstream is programmed. Use only a Qubitor-supplied, compatible device/bitstream and follow the hardware-specific setup instructions supplied with that device.

### Backend limits and coefficient scaling

- N=512: dense QUBO interface, up to 512 binary variables. The current adapter checks the signed 16-bit coefficient storage range after scaling.
- N=1024: sparse QUBO interface, up to 1,024 binary variables, with a maximum of 65,535 directed matrix entries in this adapter.
- Coefficients are quantized using `round(coefficient * scale)`. Choose a scale that preserves useful coefficient precision without overflow. The default scale is 2 for model-builder-generated QUBOs and 1 for direct QUBO/Ising inputs.
- The returned FPGA solution is a candidate. Independently recompute the original objective and validate constraints in your application.

## PUBO support

The SDK represents higher-order binary polynomial objectives using `PuboModel` and converts them to QUBO through Rosenberg quadratization before hardware submission:

```python
import qubitor

pubo = qubitor.from_pubo({(0, 1, 2): -5.0, (0,): 1.0}, n=3)
result = qubitor.solve(pubo, backend="mock_exact")
print(result.solution, result.objective)
```

This is host-side quadratization. The FPGA interface accepts QUBO coefficients; the FPGA is not executing native higher-order PUBO terms. Quadratization may add ancilla variables and increase model size.

## Supported model-builder scope

The current `Model` builder supports binary variables, linear terms, quadratic terms through `add_quadratic`, and equality constraints / one-hot constraints using penalty compilation. Inequalities, continuous variables, arbitrary integer variables, automatic slack modelling, and general MILP/MIQP ingestion are not implemented.

## Tests

```bash
python -m unittest discover -s tests -v
```

Tests use the CPU-only mock backend and do not require a physical FPGA. They do not certify a particular board, bitstream, UART wiring or hardware revision.

## License and distribution

This is source-available proprietary software from Qubitor Labs. Public visibility of this repository does not grant permission to redistribute, sublicense, modify for third-party distribution, or use commercially beyond the rights expressly granted by a separate Qubitor SDK licence/EULA. Qubitor should approve the final customer licence before public release. This README is not legal advice.

## Support

Website: https://www.qubitor.com  
GitHub: https://github.com/qubitor2017/qubitor-sdk  
Contact: info@qubitor.com
