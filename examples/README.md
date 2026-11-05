# Qubitor SDK 2.0 — Example Library

The folders mirror the 30 application domains listed in Qubitor's website `index.html`. Each example is a small, runnable formulation intended to help customers explore how a domain problem can be represented as binary decisions and QUBO interactions.

Run examples from the SDK repository root after installing the package:

```bash
python examples/<path-to-example>.py
```

By default, each example uses `mock_exact` (maximum 24 variables). To submit to a Qubitor board, pass `--backend n512 --port /dev/ttyUSB0` or `--backend n1024 --port COM4` as appropriate. Do not assume every example has been validated on physical hardware.

## Website domain map

### Engineering

| Folder | Example(s) |
|---|---|
| `01_engineering/01_manufacturing_production` | Job-to-machine assignment; single-machine slot scheduling |
| `01_engineering/02_mechanical` | Gear-train ratio and component selection |
| `01_engineering/03_structural` | Structural member option selection |
| `01_engineering/04_thermal` | Cooling configuration |
| `01_engineering/05_fluid` | Pump-valve configuration |
| `01_engineering/06_electrical_electronics` | Circuit component selection |
| `01_engineering/07_semiconductor_design` | Cell placement; test-station assignment |
| `01_engineering/08_rf_microwave_photonics` | Antenna-band configuration |
| `01_engineering/09_robotics_autonomous_systems` | Robot-task allocation |
| `01_engineering/10_aerospace_space_systems` | Satellite-to-target assignment |
| `01_engineering/11_energy_power_systems` | Binary generator commitment toy |
| `01_engineering/12_telecommunications_networks` | Frequency assignment |
| `01_engineering/13_chemical_process_engineering` | Process-train configuration |
| `01_engineering/14_materials_engineering` | Material selection |
| `01_engineering/15_data_centers_hpc` | HPC task-to-node mapping |
| `01_engineering/16_construction_infrastructure` | Crew-to-task assignment |
| `01_engineering/17_network_graph_problems` | Max-Cut, maximum independent set, minimum vertex cover, graph colouring, knapsack |

### Medical

| Folder | Example(s) |
|---|---|
| `02_medical/01_biomedical_pharmaceutical` | Staff shift assignment; synthetic research option selection |
| `02_medical/02_cancer_drug_discovery` | Synthetic compound candidate selection |
| `02_medical/03_precision_oncology` | Synthetic biomarker panel selection |
| `02_medical/04_cancer_treatment` | Synthetic beam-option selection (not a treatment plan) |
| `02_medical/05_cancer_systems_biology` | Synthetic intervention-target selection |

### Finance

| Folder | Example(s) |
|---|---|
| `03_finance/01_portfolio_management` | Cardinality-constrained portfolio; index-tracking asset selection proxy |
| `03_finance/02_trading_execution` | Execution-venue allocation |
| `03_finance/03_banking_treasury` | Liquidity-instrument selection |
| `03_finance/04_financial_operations` | Transaction matching |

### Others

| Folder | Example(s) |
|---|---|
| `04_others/01_logistics_transportation` | Four-city TSP; delivery-job assignment |
| `04_others/02_ai_machine_learning` | Feature selection; model-ensemble selection |
| `04_others/03_agriculture_food_systems` | Crop-to-field allocation |
| `04_others/04_environmental_scientific` | Sensor-site selection proxy |

## Example status and cautions

- These are runnable educational formulations using small synthetic datasets.
- A working toy formulation is not proof that the corresponding industrial workflow is fully modelled.
- Many real-world variants need additional constraints, integer/slack encodings, data pipelines, domain calibration, and independent feasibility checks.
- Medical examples are synthetic research exercises only and must not be used for patient diagnosis or treatment.
- Finance examples are not investment advice and do not replace a full risk model, continuous portfolio construction, transaction-cost model or regulatory review.
- `mock_exact` is exponential-time exhaustive search for models up to 24 variables; it is not a scalable production solver.
