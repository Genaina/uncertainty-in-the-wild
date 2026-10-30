# Uncertainty in the Wild

This repository accompanies the paper submission "Uncertainty in the Wild: A Cross-Domain Catalogue of Uncertainty Interactions in Autonomous and Self-Adaptive Systems".

The project brings together a curated catalogue of cross-domain exemplars of uncertainty interactions in autonomous and self-adaptive systems, along with the analysis scripts used to characterize the catalogue and reproduce the study results. The goal is to make the underlying dataset, the analysis process, and the study findings accessible to researchers and practitioners who want to inspect the evidence, reuse the material, or replicate the reported analysis.

## Why this repository exists

Autonomous and self-adaptive systems must operate under multiple sources of uncertainty arising from their environments, runtime models, adaptation mechanisms, resources, humans, and goals. Although uncertainty management has been widely studied, uncertainty sources are often considered in isolation, even though practical systems frequently exhibit dependencies in which the presence or treatment of one uncertainty affects another.

This repository provides the catalogue and the analysis workflow supporting the study of these interactions across domains such as AI-enabled cloud infrastructures, automotive systems, robotics, healthcare, smart cities, and aerospace. It is intended as a reusable artifact for exploring the collected exemplars, understanding how uncertainty interactions are characterized, and reproducing the analysis reported in the paper.

## Repository structure

- `uip_analysis/` — main analysis package containing the raw catalogue data, coding logic, statistical scripts, and outputs used to reproduce the study.
- `LICENSE` — project license.

Within `uip_analysis/`, you will find the scripts used to run the analysis, including:

- `run_all.py` — executes the full analysis pipeline.
- `rq1.py` to `rq4.py` — individual scripts for the paper's research questions.
- `data/` — the dataset used in the study.
- `output/` — generated tables, figures, and reports.

## How to use this repository

The repository is intended for two main purposes:

1. To inspect the catalogue of uncertainty-interaction exemplars and their characterization.
2. To reproduce the analysis workflow described in the paper.

For reproduction, the analysis scripts are located in the `uip_analysis` directory. From there, you can create a virtual environment, install the dependencies, and run the study.

## Quick start

```bash
cd uip_analysis
python3 -m venv .venv
source .venv/bin/activate    # On Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python run_all.py
```

This will run the analysis pipeline and generate the outputs in `uip_analysis/output/`.

You can also run the research-question-specific scripts directly:

```bash
python rq1.py
python rq2.py
python rq3.py
python rq4.py
```

## Notes

- The analysis is designed to be run from inside the `uip_analysis` directory.
- The project uses Python 3.9 or newer.
- The generated report and associated files are stored in `uip_analysis/output/`.

## Citation / paper context

The repository supports the TAAS paper submission entitled "Uncertainty in the Wild: A Cross-Domain Catalogue of Uncertainty Interactions in Autonomous and Self-Adaptive Systems." The accompanying analysis synthesizes the catalogue into a structured set of observations about uncertainty interaction types, abstraction spans, impacts, and mitigation strategies.

The paper's findings show that uncertainty interactions are commonly heterogeneous, often cross levels of system description, and typically affect multiple system qualities. The catalogue and cross-case synthesis are intended to support researchers and practitioners in recognizing and managing interaction risks and in guiding future representations, analysis techniques, and mitigation approaches.
