"""RQ2 - Which uncertainty sources, system elements, abstraction levels and causal mechanisms participate? (Sec. 6.2)"""
import pandas as pd
from common import load_raw, OUT, pct, cases_to_str
from coding import code_abstraction, code_sources, code_mechanisms
from analyst_assignments import DOMAINS


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
        print(f"     {cid:<5} {t if t.lower() != 'nan' else '(empty field)'}")

    # ---- 6.2.2 sources (type and category) -- keyword heuristic
    types, cats = code_sources(raw)
    print("\n[6.2.2] Sources by CATEGORY (cases that mention it; keyword heuristic):")
    cc = cats.sum().sort_values(ascending=False)
    for k, v in cc.items():
        print(f"   {k:<22} {v:>2}/{n}  {cases_to_str(cats.index[cats[k]])}")
    print("\n   Sources by TYPE (nature):")
    tc = types.sum().sort_values(ascending=False)
    for k, v in tc.items():
        print(f"   {k:<22} {v:>2}/{n}  {cases_to_str(types.index[types[k]])}")
    cats.to_csv(OUT / "rq2_source_categories_per_case.csv")
    types.to_csv(OUT / "rq2_source_types_per_case.csv")
    pd.concat([cc.rename("categoria"), tc.rename("tipo")]).to_csv(OUT / "rq2_source_counts.csv", header=["cases"])

    # ---- co-occurrence of source categories (most frequent pairs)
    pairs = {}
    for cid, r in cats.iterrows():
        on = [k for k, v in r.items() if v]
        for i in range(len(on)):
            for j in range(i + 1, len(on)):
                pairs[(on[i], on[j])] = pairs.get((on[i], on[j]), 0) + 1
    print("\n   Pairs of source categories that most often co-occur in the same case:")
    for (a, b), v in sorted(pairs.items(), key=lambda x: -x[1])[:8]:
        print(f"   {a} x {b}: {v}")

    # ---- 6.2.3 causal mechanisms
    mech = code_mechanisms(raw)
    mech.to_csv(OUT / "rq2_mechanisms_per_case.csv")
    print("\n[6.2.3] Causal mechanisms: cases whose interaction, impact, trade-off or abstraction text shows the mechanism (keyword search):")
    for m in mech.columns:
        got = mech.index[mech[m]]
        print(f"   {m:<22} {len(got):>2}/{n}  {cases_to_str(got)}")
    return {"span": span, "cats": cats, "types": types, "mech": mech}


if __name__ == "__main__":
    run()
