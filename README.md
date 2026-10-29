# Uncertainty in the Wild

Repository for the paper: "Uncertainty in the Wild: A Cross-Domain Catalogue of Uncertainty Interactions in Autonomous and Self-Adaptive Systems".

## Overview

This repository contains the curated catalogue of uncertainty-interaction exemplars used in the study. The main artifact is the spreadsheet:

- `artifacts_case_studies_raw.csv`

It documents a cross-domain collection of case studies in which multiple sources of uncertainty interact within autonomous, self-adaptive, cyber-physical, and AI-enabled systems.

The catalogue covers domains such as:

- AI-enabled cloud infrastructure
- automotive systems
- robotics
- healthcare
- smart cities
- aerospace

## Purpose of the dataset

The spreadsheet captures the structure and content of the empirical catalog used in the paper. Each row corresponds to one case study and describes:

- the system under study,
- the uncertainty sources involved,
- the interaction type among those sources,
- the abstraction levels involved,
- the likely impact of the interaction,
- the system's preparedness and mitigation strategy,
- and the trade-offs considered.

This dataset supports analysis of how uncertainties are not isolated phenomena, but often interact across levels of abstraction and affect multiple quality attributes simultaneously.

## Data file

### `artifacts_case_studies_raw.csv`

This file is a semicolon-delimited CSV because some free-text fields contain semicolons. Each case is represented as one row.

## Spreadsheet schema

The dataset contains the following columns:

1. `ID`  
   Unique case-study identifier (e.g., `CS1`, `CS2`, ... `CS18`).

2. `Participant(s)`  
   Researchers or contributors associated with the case.

3. `Case Study (Domains)`  
   Domain and system name.

4. `Summary`  
   Short description of the system and the scenario under analysis.

5. `Uncertainty Sources (verbatim)`  
   Free-text description of the uncertainty sources, often including the source type, category, and examples.

6. `Uncertainty Interaction Category`  
   Relationship among uncertainties, such as dominance, conflict, augmentation, or independence.

7. `Uncertainty Nature`  
   The nature of the uncertainty, such as occurrence, behavior, measurement, belief, design, or spatio-temporal.

8. `Abstraction Gap`  
   Whether the uncertainty interaction spans multiple abstraction levels or system layers.

9. `Impact`  
   Consequences of the interaction, such as reliability issues, performance degradation, safety risks, instability, or missed goals.

10. `Level of Preparedness`  
    How prepared the system is to detect, represent, analyze, and mitigate the uncertainty.

11. `Applicability Conditions`  
    Contextual conditions under which the interaction or mitigation is relevant.

12. `Lifecycle Stage`  
    Whether the relevant management strategy is mainly design-time, runtime, or both.

13. `Trade-offs`  
    The expected trade-offs of mitigation or compensation strategies.

14. `Strategy`  
    The detection, representation, analysis, and mitigation approach used in the case.

## Example interpretation

A row may describe, for example:

- a system in automotive or cloud computing,
- multiple uncertainty sources such as sensing noise, stochastic behavior, model drift, or timing delay,
- how one uncertainty amplifies or dominates another,
- and what mitigation strategy is applied or recommended.

## Data quality notes

- The dataset is intentionally exploratory and descriptive rather than fully normalized.
- Several fields are free-form text and may include rich narratives, examples, and multiple interaction types in the same cell.
- Some cells are intentionally left blank in the raw export and should be treated as missing information rather than as values.
- Because of the narrative nature of the catalog, interpretation often requires reading the full text of a case rather than relying only on the column names.

## Intended use

This repository is intended for:

- qualitative analysis of uncertainty interactions,
- cross-domain comparison of uncertainty management patterns,
- empirical grounding for future representation and mitigation models,
- and support for scripts or notebooks that analyze the catalogue.

## Next steps

The next stage will be to define a reproducible analysis script to:

- load the spreadsheet,
- clean and normalize the dataset,
- extract uncertainty categories and interaction patterns,
- and summarize the cross-case evidence behind the paper.

## Repository status

This repository is primarily a research artifact repository and data catalogue, not a software application repository.

