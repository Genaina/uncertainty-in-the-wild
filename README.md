# Uncertainty in the Wild

Repository for the paper: "Uncertainty in the Wild: A Cross-Domain Catalogue of Uncertainty Interactions in Autonomous and Self-Adaptive Systems".

This repository contains the empirical catalogue used in the study, together with the Python analysis pipeline that reproduces the paper's research-question analyses (RQ1–RQ4).

## Overview

The project studies how uncertainty sources interact across autonomous, self-adaptive, cyber-physical, and AI-enabled systems. The main artifact is the case-study catalogue in `artifacts_case_studies_raw.csv`, which records a cross-domain set of scenarios spanning domains such as:

- AI-enabled cloud infrastructure
- automotive systems
- robotics
- healthcare
- smart cities
- aerospace

The repository is organized around two major components:

1. the raw and curated case-study dataset
2. the reproducible analysis scripts in `uip_analysis/`

## Repository structure

```text
uncertainty-in-the-wild/
├── LICENSE
├── README.md
├── artifacts_case_studies_raw.csv
├── uip_analysis/
│   ├── README.md
│   ├── common.py
│   ├── coding.py
│   ├── paper_reported.py
│   ├── rq1.py
│   ├── rq2.py
│   ├── rq3.py
│   ├── rq4.py
│   ├── run_all.py
│   ├── data/
│   │   ├── artifacts_case_studies_raw_ORIGINAL.csv
│   │   ├── artifacts_case_studies_raw_corrected.csv
│   │   └── manual_interaction_counts.csv
│   └── output/
└── ...
```

## Core dataset

The repository includes the following key dataset files:

- `artifacts_case_studies_raw.csv` — primary raw catalogue used in the study
- `uip_analysis/data/artifacts_case_studies_raw_ORIGINAL.csv` — original source export retained for traceability
- `uip_analysis/data/artifacts_case_studies_raw_corrected.csv` — corrected version aligned with the manuscript and analysis workflow
- `uip_analysis/data/manual_interaction_counts.csv` — manually curated counts used as the validation ground truth for RQ1

## Analysis workflow

The analysis code is contained in `uip_analysis/` and implements the paper's quantitative and qualitative analyses:

- `common.py` — shared CSV loading, validation, and helper logic
- `coding.py` — rule-based coding for uncertainty interaction patterns
- `paper_reported.py` — numbers and case lists as originally reported in the paper for validation
- `rq1.py` — dominance/conflict/augmentation/independence analyses and related figures
- `rq2.py` — cross-layer vs. same-level analysis and source/category breakdowns
- `rq3.py` — impact analysis and quality-dimension summaries
- `rq4.py` — preparedness, applicability, lifecycle, trade-offs, and strategy analyses
- `run_all.py` — executes the complete analysis pipeline

## Quick start

To reproduce the analysis locally:

```bash
cd uip_analysis
pip install pandas matplotlib
python run_all.py
```

This script runs the analyses for RQ1–RQ4, prints the report, and writes results into the `output/` folder.

## Data format and schema

The main raw file is a semicolon-delimited CSV because some free-text fields contain semicolons. Each row represents one case study.

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
10. `Level of Preparedness` — detection/representation/mitigation readiness
11. `Applicability Conditions` — contextual conditions for use or mitigation
12. `Lifecycle Stage` — design-time, runtime, or both
13. `Trade-offs` — expected trade-offs of mitigation strategies
14. `Strategy` — detection, reasoning, or mitigation approach

## Interpretation notes

The dataset is intentionally descriptive and exploratory rather than fully normalized. Several cells are free-form text and may contain multiple interacting factors in the same entry. As a result, interpretation often requires reading the full case description rather than relying solely on the column names.

## Intended use

This repository is intended for:

- qualitative analysis of uncertainty interaction patterns,
- cross-domain comparison of uncertainty handling strategies,
- empirical grounding for future models and mitigation approaches,
- and reproducible analysis of the catalogue used in the paper.

## License

This project is distributed under the MIT License. See `LICENSE` for details.

## Repository status

This repository is primarily a research artifact and data catalogue, with a Python-based analysis pipeline for reproducing the paper's findings.
