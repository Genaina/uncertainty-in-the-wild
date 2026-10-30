"""RQ3 - Operational impacts and how they are characterised/assessed (Sec. 6.3)"""
import re
import pandas as pd
from common import load_raw, OUT, pct, by_domain, compare_sets, report_check, cases_to_str, is_blank
from coding import code_impact, IMPACT_DIMS
from paper_reported import DOMAINS, RQ3_TEXT, RQ3_TABLE6, RQ3_TABLE7


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
    for k in RQ3_TEXT:
        report_check(f"text {k}", RQ3_TEXT[k], int(cls.get(k, 0)))
    tab = pd.crosstab(dom, imp["impact_class"]).reindex(DOMAINS).fillna(0).astype(int)
    for c in ["Multi-dimensional", "Generic/Template"]:
        if c not in tab:
            tab[c] = 0
    tab = tab[["Multi-dimensional", "Generic/Template"]]
    tab.to_csv(OUT / "rq3_impact_class_by_domain.csv")
    print("\n[Tab.6] per domain (computed):")
    print(tab.to_string())
    for d in DOMAINS:
        c = (int(tab.loc[d, "Multi-dimensional"]), int(tab.loc[d, "Generic/Template"]))
        if c != RQ3_TABLE6[d]:
            report_check(f"Tab.6 {d}", RQ3_TABLE6[d], c)
    print(f"   Table 6 sums to: multi={sum(a for a, _ in RQ3_TABLE6.values())}, "
          f"generic={sum(b for _, b in RQ3_TABLE6.values())} (text says 15 / 3)")

    # ---- 6.3.2 affected quality dimensions (Tab.7)
    # Evidence per (case, dimension): the Impact field is the primary source; Trade-offs and Summary are
    # secondary sources (the paper's Table 7 is an analyst reading of the whole exemplar).
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
    for cid in raw.index:
        for dim, pat in patterns.items():
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
            rows.append({"ID": cid, "dimension": dim, "in_paper_table7": cid in RQ3_TABLE7.get(dim, []),
                         "support": support, "evidence_excerpt": excerpt})
    ev = pd.DataFrame(rows)
    ev.to_csv(OUT / "rq3_quality_dimension_evidence.csv", index=False)
    print("\n[Tab.7] Affected quality dimensions: evidence in the verbatim text")
    print("   Table 7 is an analyst reading of each exemplar. For every dimension the script lists the cases cited in the paper")
    print("   and what the text supports: 'impact' = the Impact field itself; 'trade-offs'/'summary' = secondary evidence.")
    summary = []
    print("\n   Agreement with Table 7, per dimension. Table 7 lists *supporting* (representative) cases, not every case that")
    print("   shows the dimension, so the relevant measure is coverage = share of the CITED cases that the text supports.")
    print(f"   {'dimension':<28}{'cited':>6}{'impact':>9}{'any field':>11}")
    for dim in patterns:
        d = ev[ev.dimension == dim]
        cited = d[d.in_paper_table7]
        strong = cited[cited.support == "impact"]
        weak = cited[cited.support.isin(["trade-offs", "summary"])]
        none = cited[cited.support == "none"]
        extra_strong = d[~d.in_paper_table7 & (d.support == "impact")]
        extra_weak = d[~d.in_paper_table7 & d.support.isin(["trade-offs", "summary"])]
        n_c = len(cited)
        print(f"   {dim:<28}{n_c:>6}{len(strong):>5} ({100 * len(strong) // max(1, n_c):>3}%){len(strong) + len(weak):>5} ({100 * (len(strong) + len(weak)) // max(1, n_c):>3}%)")
        summary.append({"dimension": dim, "n_cited_in_paper": n_c, "cited_in_paper": cases_to_str(cited.ID),
                        "cited_supported_by_impact": len(strong), "cited_supported_by_any_field": len(strong) + len(weak),
                        "coverage_impact": round(len(strong) / max(1, n_c), 2),
                        "coverage_any_field": round((len(strong) + len(weak)) / max(1, n_c), 2),
                        "cited_impact_support": cases_to_str(strong.ID),
                        "cited_secondary_only": ", ".join(f"{r.ID} ({r.support})" for r in weak.itertuples()),
                        "cited_no_evidence": cases_to_str(none.ID),
                        "not_cited_impact_support": cases_to_str(extra_strong.ID),
                        "not_cited_secondary_only": ", ".join(f"{r.ID} ({r.support})" for r in extra_weak.itertuples())})
    print("\n   Case lists per dimension (impact = supported by the Impact field; secondary = Trade-offs/Summary):")
    for row in summary:
        print(f"\n   {row['dimension']}  (cited in paper: {row['cited_in_paper']})")
        print(f"     cited, supported by the Impact field : {row['cited_impact_support'] or '-'}")
        print(f"     cited, secondary evidence only       : {row['cited_secondary_only'] or '-'}")
        print(f"     cited, NO textual evidence           : {row['cited_no_evidence'] or '-'}")
        print(f"     not cited, Impact field supports it  : {row['not_cited_impact_support'] or '-'}")
        print(f"     not cited, secondary evidence only   : {row['not_cited_secondary_only'] or '-'}")
    pd.DataFrame(summary).to_csv(OUT / "rq3_quality_dimensions.csv", index=False)
    print("\n   Full excerpts: output/rq3_quality_dimension_evidence.csv")

    return imp


if __name__ == "__main__":
    run()
