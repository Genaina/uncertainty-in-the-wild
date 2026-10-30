"""RQ3 - Operational impacts and how they are characterised/assessed (Sec. 6.3)"""
import re
import pandas as pd
from common import load_raw, OUT, pct, cases_to_str, is_blank
from coding import code_impact, IMPACT_DIMS
from analyst_assignments import DOMAINS, TABLE7


def run(raw=None):
    raw = load_raw() if raw is None else raw
    n, dom = len(raw), raw["domain"]
    print("=" * 72, "\nRQ3 - Operational impacts\n" + "=" * 72)
    imp = code_impact(raw)
    imp.drop(columns=["dims"]).to_csv(OUT / "rq3_impact_coding_per_case.csv")

    # ---- 6.3.1 multi-dimensional vs generic/template
    cls = imp["impact_class"].value_counts()
    print("\n[6.3.1] Multi-dimensional vs generic/template impact (Sec. 3.4 rule #4):")
    for k, v in cls.items():
        print(f"   {k}: {v}/{n} = {pct(v, n)}")
    print("   Generic/Template cases:", cases_to_str(imp.index[imp.impact_class == "Generic/Template"]))
    print("   Rule: generic/template when the Impact field is explicitly marked as generic or template text.")
    for cid in imp.index[imp.impact_class == "Generic/Template"]:
        print(f"     {cid:<5} {str(raw.loc[cid, 'Impact']).strip()}")
    tab = pd.crosstab(dom, imp["impact_class"]).reindex(DOMAINS).fillna(0).astype(int)
    for c in ["Multi-dimensional", "Generic/Template"]:
        if c not in tab:
            tab[c] = 0
    tab = tab[["Multi-dimensional", "Generic/Template"]]
    tab.to_csv(OUT / "rq3_impact_class_by_domain.csv")
    print("\n[Tab.6] per domain:")
    print(tab.to_string())

    # ---- 6.3.2 affected quality dimensions (Tab.7)
    # Evidence per (case, dimension): the Impact field is the primary source; Trade-offs and Summary are
    # secondary sources (Table 7 is an analyst reading of the whole exemplar).
    patterns = {
        "Safety": r"safety|safely|collision|crash|safe mode|catastroph|false (?:alarm|positive)|\bsafe\b",
        "Performance": r"performance|latenc|response time|throughput|replanning|tracking|delay|number of adaptations",
        "Reliability & Availability": r"reliab|availab|downtime|telemetry|\bsla\b|disruption",
        "Mission Success": r"mission|task success|operational continuity",
        "Human Factors & Trust": r"fatigue|trust|workload|takeover|cognitive",
        "Resource Efficiency / Cost": r"\bcosts?\b|energy|resource|overhead|bandwidth|memory|computational|utili[sz]ation|sustainab",
    }
    sources = [("Impact", "impact"), ("Trade-offs", "trade-offs"), ("Summary", "summary")]
    rows = []
    for dim, pat in patterns.items():
        for cid in TABLE7.get(dim, []):
            support, excerpt = "none", ""
            for col, tag in sources:
                txt = raw.loc[cid, col]
                if is_blank(txt) or "left blank" in str(txt).lower() or "not provided" in str(txt).lower():
                    continue
                mm = re.search(pat, str(txt), re.I)
                if mm:
                    t = re.sub(r"\s+", " ", str(txt))
                    k = max(0, mm.start() - 40)
                    support, excerpt = tag, t[k:mm.end() + 60].strip()
                    break
            rows.append({"dimension": dim, "case": cid, "support": support, "evidence_excerpt": excerpt})
    ev = pd.DataFrame(rows)
    ev.to_csv(OUT / "rq3_quality_dimension_evidence.csv", index=False)
    print("\n[Tab.7] Affected quality dimensions: supporting text for each case assigned to a dimension")
    print("   Table 7 is an analyst reading of each exemplar. For every assigned case the report shows the text that supports it:")
    print("   'impact' = the Impact field itself (primary evidence); 'trade-offs' / 'summary' = secondary evidence.")
    summary = []
    print(f"\n   {'dimension':<28}{'assigned':>9}{'impact':>9}{'any field':>11}")
    for dim in patterns:
        d = ev[ev.dimension == dim]
        strong, weak, none = d[d.support == "impact"], d[d.support.isin(["trade-offs", "summary"])], d[d.support == "none"]
        n_c = len(d)
        print(f"   {dim:<28}{n_c:>9}{len(strong):>5} ({100 * len(strong) // max(1, n_c):>3}%){len(strong) + len(weak):>5} ({100 * (len(strong) + len(weak)) // max(1, n_c):>3}%)")
        summary.append({"dimension": dim, "n_assigned": n_c, "assigned_cases": cases_to_str(d.case),
                        "supported_by_impact": cases_to_str(strong.case),
                        "secondary_only": ", ".join(f"{r.case} ({r.support})" for r in weak.itertuples()),
                        "no_textual_evidence": cases_to_str(none.case)})
    print("\n   Supporting text per dimension:")
    for dim in patterns:
        print(f"\n   {dim}")
        for r in ev[ev.dimension == dim].itertuples():
            print(f"     {r.case:<5} [{r.support}] {r.evidence_excerpt[:100] or '-- no supporting text found --'}")
    pd.DataFrame(summary).to_csv(OUT / "rq3_quality_dimensions.csv", index=False)
    print("\n   Full excerpts: output/rq3_quality_dimension_evidence.csv")

    return imp


if __name__ == "__main__":
    run()
