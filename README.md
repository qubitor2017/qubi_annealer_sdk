# Qubitor SDK 2.0.0 — Industry Example Release

**A host-side Python SDK and an industry-organised example library for QUBO / Ising optimisation on Qubitor FPGA hardware.**

The SDK is designed so a developer, researcher, operations team or domain specialist can start with a small example, inspect its binary-variable model, change the data and coefficients, and then run the same formulation locally or submit it to a compatible Qubitor FPGA.

> **Hardware is supplied separately by Qubitor.** This public SDK contains host-side software only. It does not contain FPGA RTL, XDC constraints, Vivado projects, bitstreams, firmware source or confidential hardware implementation files.

## What's new in 2.0.0

- Preserves both customer model-input options from SDK 1.2:
  - **Option A — model builder:** binary variables, linear/quadratic objective terms and equality constraints compiled to symmetric QUBO.
  - **Option B — direct input:** symmetric dense/sparse QUBO or Ising fields/couplers, validated and converted before backend submission.
- Preserves PUBO host-side representation and Rosenberg quadratization.
- Preserves N=512 dense and N=1024 sparse UART host adapters.
- Preserves the small exact CPU mock backend for local learning and correctness checks.
- Adds an industry-organised catalogue following the 30 application domains in Qubitor's website `index.html`.
- Includes **40+ runnable industry examples** with small synthetic inputs and decoded output.
- Every example defaults to `mock_exact`; hardware submission is explicit.

## Quick install

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

For CPU-only modelling without UART support, use `python -m pip install -e .`.

## Run your first examples

From the repository root:

```bash
# Both model input options
python examples/00_getting_started/01_two_model_input_options.py

# Option A — model-building API
python examples/00_getting_started/02_option_a_model_builder.py

# Option B — direct symmetric QUBO
python examples/00_getting_started/03_option_b_direct_qubo.py

# Option B — direct Ising coefficients
python examples/00_getting_started/04_option_b_ising.py

# Industry example — Max-Cut
python examples/01_engineering/17_network_graph_problems/01_maxcut.py

# Industry example — portfolio selection
python examples/03_finance/01_portfolio_management/01_cardinality_constrained_portfolio.py
```

Each industry example accepts:

```bash
--backend mock_exact
```

For a compatible Qubitor board, use an explicit hardware backend and serial port:

```bash
python examples/01_engineering/17_network_graph_problems/01_maxcut.py \
  --backend n512 --port /dev/ttyUSB0

# Windows example
python examples/01_engineering/17_network_graph_problems/01_maxcut.py \
  --backend n1024 --port COM4
```

Use only a Qubitor-supplied compatible FPGA/bitstream and the hardware setup instructions provided with it. N=512 and N=1024 use different UART protocols and memory layouts.

## Industry example catalogue

The folder hierarchy mirrors the 30 domains in the Qubitor website:

| Website family | Domain folders | Example themes |
|---|---:|---|
| Engineering | 17 | manufacturing scheduling, mechanical configuration, structural selection, thermal/fluid systems, electronics, semiconductor placement/test, RF, robotics, aerospace, energy, telecom, chemical processes, materials, data-centre/HPC, construction, graph optimisation |
| Medical | 5 | biomedical resource scheduling, compound selection, biomarker panels, beam-option research, systems-biology target selection |
| Finance | 4 | cardinality-constrained portfolio selection, index-tracking selection, execution venue allocation, treasury liquidity, transaction matching |
| Others | 4 | TSP and delivery assignment, AI feature/ensemble selection, crop allocation, sensor-site selection |

See [`examples/README.md`](examples/README.md) for the complete folder map and [`docs/EXAMPLE_CATALOG.md`](docs/EXAMPLE_CATALOG.md) for each example's modelling assumptions and limitations.

## How the examples work

Most examples use the Option A model builder:

```python
import qubitor

m = qubitor.Model("choose_two")
x = m.binary_vars("asset", 4)
m.minimize(2*x[0] + x[1] + 3*x[2] + x[3])
m.add_constraint(sum(x) == 2, name="select_exactly_two")

qubo = qubitor.compile(m, penalty=10.0)
result = qubitor.solve(qubo, backend="mock_exact")
print(result.solution, result.objective)
```

Option B remains available when the customer already has a QUBO matrix or Ising coefficients:

```python
qubo = qubitor.from_qubo([[-2.0, 0.5], [0.5, -1.0]])
result = qubitor.solve(qubo, backend="mock_exact")
```

The SDK uses the same validated QUBO backend path for both options.

## Backend limits and coefficient scaling

- `mock_exact`: exhaustive enumeration, maximum 24 variables. It is for small examples and correctness checks, not a performance benchmark.
- `n512`: dense QUBO interface, up to 512 binary variables. The current adapter checks signed 16-bit coefficient storage after scaling.
- `n1024`: sparse QUBO interface, up to 1,024 binary variables, with a maximum of 65,535 directed matrix entries in this adapter.
- FPGA coefficients are quantised using `round(coefficient * scale)`. Choose a scale that preserves useful precision without overflow.
- The FPGA returns a candidate solution. Recompute the original objective and verify every original constraint in the customer application.

## Important modelling limits

This release is an **industry example library**, not a claim that every problem in every domain is already a production-ready solver.

- Option A supports binary variables, linear/quadratic objectives and equality constraints.
- Inequalities, continuous/general integer variables, automatic slack-variable modelling and general MILP/MIQP ingestion are not implemented.
- Some examples use explicit binary slack variables or problem-specific penalty terms; these are visible in the source.
- TSP is a small permutation model, not a complete capacitated VRP with time windows, driver rules and fleet constraints.
- The manufacturing scheduling examples are small assignment/slot models, not general job-shop scheduling.
- Portfolio examples are binary selection / equal-weight proxies, not continuous Markowitz optimisation or investment advice.
- Medical/oncology examples use synthetic values for optimisation education only. They are not diagnostic, drug-discovery evidence, treatment plans or clinical recommendations.
- All example inputs are synthetic. Replace them with validated domain data and obtain domain-expert review before operational use.

## Tests

```bash
python -m unittest discover -s tests -v
```

Tests run on the CPU mock backend and do not validate a physical FPGA, a particular bitstream, UART wiring or hardware revision.

## License and distribution

This is source-available proprietary software from Qubitor Labs. Public visibility of the repository does not grant permission to redistribute, sublicense, modify for third-party distribution, or use commercially beyond the rights expressly granted by a separate Qubitor SDK licence/EULA. Approve the final customer licence before public release. This README is not legal advice.

Website: https://www.qubitor.com  
GitHub: https://github.com/qubitor2017/qubitor-sdk  
Contact: info@qubitor.com
