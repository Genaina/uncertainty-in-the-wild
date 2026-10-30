"""RQ4 - Detection/representation/analysis/prevention/mitigation mechanisms and their conditions (Sec. 6.4)

Tables 8 and 12 (preparedness, strategy) are computed by parsing the labelled entries of the verbatim fields.
Tables 9 and 11 (applicability conditions, trade-offs) are analyst-assigned categories, so for every assigned case
the script shows the text excerpt that supports the assignment.
"""
import re
import pandas as pd
from common import load_raw, OUT, pct, cases_to_str, is_blank
from coding import code_preparedness, code_strategy, code_lifecycle, _prep_segments
from analyst_assignments import TABLE9, TABLE10, TABLE11

PREP_TO_STRAT = {"Detectability": "Detection", "Representation": "Representation",
                 "Understanding": "Analysis", "Mitigation": "Mitigation"}

APPLIC_PATTERNS = {
    "Architectural Assumptions": r"central coordinator|reconfiguration|architecture|layers",
    "Infrastructure Requirements": r"\bbus\b|fram|communication|sensing capability|storage",
    "Observability Requirements": r"observab|sensing|sensor|measure|metrics are available|confidence",
    "Model Availability": r"model|quantified",
    "Adaptation Capability": r"controllable|adaptive|alternative configurations|reconfiguration|adaptation|switch",
    "Operational Scope": r"enabling scope|restricted|contexts?",
}
TRADEOFF_PATTERNS = {
    "Robustness vs Resource Consumption": r"robustness|redundan|overhead|energy|memory|computational|cost",
    "Safety vs Performance": r"safety|conservative",
    "Responsiveness vs Stability": r"stability|instabil|responsiveness|volatility",
    "Autonomy vs Assurance": r"autonomy|assurance|guarantee",
    "Sensitivity vs False Positives": r"false (?:alarm|positive)|sensitivity",
}


def _short(t, n=105):
    t = re.sub(r"\s+", " ", str(t)).strip()
    return t if len(t) <= n else t[:n] + "..."


def _prep_text(raw, cid, dim):
    t = raw.loc[cid, "Level of Preparedness"]
    if is_blank(t):
        return ""
    segs = _prep_segments(t)
    return segs.get(dim, "" if segs else re.sub(r"\s+", " ", str(t)))


def _strat_text(raw, cid, label):
    t = raw.loc[cid, "Strategy"]
    if is_blank(t):
        return ""
    t = re.sub(r"\s+", " ", str(t))
    ms = list(re.finditer(r"\b(Detection|Representation|Analysis|Mitigation)\s*:", t))
    for i, m in enumerate(ms):
        if m.group(1) == label:
            return t[m.end(): ms[i + 1].start() if i + 1 < len(ms) else len(t)].strip()
    return ""


def _list_labeled(raw, title, computed, kind, long_rows):
    """Tables 8 / 12: for every dimension, the cases whose text reports it, with the supporting entry."""
    print(f"\n{title}")
    rows = []
    for dim in computed.columns:
        got = computed.index[computed[dim]]
        print(f"   {dim}: {len(got)}/{len(computed)} cases  ({cases_to_str(got)})")
        for cid in got:
            if kind == "prep":
                ev = f"Preparedness: '{_short(_prep_text(raw, cid, dim))}'"
            else:
                ev = f"Strategy: '{_short(_strat_text(raw, cid, dim))}'"
            print(f"          {cid:<5} {ev}")
            long_rows.append({"table": title.split(":")[0].strip(), "dimension": dim, "case": cid, "evidence": ev})
        rows.append({"dimension": dim, "n_cases": len(got), "cases": cases_to_str(got)})
    return pd.DataFrame(rows)


def _evidence_table(raw, title, field, patterns, assignments):
    """Tables 9 / 11: for every assigned case, the excerpt of `field` that supports the assignment."""
    print(f"\n{title}")
    rows = []
    for dim, ids in assignments.items():
        pat = re.compile(patterns[dim], re.I)
        ok = []
        for cid in ids:
            txt = raw.loc[cid, field]
            mm = None if is_blank(txt) else pat.search(str(txt))
            if mm:
                t = re.sub(r"\s+", " ", str(txt))
                k = max(0, mm.start() - 35)
                ex = t[k: mm.end() + 55].strip()
                ok.append(cid)
            else:
                ex = ""
            rows.append({"dimension": dim, "case": cid, "supported": bool(mm), "evidence_excerpt": ex})
        miss = [c for c in ids if c not in ok]
        print(f"   {dim}: {len(ok)}/{len(ids)} assigned cases have supporting text" + (f"  (no match: {cases_to_str(miss)})" if miss else ""))
        for r in rows[-len(ids):]:
            print(f"          {r['case']:<5} {_short(r['evidence_excerpt'], 95) or '-- no supporting text found --'}")
    return pd.DataFrame(rows)


