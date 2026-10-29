# RQ1–RQ4 analysis scripts — "Uncertainty in the Wild"

Reproduces, from `data/artifacts_case_studies_raw_corrected.csv`, the analyses of Sections 6.1–6.4 of the manuscript
and **validates every number against what was originally printed in the paper** (`[OK]` / `[DIFF]`).

## Data
- `data/artifacts_case_studies_raw_corrected.csv`: the original contributor sheet with the content columns
  (Uncertainty Sources … Strategy) of rows CS11 and CS12 swapped, so that they match the Summary/domain columns
  (CS11 = Body Sensor Network, CS12 = Lab Sample Logistics). The original file is kept as `data/..._ORIGINAL.csv`.
- `data/manual_interaction_counts.csv`: the authors' manual count of interaction categories per case
  (CS11/CS12 rows already corrected). It is the ground truth for RQ1; the rule-based coder is only a cross-check.

## Usage
```bash
pip install pandas matplotlib
python run_all.py        # runs RQ1..RQ4, prints the report and saves everything to output/
python rq1.py            # or each RQ separately
```

## Files
| File | Content |
|---|---|
| `common.py` | CSV loading (`;`, cp1252), the paper's domain map, comparison helpers |
| `coding.py` | automatic rule-based coding (Section 3.4 of the paper) |
| `paper_reported.py` | numbers / case lists **as originally printed** in the paper, used only for validation |
| `rq1.py` | interaction categories (dominance/conflict/augmentation/independence), heterogeneity, Fig. 1, Fig. 3, Tab. 4 |
| `rq2.py` | cross-layer vs same-level (Tab. 5), source categories/types, causal mechanisms |
| `rq3.py` | multi-dimensional vs generic impact (Tab. 6), quality dimensions (Tab. 7) |
| `rq4.py` | preparedness (Tab. 8), applicability (Tab. 9), lifecycle (Tab. 10), trade-offs (Tab. 11), strategy (Tab. 12) |

## Three automatic criteria for interaction categories (RQ1 cross-check)
- `strict`: explicit contributor evidence only
- `lenient`: + tentative marks (`(?)`, `(Possible)`, `Conflict (dominant)`)
- `paper`: + template-only answers (CS4, CS7, CS8, CS14 returned only the template definitions)

## What is fully reproducible and what is not
- **Reproduced from the CSV**: heterogeneous/homogeneous (16/2), cross-layer/same (14/4), generic impact (15/3), lifecycle.
  Interaction categories (RQ1) use the **manual sheet** as ground truth.
- **Analyst-derived** (Tabs. 7, 9, 10, 11 and parts of 8 and 12): they depend on manual interpretation. The scripts provide a
  keyword cross-check with Jaccard similarity; differences there indicate interpretation choices, not necessarily errors.

## Divergences found and status

Computed values below use the manual sheet and the corrected CSV. `paper_reported.py` keeps the values **as originally printed**,
so the report still shows `[DIFF]` at these points (expected).

| # | Original divergence | Status | Resolution in the .tex files (`tex_marked/`) |
|---|---|---|---|
| 1 | Sec. 6.1.1 said 17/16/15/4 (dominance/conflict/augmentation/independence); Fig. 3 summed to 13/14/14 | **Resolved** | Text now 13 (72.2%), 14 (77.8%), 14 (77.8%), 4 (22.2%); "vast majority" → "most" (also in Lesson 1) |
| 2 | Fig. 3, dominance: Robotics/Healthcare | **Resolved** | With CS5 under Robotics and CS11/CS12 content corrected: Robotics 3, Healthcare 0 (original: 1 and 2) |
| 3 | Tab. 4 summed to 15+3 (text: 16/2) | **Resolved** | Robotics 3/0 (the `\added{1}` was an editing leftover) |
| 4 | Tab. 5 summed to 17 | **Resolved** | IT/Cloud 6/1, Robotics 3/0 (checked against the `%Cross-layer` comment in the .tex) |
| 5 | Tab. 6 summed to 10/8 (text: 15/3) | **Resolved** | Automotive 4/1, IT 5/2, Robotics 3/0, Healthcare 1/0, Smart City 1/0, Aerospace 1/0. Commented impact list: generic = CS8, CS10, CS14 (the old list with CS3, CS4, CS6, CS7 was wrong: CS4 and CS7 were template-only in the interaction field, not in the impact field) |
| 6 | CS11 × CS12 | **Resolved (reinterpreted)** | Tab. 3 and the Summary/domain columns are **correct** (CS11 = BSN, CS12 = Lab Sample). The error was in the CSV: the content columns of the two rows were swapped. CSV corrected; citations fixed in the text: energy (CS12), communication (CS11), BSN (CS11), battery (CS12), Tab. 9 Architectural (CS12), Tab. 11 Sensitivity (CS11) |
| 7 | CS5: dual domain Healthcare/Robotics | **Resolved** | Kept under Robotics; sentence added in Sec. 3.3, note in Sec. 5 and in Tab. 3 |
| 8 | Fig. 1 rounding: 38.8% and 5.5% (summed to 99.8%) | **Resolved** | 38.9% and 5.6% in the text and in the pie data |
| 9 | Tab. 8 Prevention and Tab. 11 Robustness vs Resource | **Resolved** | Added CS11 and CS12 (Prevention) and CS12 (Robustness vs Resource Consumption) |
| 10 | Template-only answers (CS4, CS7, CS8, CS14) counted in the categories without case-specific evidence | **Open** | Authors' decision; `TODO(authors)` in Sec. 6.1.1 |
| 11 | Codings to double-check: CS1 (conflict counted as dominance, but cited as conflict in 6.2.3), CS5 (no augmentation), CS10 (dominance/augmentation without support in the raw text), CS15 (independence and conflict counted despite "N/A"), CS14 (independence not counted) | **Open** | `TODO(authors)` in 6.1.1 and 6.2.3 |
| 12 | CS12 under Responsiveness vs Stability (Tab. 11) | **Optional** | Not applied; debatable |

If the authors' own counting sheet (UC-Conflict etc.) still has rows CS11/CS12 as in the original CSV, they must be swapped there too.
