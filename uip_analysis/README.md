# Reproducing the RQ1–RQ4 analysis of "Uncertainty in the Wild"

This package reproduces the cross-case analysis (Sections 6.1–6.4) of the paper *Uncertainty in the Wild: A Cross-Domain Catalogue of
Uncertainty Interactions in Autonomous and Self-Adaptive Systems*. It takes the catalogue of 18 uncertainty-interaction exemplars
(CS1–CS18), computes the frequencies, tables and figures of each research question (RQ1–RQ4), and prints the verbatim text that supports the
codes and assignments behind them.

## Quick start
Requirements: Python 3.9 or newer and `git`. The steps use a virtual environment, which works on macOS, Linux and Windows and avoids the
`externally-managed-environment` error raised by system-managed Python installations (e.g., Homebrew).

```bash
python3 -m venv .venv                          # create the environment (once)
source .venv/bin/activate                      # activate it (Windows PowerShell: .venv\Scripts\Activate.ps1)
python -m pip install -r requirements.txt      # install pandas and matplotlib (once)
python run_all.py                              # run RQ1..RQ4: prints the report and writes everything to output/
```
- Run the commands **from inside the `uip_analysis` folder**. After activation the prompt starts with `(.venv)`; from then on use `python`
  and `python -m pip` (not `python3`/`pip`) so that the packages and the interpreter always match.
- In later sessions only `source .venv/bin/activate` and `python run_all.py` are needed.
- A single research question can be run on its own: `python rq1.py` (… `rq4.py`).
- `ModuleNotFoundError: No module named 'pandas'` means the environment is not activated (or the install step was skipped).
  Check with `python -m pip show pandas`.
- Output: `output/full_report.txt` holds the complete printed report, and every table is also saved as a CSV (plus two PNG figures) in `output/`.

## Package layout
| Path | Content |
|---|---|
| `data/artifacts_case_studies_raw.csv` | The catalogue: one row per exemplar with the contributors' verbatim answers to the characterisation template |
| `data/manual_interaction_counts.csv` | Manual coding of the interaction categories per exemplar (used by RQ1) |
| `requirements.txt` | Python dependencies (pandas, matplotlib) |
| `common.py` | CSV loading, domain map (Table 3 / Fig. 1) and small formatting helpers |
| `coding.py` | Rule-based coding of the verbatim fields (follows the operational coding rules of Section 3.4) |
| `analyst_assignments.py` | The case assignments of the analyst-derived tables (Tables 7, 9, 10, 11), used as input; the scripts show the text that supports each one |
| `rq1.py` … `rq4.py` | One script per research question |
| `run_all.py` | Runs the four scripts in order |

## Input data
**`artifacts_case_studies_raw.csv`** — separator `;`, encoding cp1252. Columns: `ID`, `Participant(s)`, `Case Study (Domains)`, `Summary`,
and the template fields `Uncertainty Sources (verbatim)`, `Uncertainty Interaction Category`, `Uncertainty Nature`, `Abstraction Gap`,
`Impact`, `Level of Preparedness`, `Applicability Conditions`, `Lifecycle Stage`, `Trade-offs`, `Strategy`.
The *problem space* (sources, interaction category, nature, abstraction gap, impact) feeds RQ1–RQ3; the *solution space*
(preparedness, applicability, lifecycle, trade-offs, strategy) feeds RQ4. Empty or "not provided" fields are treated as
**missing information, never as negative evidence** (Section 3.4).

**`manual_interaction_counts.csv`** — columns `ID, conflict, dominance, augmentation, independence, template_only`.
Each value is the number of documented interaction instances of that category in the exemplar; a category counts once per exemplar
when the value is ≥ 1 (Section 3.4, rule 1). Coding protocol, applied to the verbatim `Uncertainty Interaction Category` text:
- a category is coded when the text describes it for the case; tentative marks such as `(?)` or `(Possible)` are coded;
- a word such as "(dominant)" attached to another label is not a separate category; answers marked "N/A" are not coded;
- `template_only = 1` flags the four exemplars (CS4, CS7, CS8, CS14) whose interaction field contains only the template definitions:
  the categories whose labels appear in the template answer are counted as coded, and `rq1.py` also prints the counts without them
  as a sensitivity check.

