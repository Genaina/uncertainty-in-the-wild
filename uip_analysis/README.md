# Reproducing the RQ1–RQ4 analysis of "Uncertainty in the Wild"

This package reproduces the cross-case analysis (Sections 6.1–6.4) of *Uncertainty in the Wild: A Cross-Domain Catalogue of
Uncertainty Interactions in Autonomous and Self-Adaptive Systems*. It takes the catalogue of 18 uncertainty-interaction
exemplars (CS1–CS18), computes the frequencies, tables and figures of each research question, and checks every number
against the values printed in the manuscript (`[OK]` / `[DIFF]` in the report).

## Quick start
```bash
pip install pandas matplotlib      # Python 3.9+
python run_all.py                  # runs RQ1..RQ4, prints the report, writes everything to output/
python rq1.py                      # or run a single research question (rq1.py ... rq4.py)
```
`output/full_report.txt` contains the complete printed report; every table is also saved as a CSV in `output/`.

## Package layout
| Path | Content |
|---|---|
| `data/artifacts_case_studies.csv` | The catalogue: one row per exemplar, with the contributors' verbatim answers to the characterisation template |
| `data/manual_interaction_counts.csv` | Authors' coding of the interaction categories per exemplar (used by RQ1, see below) |
| `common.py` | CSV loading, domain map (Table 3 / Fig. 1), comparison helpers |
| `coding.py` | Rule-based coding of the verbatim fields (follows the operational coding rules of Section 3.4) |
| `paper_reported.py` | Numbers and case lists as printed in the manuscript, used only for validation |
| `rq1.py` … `rq4.py` | One script per research question |
| `run_all.py` | Runs the four scripts in order |

## Input data
**`artifacts_case_studies.csv`** — separator `;`, encoding cp1252. Columns: `ID`, `Participant(s)`, `Case Study (Domains)`, `Summary`,
and the template fields `Uncertainty Sources (verbatim)`, `Uncertainty Interaction Category`, `Uncertainty Nature`, `Abstraction Gap`,
`Impact`, `Level of Preparedness`, `Applicability Conditions`, `Lifecycle Stage`, `Trade-offs`, `Strategy`.
The *problem space* (sources, interaction category, nature, abstraction gap, impact) feeds RQ1–RQ3; the *solution space*
(preparedness, applicability, lifecycle, trade-offs, strategy) feeds RQ4. Empty or "not provided" fields are treated as
**missing information, never as negative evidence** (Section 3.4).

**`manual_interaction_counts.csv`** — columns `ID, conflict, dominance, augmentation, independence, template_only`. Each value is the number
of documented interaction instances of that category in the exemplar; a category counts once per exemplar when the value is ≥ 1
(Section 3.4, rule 1). `template_only = 1` flags exemplars whose interaction field contains only the template definitions
(CS4, CS7, CS8, CS14): they are counted as coded, and `rq1.py` also prints the counts without them as a sensitivity check.

The **primary domain** of each exemplar follows Table 3 (six domains: Automotive, IT/Cloud, Robotics, Healthcare, Smart City, Aerospace).
Exemplars spanning two domains are assigned to the one that characterises the system (e.g., CS5, a hospital service robot with a human in the loop, is Robotics).

## What each script computes

### RQ1 — What types of uncertainty interactions are observed? (`rq1.py`, Section 6.1)
1. **Domain distribution** (Fig. 1).
2. **Interaction categories** (dominance, conflict, augmentation, independence), counted per exemplar from `manual_interaction_counts.csv`,
   in total (Section 6.1.1) and per domain (Fig. 3). As a cross-check, `coding.py` also codes the verbatim text automatically under three criteria:
   *strict* (explicit evidence only), *lenient* (+ tentative marks such as `(?)`), *paper* (+ template-only answers). The script lists the cases where the automatic rule and the manual coding differ.
3. **Interaction nature** (Section 6.1.2, Table 4): an exemplar is *heterogeneous* unless its `Uncertainty Nature` field says homogeneous.

Expected result: dominance 11/18, conflict 14/18, augmentation 14/18, independence 4/18; heterogeneous 16/18.
Outputs: `rq1_domain_distribution.csv`, `rq1_category_counts.csv`, `rq1_manual_flags.csv`, `rq1_category_by_domain.csv`, `rq1_nature_by_domain.csv`,
`rq1_interaction_coding_per_case.csv`, `rq1_fig_domains.png`, `rq1_fig_categories.png`.

