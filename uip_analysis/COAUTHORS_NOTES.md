# Notes for co-authors only — changes made to the manuscript and data

*For co-authors only. The public README describes the final state only; this file tracks what changed relative to the previous version of the manuscript and the catalogue.*

## 0. Files and how to review
- `tex_marked/MetaAnalysis.tex`, `collection.tex`, `lessons.tex`, `DataSet.tex`: the LaTeX files with every change marked; anything without a mark is the previous text.
  `\added{new}`, `\deleted{old}`, `\replaced{new}{old}`; a comment `% CHANGED: was ...` at the end of a line is used inside the Fig. 3 (pgfplots) coordinates and some table rows.
  Search for `\added`, `\replaced`, `\deleted` and `% CHANGED`. If the `changes` package is not loaded in `main.tex`, add `\input{changes_marks}` to the preamble (`changes_marks.tex`).
- `tex/`: the same files with all changes accepted (clean copies). `all_changes.diff`: the changes as a plain diff against the previous version.
- `uip_analysis/` (this repository folder): scripts, data and README that reproduce RQ1–RQ4.

## 1. Data fix
In the contributor sheet, the **content columns** (Uncertainty Sources … Strategy) of rows **CS11 and CS12 were swapped** relative to their Summary/domain
(CS11 = Body Sensor Network, Healthcare; CS12 = Lab Sample Logistics, Robotics). Table 3 was correct; the text citations followed the swapped content.
The swap is corrected in `artifacts_case_studies_raw.csv`. Only the revised sheet is kept; the original sheet was removed.

## 2. Numbers that changed in the manuscript (LaTeX files: `tex_marked/`, with change marks; `tex/`, clean)
| Where | Previous | Now |
|---|---|---|
| Sec. 6.1.1, dominance / conflict / augmentation / independence | 17 / 16 / 15 / 4 (of 18) | 11 / 14 / 14 / 4 (of 18) |
| Fig. 3, dominance (Automotive, IT/Cloud, Robotics, Healthcare, Smart City, Aerospace) | 2, 6, 1, 2, 1, 1 | 2, 4, 3, 0, 1, 1 |
| Fig. 3, augmentation | 4, 5, 2, 1, 1, 1 | 4, 4, 3, 1, 1, 1 |
| Tab. 4, Robotics (het/hom) | 2 / 1 (sum 15+3) | 3 / 0 (sum 16+2, as in the text) |
| Tab. 5, IT/Cloud · Robotics (cross/same) | 5/1 · 2/1 (sum 17) | 6/1 · 3/0 (sum 18) |
| Tab. 6 (multi/generic) | sum 10/8, text said 15/3 | Auto 4/1, IT 5/2, Robotics 3/0, Healthcare 1/0, Smart City 1/0, Aerospace 1/0 (sum 15/3) |
| Sec. 6.2.2/6.2.3, Tab. 9, Tab. 11 | CS11/CS12 cited the wrong way round | energy → CS12, communication → CS11, BSN → CS11, battery → CS12; Tab. 9 Architectural → CS12; Tab. 11 Sensitivity → CS11 |
| Tab. 8 Prevention · Tab. 11 Robustness vs Resource | CS1, CS4, CS7, CS13, CS16 · CS1, CS2, CS13 | + CS11, CS12 · + CS12 |
| Fig. 1 percentages | 38.8% / 5.5% | 38.9% / 5.6% |
| Sec. 3.3, Sec. 5, Tab. 3 | — | CS5 declared dual (Healthcare/Robotics), counted as Robotics |
| Lesson 1, Sec. 6.1.1 | "vast majority" | "most" |
| Sec. 6.1.1 surrounding sentences | examples and domain remarks written for the earlier coding (e.g., dominance in distributed systems, healthcare dominance, "greater emphasis on augmentation", independence in "modeling-oriented" environments) | rewritten to match the final data: dominance examples CS3, CS5, CS12; automotive = conflict and augmentation (4 of 5 each); robotics = dominance and augmentation in all 3; independence documented only for CS3 (CS4, CS8, CS14 are template-only); added: every exemplar shows at least one relation, 14/18 at least two, 7 all three |
| Tab. 8 (supporting cases) | Detectability, Representation, Prevention, Understanding, Mitigation as printed | + CS13 (Detectability); + CS7 (Representation); + CS9, CS18 (Prevention); + CS4, CS7, CS9 (Understanding); + CS9 (Mitigation). CS4 and CS7 Understanding: their answers say the effect "could be analyzed, depending on the type" |
| Tab. 12 (strategy) | Detection 8, Representation 8, Analysis 8, Mitigation 11 cases | Detection + CS4, CS7, CS13, CS16; Representation + CS4, CS7, CS18 and − CS2 (no Representation entry); Analysis + CS2, CS17; Mitigation + CS17. Table 12 now matches the Strategy entries exactly |
| Tab. 11 | Safety vs Performance: CS11, CS12, CS16; Responsiveness vs Stability: CS1, CS16 | Safety vs Performance: CS12, CS16, CS18 (CS11 removed: the BSN case has the sensitivity/false-alarm trade-off, the robot case has safety vs mission completion); Responsiveness vs Stability: + CS13 ("aggressive adaptation… may increase instability") |
| Sec. 6.4.1 (after the sentence on strategy evidence) | — | added: CS5 (one-sentence answer) and CS4 ("cannot be modeled") are credited from their strategy entries |
| Sec. 6.4.1, 6.4.4 sentences | case lists written for the earlier tables | detectability (+CS13), understanding (+CS4, CS7, CS9), mitigation (+CS9); safety/performance tension: "robotics and automotive" instead of "healthcare, robotics, and automotive" |