def run(raw=None):
    raw = load_raw() if raw is None else raw
    n = len(raw)
    print("=" * 72, "\nRQ4 - Solution space\n" + "=" * 72)
    long_rows = []

    # ---- 6.4.1 preparedness (Tab.8)
    prep = code_preparedness(raw)
    prep.to_csv(OUT / "rq4_preparedness_per_case.csv")
    print("\n[Tab.8] Preparedness -- number of cases reporting the capability (parsed from the text):")
    for k, v in prep.sum().sort_values(ascending=False).items():
        print(f"   {k:<15} {v:>2}/{n} = {pct(v, n)}")
    reported = raw["Level of Preparedness"].map(lambda t: isinstance(t, str) and "blank" not in t.lower()[:12])
    print(f"   Cases that filled in the Preparedness field: {int(reported.sum())}/{n} "
          f"(missing: {cases_to_str(raw.index[~reported])})")
    t8 = _list_labeled(raw, "[Tab.8] Preparedness: cases that report each capability, with the supporting entry", prep, "prep", long_rows)
    t8.to_csv(OUT / "rq4_table8_cases.csv", index=False)

    # ---- 6.4.5 strategy (Tab.12)
    strat = code_strategy(raw)
    strat.to_csv(OUT / "rq4_strategy_per_case.csv")
    print("\n[Tab.12] Strategy -- cases reporting a strategy (parsed from the text):")
    for k, v in strat.sum().items():
        print(f"   {k:<15} {v:>2}/{n}")
    t12 = _list_labeled(raw, "[Tab.12] Strategy: cases that report each strategy category, with the supporting entry", strat, "strat", long_rows)
    t12.to_csv(OUT / "rq4_table12_cases.csv", index=False)
    pd.DataFrame(long_rows).to_csv(OUT / "rq4_table8_12_evidence.csv", index=False)

    # ---- 6.4.3 lifecycle
    life = code_lifecycle(raw)
    life.to_csv(OUT / "rq4_lifecycle_per_case.csv", header=["lifecycle"])
    print("\n[6.4.3] Lifecycle stage (raw field):")
    for k, v in life.value_counts().items():
        print(f"   {k:<13} {v:>2}/{n}  {cases_to_str(life.index[life == k])}")
    rep = life[life != "not reported"]
    print(f"   Among the {len(rep)} cases that report it: both = {(rep == 'both').sum()}, "
          f"runtime-only = {(rep == 'runtime').sum()}, design-only = {(rep == 'design-time').sum()}")
    print("   Table 10 (lifecycle activities) is analyst-derived; cases assigned to each activity:")
    for k, v in TABLE10.items():
        print(f"   {k:<26} {len(v):>2} cases  ({cases_to_str(v)})")

    # ---- 6.4.2 applicability (Tab.9) and 6.4.4 trade-offs (Tab.11): evidence per assigned case
    t9 = _evidence_table(raw, "[Tab.9] Applicability conditions: supporting text for each assigned case",
                         "Applicability Conditions", APPLIC_PATTERNS, TABLE9)
    t9.to_csv(OUT / "rq4_table9_evidence.csv", index=False)
    t11 = _evidence_table(raw, "[Tab.11] Trade-offs: supporting text for each assigned case",
                          "Trade-offs", TRADEOFF_PATTERNS, TABLE11)
    t11.to_csv(OUT / "rq4_table11_evidence.csv", index=False)
    filled = raw["Applicability Conditions"].map(lambda t: isinstance(t, str) and
                                                 "blank" not in t.lower()[:12] and "not provided" not in t.lower())
    filled_t = raw["Trade-offs"].map(lambda t: isinstance(t, str) and
                                     "blank" not in t.lower()[:12] and "not provided" not in t.lower())
    print(f"\n   Cases with the Applicability field filled in: {int(filled.sum())}/{n}")
    print(f"   Cases with the Trade-offs field filled in: {int(filled_t.sum())}/{n} (not filled in: {cases_to_str(raw.index[~filled_t])})")

    # ---- coverage of solution-space information (relevant for threats to validity)
    cov = pd.DataFrame({"preparedness": reported, "applicability": filled, "lifecycle": life != "not reported",
                        "tradeoffs": filled_t, "strategy": strat.any(axis=1)})
    cov["n_fields"] = cov.sum(axis=1)
    cov.to_csv(OUT / "rq4_solution_space_coverage.csv")
    print("\n[Coverage] Solution-space fields filled in per case:")
    print(cov["n_fields"].value_counts().sort_index().to_string())
    print("   Cases with 0-1 fields:", cases_to_str(cov.index[cov.n_fields <= 1]))
    return {"prep": prep, "strat": strat, "life": life, "cov": cov}


if __name__ == "__main__":
    run()