### RQ2 — Which sources, abstraction levels and causal mechanisms participate? (`rq2.py`, Section 6.2)
1. **Abstraction span** (Section 6.2.1, Table 5): *same/partial level* when the `Abstraction Gap` field says "same" or is empty, *cross-layer* otherwise.
   Expected: 14 cross-layer, 4 same/partial (CS4, CS6, CS7, CS10).
2. **Uncertainty sources** (Section 6.2.2): frequency of source *categories* (model, adaptation functions, goals, environment, resources, human) and *types*
   (measurement, occurrence, design, behavior, belief, spatio-temporal) by keyword search over `Uncertainty Sources (verbatim)`, plus the most frequent co-occurring category pairs.
3. **Causal mechanisms** (Section 6.2.3): propagation, amplification, dominance and trade-off/conflict are searched by keyword in the interaction, impact, trade-off and abstraction fields and compared with the exemplars cited in the text.

Outputs: `rq2_abstraction_by_domain.csv`, `rq2_source_categories_per_case.csv`, `rq2_source_types_per_case.csv`, `rq2_source_counts.csv`, `rq2_mechanisms_per_case.csv`.
Items 2 and 3 are **keyword heuristics**: they quantify what the verbatim text supports and do not replace the qualitative reading in the paper.

### RQ3 — What operational impacts are associated with the interactions? (`rq3.py`, Section 6.3)
1. **Impact characterisation** (Section 6.3.1, Table 6): *generic/template* when the `Impact` field is explicitly marked as generic or template text (CS8, CS10, CS14), *multi-dimensional* otherwise (Section 3.4, rule 4). Expected: 15 and 3.
2. **Affected quality dimensions** (Section 6.3.2, Table 7): safety, performance, reliability & availability, mission success, human factors & trust, resource efficiency/cost, detected by keywords in the `Impact` field and compared (Jaccard similarity) with the case lists of Table 7, which is analyst-derived.

Outputs: `rq3_impact_coding_per_case.csv`, `rq3_impact_class_by_domain.csv`, `rq3_quality_dimensions.csv`.

### RQ4 — Which mechanisms address the interactions, and under what conditions? (`rq4.py`, Section 6.4)
1. **Preparedness** (Table 8): the `Level of Preparedness` text is split on the labels Awareness, Prevention, Detectability, Representation, Comprehension (= Understanding) and Mitigation; a capability is *reported* when its segment has non-empty, non-negative content ("Limited"/"Partial" count as partial capability).
2. **Strategy** (Table 12): the `Strategy` field is split on Detection / Representation / Analysis / Mitigation; entries such as "unknown" or "blank" are not counted.
3. **Lifecycle stage** (Section 6.4.3): design-time, runtime or both, from the `Lifecycle Stage` field; Table 10 (lifecycle activities) is analyst-derived and its counts are only printed.
4. **Applicability conditions** (Table 9) and **trade-offs** (Table 11): keyword cross-check against the manual analysis in the paper.
5. **Coverage**: how many of the solution-space fields each exemplar filled in (relevant for the threats to validity).

Outputs: `rq4_preparedness_per_case.csv`, `rq4_strategy_per_case.csv`, `rq4_lifecycle_per_case.csv`, `rq4_applicability_keywords_per_case.csv`,
`rq4_tradeoffs_keywords_per_case.csv`, `rq4_solution_space_coverage.csv`, and the comparison files `rq4_table8/9/11/12_comparison.csv` (with Jaccard similarity per dimension).

## How to read the validation report
- **RQ1–RQ3 problem-space numbers** (Tables 4, 5, 6, the Fig. 3 series and the counts of Sections 6.1–6.3) are fully determined by the data and the coding rules, and should print `[OK]` (or no difference lines).
- **Analyst-derived tables** (Tables 7–12) depend on the authors' interpretation of free text. The scripts reproduce what can be parsed mechanically and report the differences as `[DIFF]` with the cases on each side; these differences show where interpretation, not computation, drives the table.

## Limitations
The exemplars are purposively sampled contributor descriptions, so frequencies describe the catalogue and not the wider population of systems (Section 7).
Several fields were answered in free text with varying detail; the rule-based coders are deliberately conservative and the manual coding of interaction categories is the reference for RQ1.
