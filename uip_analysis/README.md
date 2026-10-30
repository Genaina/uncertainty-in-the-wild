# Reproducing the RQ1–RQ4 analysis of "Uncertainty in the Wild"

This package reproduces the cross-case analysis (Sections 6.1–6.4) of the paper *Uncertainty in the Wild: A Cross-Domain Catalogue of
Uncertainty Interactions in Autonomous and Self-Adaptive Systems*. It takes the catalogue of 18 uncertainty-interaction exemplars
(CS1–CS18), computes the frequencies, tables and figures of each research question (RQ1–RQ4), and checks every number against the
values printed in the paper (`[OK]` / `[DIFF]` in the report).

## Quick start
Requirements: Python 3.9 or newer and `git`. The steps use a virtual environment, which works on macOS, Linux and Windows and avoids the
`externally-managed-environment` error raised by system-managed Python installations (e.g., Homebrew).

```bash
git clone https://github.com/Genaina/uncertainty-in-the-wild.git
cd uncertainty-in-the-wild/uip_analysis

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
| `common.py` | CSV loading, domain map (Table 3 / Fig. 1), comparison helpers |
| `coding.py` | Rule-based coding of the verbatim fields (follows the operational coding rules of Section 3.4) |
| `paper_reported.py` | The numbers and case lists printed in the paper, used only for validation |
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
   *strict* (explicit evidence only), *lenient* (+ tentative marks such as `(?)`), *paper* (+ template-only answers); the script lists the cases where the
   automatic rule and the manual coding differ. The *paper* criterion reproduces the manual coding exactly (11/14/14/4); *strict* and *lenient* show how many
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
   trade-off and abstraction fields and compared with the exemplars cited in the text.

Outputs: `rq2_abstraction_by_domain.csv`, `rq2_source_categories_per_case.csv`, `rq2_source_types_per_case.csv`, `rq2_source_counts.csv`, `rq2_mechanisms_per_case.csv`.
Items 2 and 3 are **keyword heuristics**: they quantify what the verbatim text supports and do not replace the qualitative reading in the paper.

### RQ3 — What operational impacts are associated with the interactions? (`rq3.py`, Section 6.3)
1. **Impact characterisation** (Section 6.3.1, Table 6): *generic/template* when the `Impact` field is explicitly marked as generic or template text, *multi-dimensional* otherwise (Section 3.4, rule 4).
2. **Affected quality dimensions** (Section 6.3.2, Table 7): safety, performance, reliability & availability, mission success, human factors & trust, resource efficiency/cost.
   Table 7 is an analyst reading of each exemplar, so the script does not recompute it; it lists, for every dimension, the cases cited in the paper and what the verbatim text supports:
   the `Impact` field itself (primary evidence) or the `Trade-offs` / `Summary` fields (secondary evidence), with the supporting excerpt. Cases cited without textual evidence and
   cases the `Impact` field supports but the table does not cite are listed separately.
   Because Table 7 lists *supporting* cases and not every case that shows a dimension, the agreement measure is **coverage**: the share of the cited cases that the text supports,
   from the `Impact` field alone and from any field.

Outputs: `rq3_impact_coding_per_case.csv`, `rq3_impact_class_by_domain.csv`, `rq3_quality_dimensions.csv`, `rq3_quality_dimension_evidence.csv`.

### RQ4 — Which mechanisms address the interactions, and under what conditions? (`rq4.py`, Section 6.4)
1. **Preparedness** (Table 8): the `Level of Preparedness` text is split on the labels Awareness, Prevention, Detectability, Representation, Comprehension (= Understanding) and Mitigation;
   a capability is *reported* when its segment has non-empty, non-negative content ("Limited"/"Partial" count as partial capability).
2. **Strategy** (Table 12): the `Strategy` field is split on Detection / Representation / Analysis / Mitigation; entries such as "unknown" or "blank" are not counted.
3. **Lifecycle stage** (Section 6.4.3): design-time, runtime or both, from the `Lifecycle Stage` field. Table 10 (lifecycle activities) is analyst-derived; its case lists are only printed.
4. **Applicability conditions** (Table 9) and **trade-offs** (Table 11): keyword cross-check against the case lists in the paper.
5. **Coverage**: how many of the solution-space fields each exemplar filled in (relevant for the threats to validity).

Outputs: `rq4_preparedness_per_case.csv`, `rq4_strategy_per_case.csv`, `rq4_lifecycle_per_case.csv`, `rq4_applicability_keywords_per_case.csv`,
`rq4_tradeoffs_keywords_per_case.csv`, `rq4_solution_space_coverage.csv`, and the comparison files `rq4_table8/9/11/12_comparison.csv` (coverage per dimension: the share of the cases cited in the paper that the parsed text supports, plus the cases on each side).

## How to read the validation report
- **RQ1–RQ3 problem-space numbers** (Tables 4, 5 and 6, the Fig. 3 series and the counts of Sections 6.1–6.3) are fully determined by the data and the coding rules; they print `[OK]`
  or no difference lines.
- **RQ4 tables (8, 9, 11, 12) and Tables 7 and 10** reflect the authors' qualitative reading of free-text answers. The scripts apply a mechanical parse of the same text, so the counts can differ slightly
  from the paper (like Table 7, these tables list supporting or representative cases, so each comparison reports **coverage** — the share of the cited cases that the parsed text supports — and the cases that appear on only one side) (for example, the parse also counts every "Partial"/"Limited" statement); each `[DIFF]` lists the cases on each side, which shows where interpretation, not computation, drives the table.

## Limitations
The exemplars are purposively sampled contributor descriptions, so frequencies describe the catalogue and not the wider population of systems (Section 7).
Several fields were answered in free text with varying detail; the rule-based coders are deliberately conservative, and the manual coding of the interaction categories is the reference for RQ1.
