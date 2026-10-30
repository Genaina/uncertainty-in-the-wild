"""RQ1 - What types of uncertainty interactions are observed? (Sec. 6.1)

Outputs: output/rq1_*.csv, output/rq1_fig_domains.png, output/rq1_fig_categories.png
The reference coding of the interaction categories is the manual coding in
data/manual_interaction_counts.csv; the rule-based coder is used as a cross-check.
"""
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from common import load_raw, OUT, BASE, pct, by_domain, report_check, cases_to_str
from coding import code_interactions, interaction_flags, code_nature, CATS
from paper_reported import DOMAINS, RQ1_TEXT, RQ1_NATURE_TEXT, RQ1_FIG3, RQ1_TABLE4


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
    print("\n[6.1.1] Interaction categories (count per exemplar), 3 automatic coding criteria (cross-check only; the reference is the manual coding below):")
    print("   strict  = explicit contributor evidence only")
    print("   lenient = + tentative marks '(?)' / '(Possible)'")
    print("   paper   = + template-only answers (label without content) counted as present")
    tbl = {}
    for mode in ["strict", "lenient", "paper"]:
        tbl[mode] = interaction_flags(coded, mode).sum()
    tbl = pd.DataFrame(tbl)
    print(tbl.to_string())
    tbl.to_csv(OUT / "rq1_category_counts.csv")

    # ---- MANUAL CODING (data/manual_interaction_counts.csv) -> reference coding
    man = pd.read_csv(BASE / "data" / "manual_interaction_counts.csv").set_index("ID")
    tmpl = man["template_only"] == 1
    mflags = man[CATS] > 0
    print(f"\n[MANUAL] Per-exemplar counts from the manual coding (n = {n}).")
    print(f"   Template-only answers kept in the counts (flagged, no case-specific text): {cases_to_str(man.index[tmpl])}")
    for c in CATS:
        k = int(mflags[c].sum())
        print(f"   {c:<13} {k:>2}/{n} = {pct(k, n)}   (manuscript text = {RQ1_TEXT[c]}/18)")
        report_check(f"manual vs manuscript text: {c}", RQ1_TEXT[c], k)
    ex = mflags[~tmpl]
    print(f"   Sensitivity -- excluding the template-only cases (n = {len(ex)}): " +
          ", ".join(f"{c} {int(ex[c].sum())}/{len(ex)}" for c in CATS))
    auto = interaction_flags(coded, "paper")
    print("   Cases where the automatic rule ('paper' criterion) differs from the sheet:")
    for c in CATS:
        diff = cases_to_str(mflags.index[mflags[c] != auto[c]])
        print(f"     {c:<13} {diff or '-'}")
    mflags.to_csv(OUT / "rq1_manual_flags.csv")
    f = mflags   # the manual coding is used in the tables/figures below

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
    print("   (layers: explicit text -> tentative mark -> template-only; the manuscript number is their union)")
    consistent = True
    for c in CATS:
        sub = evdf[(evdf.category == c) & evdf.counted]
        layers = {k: cases_to_str(sub.ID[sub.text_support == k]) for k in label.values()}
        counted = cases_to_str(sub.ID)
        n_ = {k: int((sub.text_support == k).sum()) for k in label.values()}
        print(f"\n   {c.upper()}  {len(sub)}/{n} counted: {counted}")
        print(f"     explicit text   ({n_['explicit text']:>2}): {layers['explicit text'] or '-'}")
        print(f"     tentative mark  ({n_['tentative mark']:>2}): {layers['tentative mark'] or '-'}")
        print(f"     template-only   ({n_['template-only']:>2}): {layers['template-only'] or '-'}")
        if n_["no evidence"]:
            consistent = False
            print(f"     NO TEXT SUPPORT ({n_['no evidence']:>2}): {layers['no evidence']}   <-- counted in the manual coding without textual support")
        for _, r_ in sub.iterrows():
            ex = r_.evidence_excerpt
            print(f"       {r_.ID:<5} [{r_.text_support}] {ex[:110]}{'...' if len(ex) > 110 else ''}")
        missed = evdf[(evdf.category == c) & ~evdf.counted & (evdf.text_support.isin(["explicit text", "tentative mark"]))]
        if len(missed):
            consistent = False
            print(f"     TEXT SUPPORT BUT NOT COUNTED: {cases_to_str(missed.ID)}")
    print("\n   Manual coding fully explained by the text (explicit + tentative + template-only):", consistent)
    print("   Full excerpts: output/rq1_interaction_evidence.csv")

    # ---- by domain (Fig. 3)
    per_dom = pd.DataFrame({c: by_domain(f[c], dom.loc[f.index], DOMAINS) for c in CATS})
    print("\n[Fig.3] Categories per domain (manual coding):")
    print(per_dom.to_string())
    per_dom.to_csv(OUT / "rq1_category_by_domain.csv")
    print("\n   Validation against the pgfplots data of Fig. 3 (only differences are listed):")
    for c in ["dominance", "conflict", "augmentation"]:
        for d in DOMAINS:
            if per_dom.loc[d, c] != RQ1_FIG3[c][d]:
                report_check(f"{c}/{d}", RQ1_FIG3[c][d], int(per_dom.loc[d, c]))

    # ---- co-occurrence of categories
    k = f[["dominance", "conflict", "augmentation"]].sum(axis=1)
    print("\n   Cases with all 3 categories:", int((k == 3).sum()),
          "| 2:", int((k == 2).sum()), "| 1:", int((k == 1).sum()), "| 0:", int((k == 0).sum()))

    # ---- 6.1.2 interaction nature
    nat = code_nature(raw)
    nat_tbl = pd.crosstab(dom, nat).reindex(DOMAINS).fillna(0).astype(int)
    for col in ["Heterogeneous", "Homogeneous/Mixed"]:
        if col not in nat_tbl:
            nat_tbl[col] = 0
    nat_tbl = nat_tbl[["Heterogeneous", "Homogeneous/Mixed"]]
    print("\n[6.1.2 / Tab.4] Interaction nature per domain (computed):")
    print(nat_tbl.to_string())
    tot = nat.value_counts()
    for k_, v in tot.items():
        print(f"   {k_}: {v}/{n} = {pct(v, n)}")
    print("   Homogeneous/Mixed:", ", ".join(nat[nat == 'Homogeneous/Mixed'].index))
    nat_tbl.to_csv(OUT / "rq1_nature_by_domain.csv")
    print("   Validation against the Table 4 / text:")
    for d in DOMAINS:
        p = RQ1_TABLE4[d]
        c = (int(nat_tbl.loc[d, "Heterogeneous"]), int(nat_tbl.loc[d, "Homogeneous/Mixed"]))
        if p != c:
            report_check(f"Tab.4 {d}", p, c)
    for k_ in RQ1_NATURE_TEXT:
        report_check(f"text {k_}", RQ1_NATURE_TEXT[k_], int(tot.get(k_, 0)))
    print(f"   Table 4 sums to: {sum(a for a, _ in RQ1_TABLE4.values())} het + "
          f"{sum(b for _, b in RQ1_TABLE4.values())} hom = "
          f"{sum(a + b for a, b in RQ1_TABLE4.values())} (expected 18)")

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