**Primary domain.** Each exemplar has one primary domain (Table 3, six domains: Automotive, IT/Cloud, Robotics, Healthcare, Smart City, Aerospace),
defined by the type of system under study rather than by its deployment context. CS5 (a hospital service robot with a human in the loop)
is tagged `Healthcare/Robotics` in the CSV and counted as Robotics.

## Results at a glance (what a correct run prints)
| RQ | Result |
|---|---|
| RQ1 | Dominance 11/18, conflict 14/18, augmentation 14/18, independence 4/18; heterogeneous interactions 16/18 |
| RQ2 | Cross-layer 14/18, same/partial level 4/18 (CS4, CS6, CS7, CS10) |
| RQ3 | Multi-dimensional impact 15/18, generic/template 3/18 (CS8, CS10, CS14) |
| RQ4 | Counts per preparedness dimension, strategy category and lifecycle stage printed from the parsed text (see below) |

## What each script computes

### RQ1 — What types of uncertainty interactions are observed? (`rq1.py`, Section 6.1)
1. **Domain distribution** (Fig. 1).
2. **Interaction categories** (dominance, conflict, augmentation, independence), counted per exemplar from `manual_interaction_counts.csv`,
   in total (Section 6.1.1) and per domain (Fig. 3). As a cross-check, `coding.py` codes the verbatim text automatically under three criteria:
   *strict* (explicit evidence only), *lenient* (+ tentative marks such as `(?)`), *full* (+ template-only answers); the script reports whether the
   automatic rule reproduces the manual coding. The *full* criterion reproduces the manual coding exactly (11/14/14/4); *strict* and *lenient* show how many
   category codes rest on explicit case-specific text (6/10/9/1 and 8/10/10/1), the difference being the four template-only exemplars.
   The report then prints an **evidence section**: for every category, the cases counted, split into *explicit text*, *tentative mark* and *template-only*, with the
   verbatim excerpt that supports each code, and it confirms that the manual coding is fully explained by these three layers (`rq1_interaction_evidence.csv` holds the full excerpts).
3. **Interaction nature** (Section 6.1.2, Table 4): an exemplar is *heterogeneous* unless its `Uncertainty Nature` field says homogeneous.

Outputs: `rq1_domain_distribution.csv`, `rq1_category_counts.csv`, `rq1_manual_flags.csv`, `rq1_category_by_domain.csv`, `rq1_nature_by_domain.csv`,
`rq1_interaction_coding_per_case.csv`, `rq1_interaction_evidence.csv`, `rq1_fig_domains.png`, `rq1_fig_categories.png`.

### RQ2 — Which sources, abstraction levels and causal mechanisms participate? (`rq2.py`, Section 6.2)
1. **Abstraction span** (Section 6.2.1, Table 5): *same/partial level* when the `Abstraction Gap` field says "same" or is empty, *cross-layer* otherwise.
2. **Uncertainty sources** (Section 6.2.2): frequency of source *categories* (model, adaptation functions, goals, environment, resources, human) and *types*
   (measurement, occurrence, design, behavior, belief, spatio-temporal) by keyword search over `Uncertainty Sources (verbatim)`, plus the most frequent co-occurring category pairs.
3. **Causal mechanisms** (Section 6.2.3): propagation, amplification, dominance and trade-off/conflict are searched by keyword in the interaction, impact,
   trade-off and abstraction fields, and the cases that show each mechanism are listed.

Outputs: `rq2_abstraction_by_domain.csv`, `rq2_source_categories_per_case.csv`, `rq2_source_types_per_case.csv`, `rq2_source_counts.csv`, `rq2_mechanisms_per_case.csv`.
Items 2 and 3 are **keyword heuristics**: they quantify what the verbatim text supports and do not replace the qualitative reading in the paper.

