# Introduction

This repository contains all software, data, models that are used for the Paper:

> **Process Mining for Intrusion Detection in Cybersecurity: A Conformance-based Point of View**

The work is based on:

This repository contains the software artifacts implemented during the master’s thesis carried out by **Emil Løvstrand Mortensen** and **Emil Pontoppidan Rasmussen**.

For further information, we encourage reading the thesis titled:

> **Modeling and Simulating Attacks with Process Mining for Cybersecurity Research**

# Abstract 
Cybersecurity threats are increasing as digital systems grow in scale and complexity. Detailed system monitoring logs provide an important source of evidence for detecting breaches and understanding attacker behavior. In practice, however, compromised-system logs are scarce and difficult to analyze. Formal process models offer a structured representation of system behavior, enabling explicit reasoning about benign and malicious activity. This thesis aimed to investigate whether process mining and formal representation of models can be used in the context of cybersecurity to model and analyze benign and malicious behavior in a more flexible way than analyzing the actual compromised system. This was achieved by modeling benign \textit{Windows} system behavior in two ways: manual modeling and automated modeling using process mining techniques. Attacks inspired by the \textit{MITRE ATT\&CK} framework were then injected to obtain attack models, which supported simulation and classification of behavior. The realism of the models was validated using conformance checking and behavioral analysis. The models and simulated logs exhibit high conformance with observed behavior, indicating substantial realism of the obtained models, and the classification results are promising, as the approach detects and classifies attacks.

# How to Run Code

## VM Script Generation and Execution Tool

### Generate PowerShell Scripts

CLI template for generating a set of random *PowerShell* scripts. The command takes the number of scripts to generate as a required argument (`--n`) and optionally accepts a random seed (`--seed`) to make the generation process reproducible. This fills an existing folder with *n* scripts.

```bash
python -m Scripts.Phase_2.generate_scripts \
  --n <NUM_SCRIPTS> \
  --seed <RANDOM_SEED>
```

### Execute All Generated PowerShell Scripts

CLI template for running all scripts in the folder filled using the script generation command. The command executes each generated *PowerShell* script sequentially and applies an optional fixed delay between runs. After execution, the resulting `EVTX` file can be collected from the machine for analysis.

```bash
python -m Scripts.Phase_2.script_runner \
  --delay <SECONDS_BETWEEN_RUNS>
```

## EVTX to XES Transformation

CLI template for transforming an *EVTX* file into *XES* format via an intermediate *CSV* file. The command takes the input *EVTX* file via `--evtx`, the path for the intermediate *CSV* output via `--csv-out`, and the path for the final *XES* output via `--xes-out`.

```bash
python -m Scripts.Phase_2.evtx_to_xes.evtx2xes \
  --evtx "<INPUT_EVTX_FILE>" \
  --csv-out "<OUTPUT_CSV_FILE>" \
  --xes-out "<OUTPUT_XES_FILE>"
```

## Discovery Pipeline

CLI template for using the discovery pipeline. The command takes an input *XES* file as a positional argument and accepts space-separated parameter lists via `--variant_params`, `--dependency_params`, `--and_params`, and `--loop_params`, which correspond to the common parameters of the *PM4PY* implementation of the *Heuristic Miner*. The output is the *PNML* file for which the Petri net achieves the best *fitness* and *precision* scores while containing the highest number of transitions (excluding silent transitions).

```bash
python -m ModelDiscovery.model_discovery_pipeline "<XES_FILE>" \
  --variant_params <VAR_1> <VAR_2> <VAR_3> <...> \
  --dependency_params <DEP_1> <DEP_2> <DEP_3> <...> \
  --and_params <AND_1> <AND_2> <AND_3> <...> \
  --loop_params <LOOP_1> <LOOP_2> <LOOP_3> <LOOP_4> <...>
```

## Validation Framework

CLI template for obtaining *fitness* and *precision* scores. The command takes a *PNML* file and an *XES* file as positional arguments. The result consists of the computed *fitness* and *precision* metrics.

```bash
python -m Scripts.Validation.fitness_and_precision "<PNML_FILE>" "<XES_FILE>"
```

## Detection Framework

CLI template for the detection framework. It takes input lists of *PNML* files and *XES* files. The result is the conformance table.

```bash
python -m Scripts.Validation.conformance_table \
  --pnml <PNML_FILE_1> <PNML_FILE_2> ... <PNML_FILE_N> \
  --xes <XES_FILE_1> <XES_FILE_2> ... <XES_FILE_N>
```

## Simulation Framework and Probability Miner

### Generate Blank Config Structure

CLI template for generating an empty configuration structure, allowing the user to manually specify probabilities for each *place-transition* arc. The command takes a *PNML* file and an output directory for the generated configuration structure.

```bash
python -m Scripts.Simulation.generate_config_structure \
  --pnml "<PNML_FILE>" \
  --config-out "<CONFIG_OUTPUT_DIR>"
```

### Generate Config and Fill Probabilities

CLI template for generating a configuration structure, where the *probability miner* injects probabilities for each *place-transition* arc for which a probability is found. The command takes a *PNML* file, an output directory for the generated configuration structure, and an *XES* file used by the probability miner.

```bash
python -m Scripts.Simulation.generate_config_structure \
  --pnml "<PNML_FILE>" \
  --config-out "<CONFIG_OUTPUT_DIR>" \
  --prob-xes "<XES_FILE>"
```

### Simulate Benign Traces from a Generated Config

CLI template for simulating a Data Petri net using the *LOGPPL* integration. The command takes a filled configuration file, the number of steps for a simulation, and the number of traces to simulate. The output is an *XES* file containing the simulated traces.

```bash
python -m Scripts.Simulation.simulate_data_petrinet \
  --config "<CONFIG_JSON>" \
  --steps <NUM_STEPS> \
  --sample-size <SAMPLE_SIZE>
```

### Simulate Attack Traces from a Generated Config

CLI template for simulating a Data Petri net using the extension of *LOGPPL*. The command takes a filled configuration file, the number of simulation steps, and the number of traces to simulate, and additionally accepts an attack type. The `--attacktype` argument selects the predicate-based attack behavior to inject during simulation, with supported values `Composite`, `Redflag`, `Repeat`, and `4th` (where *4th* refers to the *Password Filter DLL* attack).

```bash
python -m Scripts.Simulation.simulate_data_petrinet \
  --config "<CONFIG_JSON>" \
  --steps <NUM_STEPS> \
  --sample-size <SAMPLE_SIZE> \
  --attacktype <Composite|Redflag|Repeat|4th>
```
