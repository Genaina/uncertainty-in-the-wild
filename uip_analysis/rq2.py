"""RQ2 - Which uncertainty sources, system elements, abstraction levels and causal mechanisms participate? (Sec. 6.2)

Section 6.2.1 (abstraction span, Table 5) is computed from the Abstraction Gap field.
Sections 6.2.2 (sources) and 6.2.3 (causal mechanisms) list, for each kind of source and each mechanism, the exemplars the
authors assigned to it; the report shows the text of each exemplar that supports the assignment.
"""
import re
import pandas as pd
from common import load_raw, OUT, pct, cases_to_str, is_blank
from coding import code_abstraction, _strip_template
from analyst_assignments import DOMAINS, SOURCES_622, MECHANISMS_623

SOURCE_PATTERNS = {
    "workload variation": r"workload|request|arrival|demand",
    "network disruptions and communication failures": r"network|connectivity|communication|partition|packet|disconnect",
    "physical disturbances": r"disturbance|wind|floor|push|occlusion|lighting",
    "human behavior": r"human|user|patient|driver|behaviou?r",
    "traffic conditions": r"traffic|road|pedestrian|fog|visibility|vehicle",
    "changing operational contexts": r"context|situation|operating|environment",
    "computational resources": r"comput|memory|gpu|cpu|resource|processing",
    "communication infrastructure": r"communication|network|telemetry|\bbus\b|bandwidth|link|topology|partition|disconnect",
    "energy availability": r"battery|energy|power",
    "sensing infrastructure": r"sensor|sensing|measurement|camera|signal",
    "actuator behavior": r"actuator|brak|motor",
    "abstractions and assumptions in formal models": r"abstraction|assumption|incomplete|model",
    "estimation and prediction processes": r"estimat|predict|forecast|belief",
    "digital twins": r"twin|fidelity|completeness",
    "machine-learning components": r"\bml\b|machine|learn|neural|\bllm\b|\bai\b|classifier|predictor|perception",
    "system representations": r"representation|parametr|mismatch|model",
    "planning, configuration selection, runtime decision-making and control policies": r"adapt|planning|decision|configuration|polic|tactic|control",
    "competing objectives (safety, performance, reliability, cost, efficiency)": r"goal|objective|utility|requirement|trade|safety|cost|performance",
}
MECHANISM_PATTERNS = {
    "Propagation": r"propagat|transform|cascad|flows? into|levels?|layers?|across|\u2192|to high-level",
    "Amplification": r"amplif|reinforc|jointly increase|correlated|augment",
    "Dominance": r"dominan|dominat",
    "Trade-off / conflict": r"conflict|trade-?off|reducing|increase[s]? (?:uncertainty|instability|overhead)",
}
SOURCE_FIELDS = ["Uncertainty Sources (verbatim)", "Applicability Conditions", "Summary"]
MECHANISM_FIELDS = ["Uncertainty Interaction Category", "Impact", "Trade-offs", "Abstraction Gap", "Summary"]


LABELS = {"augmentation", "conflict", "dominance", "independence"}


def _first_match(raw, cid, fields, pattern):
    """First excerpt that supports `pattern` (a label that is followed by no text, as in a template-only answer, does not count)."""
    pat = re.compile(pattern, re.I)
    for f in fields:
        t = raw.loc[cid, f]
        if is_blank(t):
            continue
        t = _strip_template(t) if f == "Uncertainty Interaction Category" else str(t)    # ignore the template definitions
        s = re.sub(r"\s+", " ", t)
        for mm in pat.finditer(s):
            tail = [w for w in re.sub(r"[^A-Za-z ]", " ", s[mm.end(): mm.end() + 80]).split() if w.lower() not in LABELS]
            if f == "Uncertainty Interaction Category" and len(tail) < 3:
                continue
            k = max(0, mm.start() - 35)
            return f, s[k: mm.end() + 55].strip()
    return "", ""


def run(raw=None):
    raw = load_raw() if raw is None else raw
    n, dom = len(raw), raw["domain"]
    print("=" * 72, "\nRQ2 - Sources, abstraction levels and causal mechanisms\n" + "=" * 72)

    # ---- 6.2.1 cross-layer vs same/partial
    span = code_abstraction(raw)
    tab = pd.crosstab(dom, span).reindex(DOMAINS).fillna(0).astype(int)
    for c in ["Cross-layer", "Same/Partial"]:
        if c not in tab:
            tab[c] = 0
    tab = tab[["Cross-layer", "Same/Partial"]]
    tab.to_csv(OUT / "rq2_abstraction_by_domain.csv")
    print("\n[Tab.5] Abstraction span per domain:")
    print(tab.to_string())
    for k, v in span.value_counts().items():
        print(f"   {k}: {v}/{n} = {pct(v, n)}  ({cases_to_str(span.index[span == k])})")
    print("   Rule: 'Same/Partial' when the Abstraction Gap field says 'same' or is empty; 'Cross-layer' otherwise.")
    print("\n   Abstraction Gap text of the Same/Partial exemplars:")
    for cid in span.index[span == "Same/Partial"]:
        t = str(raw.loc[cid, "Abstraction Gap"]).replace("\n", " ")
        print(f"     {cid:<5} {t}")

    # ---- 6.2.2 uncertainty sources: supporting text for every assigned case
    print("\n[6.2.2] Uncertainty sources: supporting text for each exemplar assigned to a kind of source")
    print("   (excerpt of the 'Uncertainty Sources (verbatim)' field first, then 'Applicability Conditions' and 'Summary'; the assignments are the authors' reading of the exemplars)")
    rows = []
    for category, kinds in SOURCES_622.items():
        print(f"\n   {category.upper()}")
        for kind, ids in kinds.items():
            print(f"     {kind}: {cases_to_str(ids)}")
            for cid in ids:
                f, ex = _first_match(raw, cid, SOURCE_FIELDS, SOURCE_PATTERNS[kind])
                rows.append({"category": category, "kind": kind, "case": cid, "supported": bool(ex), "field": f, "evidence_excerpt": ex})
                tag = {"Uncertainty Sources (verbatim)": "sources", "Applicability Conditions": "applicability", "Summary": "summary"}.get(f, "-")
                print(f"        {cid:<5} [{tag}] {ex[:95] or '-- no supporting text found --'}")
    pd.DataFrame(rows).to_csv(OUT / "rq2_sources_evidence.csv", index=False)

    # ---- 6.2.3 causal mechanisms: supporting text for every assigned case
    print("\n[6.2.3] Causal mechanisms: supporting text for each exemplar assigned to a mechanism")
    print("   (first matching field among: " + ", ".join(MECHANISM_FIELDS) + ")")
    mrows = []
    for mech, ids in MECHANISMS_623.items():
        print(f"\n   {mech}: {cases_to_str(ids)}")
        for cid in ids:
            f, ex = _first_match(raw, cid, MECHANISM_FIELDS, MECHANISM_PATTERNS[mech])
            mrows.append({"mechanism": mech, "case": cid, "supported": bool(ex), "field": f, "evidence_excerpt": ex})
            print(f"        {cid:<5} [{f or '-'}] {ex[:95] or '-- no supporting text found --'}")
    pd.DataFrame(mrows).to_csv(OUT / "rq2_mechanisms_evidence.csv", index=False)
    return {"span": span}


if __name__ == "__main__":
    run()
