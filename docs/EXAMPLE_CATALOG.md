# SDK 2.0 example catalogue and modelling boundaries

This catalogue follows the 30 domains exposed in the Qubitor website `index.html`. The examples demonstrate representative binary-decision formulations. They do not claim to cover all 384 problem classes listed by the website or to be production-validated domain solvers.

| Website family | Domain | Example formulation | Current boundary |
|---|---|---|---|
| Engineering | Manufacturing & Production | Job-machine assignment; one-machine slot scheduling | No general job-shop, sequence-dependent setup, calendars or multi-resource constraints |
| Engineering | Mechanical | Component and gear-ratio selection | Small discrete design choices; no continuous mechanics simulation |
| Engineering | Structural | Member-option selection | Not structural analysis, stress certification or code compliance |
| Engineering | Thermal | Cooling configuration selection | Not CFD or coupled thermal simulation |
| Engineering | Fluid | Pump-valve configuration | Not fluid dynamics or hydraulic network simulation |
| Engineering | Electrical & Electronics | Circuit component selection | Not SPICE, analog design or circuit verification |
| Engineering | Semiconductor Design | Cell placement; test-station assignment | Small assignment proxies, not full place-and-route or fab scheduling |
| Engineering | RF, Microwave & Photonics | Antenna-band configuration | Not electromagnetic simulation or full beamforming |
| Engineering | Robotics & Autonomous Systems | Robot-task allocation | Not motion planning, collision avoidance or real-time control |
| Engineering | Aerospace & Space Systems | Satellite-target assignment | Not orbital mechanics, attitude control or mission certification |
| Engineering | Energy & Power Systems | Binary generator commitment toy | Exact small demand equality; not full unit commitment, ramping, reserves or network constraints |
| Engineering | Telecommunications & Networks | Frequency assignment | Small interference graph; no propagation model or spectrum regulation |
| Engineering | Chemical & Process Engineering | Process-train configuration | Not process simulation, safety analysis or continuous operating-point optimisation |
| Engineering | Materials Engineering | Material selection | Not materials discovery or physical property prediction |
| Engineering | Data Centers & HPC | Task-to-node mapping | Small static mapping; no full scheduling, memory, network or thermal model |
| Engineering | Construction & Infrastructure | Crew-task assignment | Not full project scheduling with precedence, calendars and resource levelling |
| Engineering | Network & Graph Problems | Max-Cut, MIS, minimum vertex cover, graph colouring, knapsack | Small canonical examples; graph colouring uses a fixed colour count |
| Medical | Biomedical & Pharmaceutical | Staff scheduling; synthetic option selection | Operational toy only; no patient-care decision support |
| Medical | Cancer Drug Discovery | Synthetic compound selection | No molecular docking, chemistry, ADMET or biological evidence |
| Medical | Precision Oncology | Synthetic biomarker panel selection | No diagnostic validity or patient data |
| Medical | Cancer Treatment | Synthetic beam-option selection | Not dose calculation, radiotherapy optimisation or a treatment plan |
| Medical | Cancer Systems Biology | Synthetic intervention-target selection | No validated biological network or causal inference |
| Finance | Portfolio Management | Cardinality-constrained selection; index-tracking proxy | Binary/equal-weight toy, not continuous Markowitz optimisation or live market research |
| Finance | Trading & Execution | Execution-venue allocation | No order-book simulation, latency, market impact or broker integration |
| Finance | Banking & Treasury | Liquidity-instrument selection | Synthetic discrete liquidity target; no ALM, regulatory capital or risk model |
| Finance | Financial Operations | Transaction matching | Synthetic one-to-one matching; no production reconciliation or fraud controls |
| Others | Logistics & Transportation | Four-city TSP; delivery assignment | Not full capacitated VRP, time windows, pickup-delivery or fleet routing |
| Others | AI & Machine Learning | Feature and ensemble selection | Synthetic scores; not an end-to-end ML pipeline |
| Others | Agriculture & Food Systems | Crop-field allocation | Synthetic profit; no agronomy, weather, soil or water model |
| Others | Environmental & Scientific | Sensor-site selection proxy | Synthetic site scores; not a validated coverage, field or scientific measurement model |

## Formulation conventions

- Binary decision variable: `x_i ∈ {0,1}`.
- Objective: minimise `offset + xᵀQx`, with symmetric `Q`.
- Model-builder equality constraint: encoded as a positive penalty `P(lhs-rhs)^2`.
- Direct QUBO: matrix must be square, finite and symmetric; asymmetric inputs are rejected.
- Direct Ising: fields `h_i`, couplers `J_ij`, spins `s_i ∈ {-1,+1}`; SDK converts to symmetric QUBO.
- PUBO is host-side and quadratized before backend submission; the FPGA backend receives QUBO, not native higher-order terms.

## How to extend an example responsibly

1. Replace the synthetic values with real, permissioned, validated input data.
2. Write down the original business objective and every hard constraint before translating it.
3. Decide which constraints can be represented as equalities and which require explicit slack-variable or alternative encodings.
4. Select and justify penalty magnitudes; test whether feasible solutions remain preferred over infeasible ones.
5. Recompute the original objective and check all constraints from the returned bitstring.
6. Compare against an appropriate classical baseline and multiple random seeds.
7. Only then evaluate the model on a Qubitor FPGA; record coefficient scale, variable count, nonzero count, runtime and solution quality.

Do not treat the CPU `mock_exact` backend as evidence of FPGA speed or scalability. Do not treat a synthetic example as a validated domain application.