## 3. Coding decisions taken (interaction categories, checked against the raw text)
- CS1: dominance removed; conflict counted (label is "Conflict (dominant)").
- CS10: dominance and augmentation removed (the text only describes a conflict).
- CS5: augmentation counted (the text has an Augmentation block).
- CS15: independence and conflict removed ("N/A in this case").
- CS9: dominance recorded as 2 instances (no effect on exemplar-level counts).
- CS4, CS7, CS8, CS14 (template-only answers): **kept in the counts**; one sentence in Sec. 6.1.1 discloses that their categories are not backed by case-specific text. CS14 independence is set to 1 for consistency with CS4 and CS8 (if it should not count, independence becomes 3/18 = 16.7%).
- CS12 is **not** added under "Responsiveness vs Stability" (Tab. 11): it only concerns energy cost.
- Impact lists in the .tex comments corrected: generic = CS8, CS10, CS14.

## 4. Pending to double-check with Raffaela and Javier
- Ask the contributors of CS4, CS7, CS8 and CS14 for the interaction text (CS8 and CS14 are also generic on impact and blank on the solution space), then replace the template-only codes with evidence-backed ones and delete the disclosure sentence.
- Table 8: CS5 and CS4 Representation are credited from the Strategy entries; a sentence explaining this was added to Sec. 6.4.1 (marked) and to the README. Decide whether to keep these two credits.
- Table 7 (quality dimensions) is unchanged. Every case it lists has supporting text (from the `Impact` field, or from `Trade-offs` / `Summary` for CS12 and CS17 under Safety, CS12 under Mission Success, and CS3 and CS18 under Resource Efficiency). The `Impact` field also supports cases that the table does not list (e.g., CS9 under Safety, Reliability and Cost; CS6 under Safety; CS13 and CS11 under Performance). Decide whether to keep the table as a list of supporting cases or to extend it.
- Not reviewed in this round: `LLMAnalysis.tex` and `Catalog-Javi.tex`.

## 5. Public scripts vs tracking
The public package (`uip_analysis`) describes only the final state: the scripts compute the results and print the supporting text, and contain **no comparison with earlier versions or with the printed values of the paper**
(the former `[OK]`/`[DIFF]` checks and `paper_reported.py` were removed; `analyst_assignments.py` keeps only the case assignments of Tables 7, 9, 10 and 11 as input).
All tracking of what changed lives in this file, in `tex_marked/` (change marks) and in `all_changes.diff`.
