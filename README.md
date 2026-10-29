# Uncertainty in the Wild

Repository for the paper: "Uncertainty in the Wild: A Cross-Domain Catalogue of Uncertainty Interactions in Autonomous and Self-Adaptive Systems".

This repository contains the empirical catalogue used in the study and a Python-based analysis pipeline for reproducing the paper's research-question analyses (RQ1–RQ4).

## Overview

The project studies how uncertainty sources interact across autonomous, self-adaptive, cyber-physical, and AI-enabled systems. The main artifact is the case-study catalogue stored in `uip_analysis/data/`, together with the scripts that compute the reported frequencies, comparisons, and figures.

The catalogue spans multiple domains, including:

- AI-enabled cloud infrastructure
- automotive systems
- robotics
- healthcare
- smart cities
- aerospace

## Repository structure

```text
uncertainty-in-the-wild/
├── LICENSE
├── README.md
├── uip_analysis/
│   ├── README.md
│   ├── README_uip_analysis.md
│   ├── common.py
│   ├── coding.py
│   ├── paper_reported.py
│   ├── rq1.py
│   ├── rq2.py
│   ├── rq3.py
│   ├── rq4.py
│   ├── run_all.py
│   ├── data/
│   │   ├── artifacts_case_studies_raw.csv
│   │   └── manual_interaction_counts.csv
│   └── output/
└── ...
```

## Core dataset

The repository includes the following main data files in `uip_analysis/data/`:

- `uip_analysis/data/artifacts_case_studies_raw.csv` — main raw case-study catalogue used in the study
- `uip_analysis/data/manual_interaction_counts.csv` — manually curated interaction counts used as the validation reference for RQ1

Each row represents a case study or exemplar, with fields describing uncertainty sources, interaction types, impacts, lifecycle stage, mitigation strategies, and more.

## Analysis workflow

The analysis code in `uip_analysis/` reproduces the paper's quantitative and qualitative findings:

- `common.py` — shared CSV loading and helper logic
- `coding.py` — rule-based coding for uncertainty interaction patterns
- `paper_reported.py` — numbers and case lists reported in the paper for validation
- `rq1.py` — interaction categories and cross-domain distributions
- `rq2.py` — uncertainty sources, abstraction gaps, and causal mechanisms
- `rq3.py` — impact characterisation and quality-dimension analysis
- `rq4.py` — preparedness, strategy, lifecycle, applicability, and trade-offs
- `run_all.py` — runs the complete analysis pipeline

## Quick start

To reproduce the analysis locally:

```bash
cd uip_analysis
pip install pandas matplotlib
python run_all.py
```

This script runs the analyses for RQ1–RQ4, prints the validation report, and writes the results into the `output/` folder.

## Data format and schema

The main raw catalogue file uses semicolon-delimited CSV format, since some free-text cells contain semicolons. Each row corresponds to one case study.

The catalogue includes fields such as:

1. `ID` — unique case-study identifier
2. `Participant(s)` — contributors or researchers associated with the case
3. `Case Study (Domains)` — domain and system under study
4. `Summary` — short description of the scenario
5. `Uncertainty Sources (verbatim)` — detailed description of uncertainty sources
6. `Uncertainty Interaction Category` — relationship among uncertainties
7. `Uncertainty Nature` — type of uncertainty involved
8. `Abstraction Gap` — whether the interaction spans abstraction levels
9. `Impact` — consequences of the uncertainty interaction
10. `Level of Preparedness` — awareness, detection, representation, and mitigation readiness
11. `Applicability Conditions` — contextual conditions for use or mitigation
12. `Lifecycle Stage` — design-time, runtime, or both
13. `Trade-offs` — expected trade-offs of mitigation strategies
14. `Strategy` — detection, reasoning, or mitigation approach

## Interpretation notes

The dataset is intentionally descriptive and exploratory rather than fully normalized. Several cells contain free-form text, and some entries include multiple interacting factors in the same field. The repository therefore combines raw catalogue data with rule-based coding and validation scripts rather than relying on a single fully normalized schema.

## Intended use

This repository is intended for:

- qualitative analysis of uncertainty interaction patterns,
- cross-domain comparison of uncertainty handling strategies,
- empirical grounding for future models and mitigation approaches,
- reprodcible analysis of the catalogue used in the paper.

## Citation

If you use this repository or its analysis in your work, please cite the associated paper:

> Uncertainty in the Wild: A Cross-Domain Catalogue of Uncertainty Interactions in Autonomous and Self-Adaptive Systems.

## License

This project is distributed under the MIT License. See `LICENSE` for details.

## Repository status

This repository is primarily a research artifact and data catalogue, with a Python-based analysis pipeline for reproducing the paper's findings.