### RQ3 — What operational impacts are associated with the interactions? (`rq3.py`, Section 6.3)
1. **Impact characterisation** (Section 6.3.1, Table 6): *generic/template* when the `Impact` field is explicitly marked as generic or template text, *multi-dimensional* otherwise (Section 3.4, rule 4).
2. **Affected quality dimensions** (Section 6.3.2, Table 7): safety, performance, reliability & availability, mission success, human factors & trust, resource efficiency/cost.
   Table 7 is an analyst reading of each exemplar, so the script does not recompute it. For every case assigned to a dimension it shows the supporting text:
   the `Impact` field itself (primary evidence) or the `Trade-offs` / `Summary` fields (secondary evidence), and it reports how many assigned cases are supported by the `Impact` field alone and by any field.

Outputs: `rq3_impact_coding_per_case.csv`, `rq3_impact_class_by_domain.csv`, `rq3_quality_dimensions.csv`, `rq3_quality_dimension_evidence.csv`.

### RQ4 — Which mechanisms address the interactions, and under what conditions? (`rq4.py`, Section 6.4)
1. **Preparedness** (Table 8): the `Level of Preparedness` text is split on the labels Awareness, Prevention, Detectability, Representation, Comprehension (= Understanding) and Mitigation;
   a capability is *reported* when its segment has non-empty, non-negative content ("Limited"/"Partial" count as partial capability; "cannot…", "unknown" and "(blank)" do not).
2. **Strategy** (Table 12): the `Strategy` field is split on Detection / Representation / Analysis / Mitigation; entries such as "unknown" or "blank" are not counted.
3. **Tables 8 and 12**: for every dimension the script lists the cases that report it, each with the supporting entry of the verbatim text.
4. **Lifecycle stage** (Section 6.4.3): design-time, runtime or both, from the `Lifecycle Stage` field. Table 10 (lifecycle activities) is analyst-derived; its case counts are only printed.
5. **Applicability conditions** (Table 9) and **trade-offs** (Table 11): these categories are assigned by the analyst, so for every assigned case the script shows the excerpt of the `Applicability Conditions` /
   `Trade-offs` field that supports the assignment, and reports any assigned case without supporting text.
6. **Coverage**: how many of the solution-space fields each exemplar filled in (relevant for the threats to validity).

Outputs: `rq4_preparedness_per_case.csv`, `rq4_strategy_per_case.csv`, `rq4_lifecycle_per_case.csv`, `rq4_solution_space_coverage.csv`,
`rq4_table8_cases.csv`, `rq4_table12_cases.csv`, `rq4_table8_12_evidence.csv`, `rq4_table9_evidence.csv`, `rq4_table11_evidence.csv`.

## How to read the report
- **RQ1–RQ3 problem-space results** (interaction categories, heterogeneity, abstraction span, impact class and their per-domain tables and figures) are fully determined by the data and the coding rules.
  For the interaction categories the report also prints the supporting excerpt of every code.
- **Tables 8 and 12 (RQ4)** are computed by parsing the labelled entries of the verbatim answers; each case listed under a dimension is shown with the entry that supports it.
  A case whose answer has no labelled entry for a dimension (for example, an answer written as a single sentence) is not listed for that dimension.
  The paper additionally credits a capability from the `Strategy` entries when the preparedness answer does not state it (Section 6.4.1): CS5 describes its preparedness in a single sentence, so its awareness,
  detectability, representation and understanding are credited from its strategy entries, and CS4, whose preparedness answer states that the uncertainty cannot be modeled, is credited with representation from its strategy.
  These are the only cases of Table 8 that the label-based parse does not list.
- **Tables 7, 9, 10 and 11** are analyst readings of the exemplars. The assignments are an input (`analyst_assignments.py`); the report shows the text that supports each assigned case.
- Keyword-based results (source categories and types, causal mechanisms) show what the verbatim text supports and do not replace the qualitative reading in the paper.

## Limitations
The exemplars are purposively sampled contributor descriptions, so frequencies describe the catalogue and not the wider population of systems (Section 7).
Several fields were answered in free text with varying detail; the rule-based coders are deliberately conservative, and the manual coding of the interaction categories is the reference for RQ1.
