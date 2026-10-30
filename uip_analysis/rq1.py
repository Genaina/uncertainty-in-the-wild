"""RQ1 - What types of uncertainty interactions are observed? (Sec. 6.1)

Outputs: output/rq1_*.csv, output/rq1_fig_domains.png, output/rq1_fig_categories.png
The reference coding of the interaction categories is the manual coding in
data/manual_interaction_counts.csv; the rule-based coder is used as a cross-check, and the report prints
the verbatim text that supports each code.
"""
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from common import load_raw, OUT, BASE, pct, by_domain, cases_to_str
from coding import code_interactions, interaction_flags, code_nature, CATS
from analyst_assignments import DOMAINS


def run(raw=None):
    raw = load_raw() if raw is None else raw
    n = len(raw)
    dom = raw["domain"]
    coded = code_interactions(raw)
    coded.to_csv(OUT / "rq1_interaction_coding_per_case.csv")

    print("=" * 72, "\nRQ1 - Types of uncertainty interaction\n" + "=" * 72)

    # ---- domain distribution (Fig. 1)
    dcount = dom.value_counts().reindex(DOMAINS)
    print("\n[Fig.1] Cases per domain:")
    for d, c in dcount.items():
        print(f"   {d:<12} {c:>2}  ({pct(c, n)})")
    dcount.to_csv(OUT / "rq1_domain_distribution.csv", header=["cases"])

    # ---- 6.1.1 interaction categories (exemplar level; Sec. 3.4 rule 1)
    print("\n[6.1.1] Interaction categories, automatic cross-check (count per exemplar):")
    print("   strict  = explicit case-specific text only")
    print("   lenient = + tentative marks '(?)' / '(Possible)'")
    print("   full    = + template-only answers (label without content) counted as present")
    tbl = pd.DataFrame({mode: interaction_flags(coded, mode).sum() for mode in ["strict", "lenient", "full"]})
    print(tbl.to_string())
    tbl.to_csv(OUT / "rq1_category_counts.csv")

    # ---- MANUAL CODING (data/manual_interaction_counts.csv) -> reference coding
    man = pd.read_csv(BASE / "data" / "manual_interaction_counts.csv").set_index("ID")
    tmpl = man["template_only"] == 1
    mflags = man[CATS] > 0
    print(f"\n[MANUAL] Per-exemplar counts from the manual coding (n = {n}):")
    for c in CATS:
        k = int(mflags[c].sum())
        print(f"   {c:<13} {k:>2}/{n} = {pct(k, n)}")
    print(f"   Template-only answers kept in the counts (flagged, no case-specific text): {cases_to_str(man.index[tmpl])}")
    ex = mflags[~tmpl]
    print(f"   Sensitivity -- excluding the template-only cases (n = {len(ex)}): " +
          ", ".join(f"{c} {int(ex[c].sum())}/{len(ex)}" for c in CATS))
    auto = interaction_flags(coded, "full")
    agree = all((mflags[c] == auto[c]).all() for c in CATS)
    print(f"   Cross-check: the automatic 'full' rule reproduces the manual coding for every exemplar and category: {agree}")
    if not agree:
        for c in CATS:
            print(f"     differs for {c}: {cases_to_str(mflags.index[mflags[c] != auto[c]]) or '-'}")
    mflags.to_csv(OUT / "rq1_manual_flags.csv")
    f = mflags

    # ---- EVIDENCE: which verbatim text supports each manual code
    _, evid = code_interactions(raw, return_evidence=True)
    label = {"explicit": "explicit text", "tentative": "tentative mark", "template": "template-only", "": "no evidence"}
    rows = []
    for cid in man.index:
        for c in CATS:
            rows.append({"ID": cid, "domain": dom[cid], "category": c, "manual_code": int(man.loc[cid, c]),
                         "counted": bool(mflags.loc[cid, c]), "text_support": label[coded.loc[cid, c]],
                         "evidence_excerpt": evid[(cid, c)]})
    evdf = pd.DataFrame(rows)
    evdf.to_csv(OUT / "rq1_interaction_evidence.csv", index=False)
    print("\n[EVIDENCE] How each manual count is supported by the verbatim text")
    print("   (layers: explicit text -> tentative mark -> template-only; the count is their union)")
    consistent = True
    for c in CATS:
        sub = evdf[(evdf.category == c) & evdf.counted]
        n_ = {k: int((sub.text_support == k).sum()) for k in label.values()}
        print(f"\n   {c.upper()}  {len(sub)}/{n} counted: {cases_to_str(sub.ID)}")
        for k in ["explicit text", "tentative mark", "template-only"]:
            print(f"     {k:<15} ({n_[k]:>2}): {cases_to_str(sub.ID[sub.text_support == k]) or '-'}")
        if n_["no evidence"]:
            consistent = False
            print(f"     NO TEXT SUPPORT ({n_['no evidence']:>2}): {cases_to_str(sub.ID[sub.text_support == 'no evidence'])}")
        for _, r_ in sub.iterrows():
            e = r_.evidence_excerpt
            print(f"       {r_.ID:<5} [{r_.text_support}] {e[:110]}{'...' if len(e) > 110 else ''}")
        missed = evdf[(evdf.category == c) & ~evdf.counted & (evdf.text_support.isin(["explicit text", "tentative mark"]))]
        if len(missed):
            consistent = False
            print(f"     TEXT SUPPORT BUT NOT COUNTED: {cases_to_str(missed.ID)}")
    print("\n   Every manual code is explained by the text (explicit + tentative + template-only):", consistent)
    print("   Full excerpts: output/rq1_interaction_evidence.csv")

    # ---- by domain (Fig. 3)
    per_dom = pd.DataFrame({c: by_domain(f[c], dom.loc[f.index], DOMAINS) for c in CATS})
    print("\n[Fig.3] Categories per domain (manual coding):")
    print(per_dom.to_string())
    per_dom.to_csv(OUT / "rq1_category_by_domain.csv")

    # ---- co-occurrence of categories
    k = f[["dominance", "conflict", "augmentation"]].sum(axis=1)
    print("\n   Exemplars with all 3 of dominance/conflict/augmentation:", int((k == 3).sum()),
          "| 2:", int((k == 2).sum()), "| 1:", int((k == 1).sum()), "| 0:", int((k == 0).sum()))

    # ---- 6.1.2 interaction nature
    nat = code_nature(raw)
    nat_tbl = pd.crosstab(dom, nat).reindex(DOMAINS).fillna(0).astype(int)
    for col in ["Heterogeneous", "Homogeneous/Mixed"]:
        if col not in nat_tbl:
            nat_tbl[col] = 0
    nat_tbl = nat_tbl[["Heterogeneous", "Homogeneous/Mixed"]]
    print("\n[6.1.2 / Tab.4] Interaction nature per domain:")
    print(nat_tbl.to_string())
    for k_, v in nat.value_counts().items():
        print(f"   {k_}: {v}/{n} = {pct(v, n)}")
    print("   Homogeneous/Mixed:", ", ".join(nat[nat == 'Homogeneous/Mixed'].index))
    nat_tbl.to_csv(OUT / "rq1_nature_by_domain.csv")

    # ---- figures
    fig, ax = plt.subplots(figsize=(7, 3.6))
    per_dom[["dominance", "conflict", "augmentation"]].plot(kind="bar", ax=ax, width=0.8)
    ax.set_ylabel("Number of case studies"); ax.set_xlabel("")
    plt.xticks(rotation=35, ha="right"); plt.tight_layout()
    fig.savefig(OUT / "rq1_fig_categories.png", dpi=200); plt.close(fig)

    fig, ax = plt.subplots(figsize=(5, 4))
    ax.pie(dcount.values, labels=[f"{d} ({c})" for d, c in dcount.items()],
           autopct=lambda p: f"{p:.1f}%", startangle=90)
    plt.tight_layout(); fig.savefig(OUT / "rq1_fig_domains.png", dpi=200); plt.close(fig)
    return {"coded": coded, "per_domain": per_dom, "nature": nat}


if __name__ == "__main__":
    run()
