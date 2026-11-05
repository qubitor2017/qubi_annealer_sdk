# SDK scope — 2.0.0

SDK 2.0 is a host-side Python SDK release focused on customer discoverability and experimentation across the 30 application domains shown in Qubitor's website `index.html`.

## Model input and backend

The two customer input options from SDK 1.2 are preserved:

1. **Option A — model-building API:** binary variables, linear/quadratic objective terms and equality constraints, compiled to a symmetric QUBO.
2. **Option B — direct model input:** symmetric dense/sparse QUBO or Ising fields/couplers, validated and converted before submission.

PUBO remains a host-side representation that is quadratized before QUBO submission. Both model-input routes share the validated QUBO backend interface.

## Example library

The release includes runnable synthetic examples organised into 30 website-aligned domains across Engineering, Medical, Finance and Others. Examples include graph optimisation, portfolio selection, routing, assignment, production scheduling, engineering configuration, semiconductor placement/test, energy, telecommunications, biomedical research toys, AI feature selection, agriculture and sensor-site selection.

The example catalogue is representative, not exhaustive: it does not implement all 384 problem classes displayed on the website and does not claim that every listed domain is a production-ready solver.

## Backends and hardware

- `mock_exact`: small brute-force local backend, up to 24 variables; educational and correctness testing only.
- N=512: dense UART host adapter.
- N=1024: sparse UART host adapter.

Compatible programmed FPGA hardware is supplied separately by Qubitor. This repository excludes FPGA RTL, XDC, Vivado projects, bitstreams, firmware source and confidential hardware implementation files.

## Not implemented

General MILP/MIQP ingestion, arbitrary continuous/general integer variables, inequality constraints in the model builder, general automatic slack modelling, full industrial domain simulators, or domain-specific production data integrations are not claimed. No physical FPGA test is claimed by CPU test results.
