"""RQ3 - Operational impacts and how they are characterised/assessed (Sec. 6.3)"""
import pandas as pd
from common import load_raw, OUT, pct, by_domain, compare_sets, report_check, cases_to_str
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
    print(f"   Original Table 6 sums to: multi={sum(a for a, _ in RQ3_TABLE6.values())}, "
          f"generic={sum(b for _, b in RQ3_TABLE6.values())} (text says 15 / 3)")

    # ---- 6.3.2 affected quality dimensions (Tab.7)
    print("\n[Tab.7] Affected quality dimensions -- keywords over the Impact field")
    print("   (Table 7 of the paper is analyst-derived; here we show what the RAW text supports)")
    rows = []
    for d in IMPACT_DIMS:
        got = {c for c, ds in imp["dims"].items() if d in ds}
        paper = set(RQ3_TABLE7.get(d, []))
        j = len(got & paper) / max(1, len(got | paper))
        rows.append({"dimension": d, "n_text": len(got), "n_paper": len(paper),
                     "jaccard": round(j, 2), "text_cases": cases_to_str(got),
                     "paper_cases": cases_to_str(paper)})
        print(f"   {d:<28} text={len(got):>2}  paper={len(paper):>2}  Jaccard={j:.2f}")
        print(f"      cited in the paper without textual evidence: {cases_to_str(paper - got) or '-'}")
    pd.DataFrame(rows).to_csv(OUT / "rq3_quality_dimensions.csv", index=False)

    nd = imp["n_dims"]
    print(f"\n   Distinct qualities per case (keywords): mean={nd.mean():.1f}, "
          f"cases with >=2: {(nd >= 2).sum()}/{n}")
    return imp


if __name__ == "__main__":
    run()
