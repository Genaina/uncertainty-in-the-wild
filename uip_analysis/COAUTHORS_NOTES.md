# Notes for co-authors only — changes made to the manuscript and data

*Not part of the public package. The public README describes the final state only.*

## 1. Data fix
In the contributor sheet, the **content columns** (Uncertainty Sources … Strategy) of rows **CS11 and CS12 were swapped** relative to their Summary/domain
(CS11 = Body Sensor Network, Healthcare; CS12 = Lab Sample Logistics, Robotics). Table 3 was correct; the text citations followed the swapped content.
The swap is corrected in `artifacts_case_studies.csv`; the unmodified file is `artifacts_case_studies_raw_ORIGINAL.csv`.
If the shared counting sheet (UC-Conflict, …) still has CS11/CS12 as in the original, its two rows must be swapped too.

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

## 3. Coding decisions taken (interaction categories, checked against the raw text)
- CS1: dominance removed; conflict counted (label is "Conflict (dominant)").
- CS10: dominance and augmentation removed (the text only describes a conflict).
- CS5: augmentation counted (the text has an Augmentation block).
- CS15: independence and conflict removed ("N/A in this case").
- CS9: dominance recorded as 2 instances (no effect on exemplar-level counts).
- CS4, CS7, CS8, CS14 (template-only answers): **kept in the counts**; one sentence in Sec. 6.1.1 discloses that their categories are not backed by case-specific text. CS14 independence is set to 1 for consistency with CS4 and CS8 (if it should not count, independence becomes 3/18 = 16.7%).
- CS12 is **not** added under "Responsiveness vs Stability" (Tab. 11): it only concerns energy cost.
- Impact lists in the .tex comments corrected: generic = CS8, CS10, CS14.

## 4. Pending
- Ask the contributors of CS4, CS7, CS8 and CS14 for the interaction text (CS8 and CS14 are also generic on impact and blank on the solution space), then replace the template-only codes with evidence-backed ones and delete the disclosure sentence.
- Two files not reviewed per instructions: `LLMAnalysis.tex` and `Catalog-Javi.tex`.
