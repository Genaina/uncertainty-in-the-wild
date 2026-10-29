"""RQ1 - Que tipos de interacao de incerteza ocorrem? (Sec. 6.1)

Saidas: output/rq1_*.csv, output/rq1_fig_domains.png, output/rq1_fig_categories.png
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

    print("=" * 72, "\nRQ1 - Tipos de interacao de incerteza\n" + "=" * 72)

    # ---- 6.1.0 distribuicao por dominio (Fig. 1)
    dcount = dom.value_counts().reindex(DOMAINS)
    print("\n[Fig.1] Casos por dominio:")
    for d, c in dcount.items():
        print(f"   {d:<12} {c:>2}  ({pct(c, n)})")
    dcount.to_csv(OUT / "rq1_domain_distribution.csv", header=["cases"])

    # ---- 6.1.1 categorias de interacao (nivel de exemplar; Sec. 3.4 regra 1)
    print("\n[6.1.1] Categorias de interacao (contagem por exemplar), 3 criterios de codificacao:")
    print("   strict  = so evidencia explicita do contribuidor")
    print("   lenient = + marcacoes tentativas '(?)' / '(Possible)' / '(dominant)'")
    print("   paper   = + respostas so-template (rotulo sem conteudo) contadas como presentes")
    tbl = {}
    for mode in ["strict", "lenient", "paper"]:
        f = interaction_flags(coded, mode)
        tbl[mode] = f.sum()
    tbl = pd.DataFrame(tbl)
    tbl["paper_text"] = pd.Series(RQ1_TEXT)
    tbl["fig3_total"] = pd.Series({k: sum(v.values()) for k, v in RQ1_FIG3.items()})
    print(tbl.to_string())
    print(f"\n   Percentuais (criterio 'paper', n={n}):")
    for c in CATS:
        print(f"   {c:<13} {tbl.loc[c, 'paper']:>2}/{n} = {pct(tbl.loc[c, 'paper'], n)}")
    tbl.to_csv(OUT / "rq1_category_counts.csv")

    # ---- CODIFICACAO MANUAL (planilha do autor) -> fonte de verdade
    man = pd.read_csv(BASE / "data" / "manual_interaction_counts.csv").set_index("ID")
    mflags = man[CATS] > 0
    print("\n[MANUAL] Contagem por exemplar a partir da planilha do autor:")
    for c in CATS:
        print(f"   {c:<13} {int(mflags[c].sum()):>2}/{n} = {pct(int(mflags[c].sum()), n)}   "
              f"(paper texto={RQ1_TEXT[c]})")
        report_check(f"manual vs texto: {c}", RQ1_TEXT[c], int(mflags[c].sum()))
    agree = {c: cases_to_str(mflags.index[mflags[c] != interaction_flags(coded, 'paper')[c]]) for c in CATS}
    print("   Casos em que a regra automatica ('paper') difere da planilha:")
    for c in CATS:
        print(f"     {c:<13} {agree[c] or '-'}")
    mflags.to_csv(OUT / "rq1_manual_flags.csv")
    f = mflags   # usa a planilha manual nas tabelas/figuras abaixo
    per_dom = pd.DataFrame({c: by_domain(f[c], dom, DOMAINS) for c in CATS})
    print("\n[Fig.3] Categorias por dominio (planilha manual):")
    print(per_dom.to_string())
    per_dom.to_csv(OUT / "rq1_category_by_domain.csv")
    print("\n   Validacao contra dados do pgfplots da Fig. 3:")
    for c in ["dominance", "conflict", "augmentation"]:
        for d in DOMAINS:
            if per_dom.loc[d, c] != RQ1_FIG3[c][d]:
                report_check(f"{c}/{d}", RQ1_FIG3[c][d], int(per_dom.loc[d, c]))
    print("   (so divergencias sao listadas acima)")
    print("   Validacao contra o TEXTO da Sec. 6.1.1:")
    for c in CATS:
        report_check(c, RQ1_TEXT[c], int(mflags[c].sum()))

    # ---- co-ocorrencia de categorias
    k = f[["dominance", "conflict", "augmentation"]].sum(axis=1)
    print("\n   Casos com 3 categorias simultaneas:", int((k == 3).sum()),
          "| 2:", int((k == 2).sum()), "| 1:", int((k == 1).sum()), "| 0:", int((k == 0).sum()))

    # ---- 6.1.2 natureza da interacao
    nat = code_nature(raw)
    nat_tbl = pd.crosstab(dom, nat).reindex(DOMAINS).fillna(0).astype(int)
    for col in ["Heterogeneous", "Homogeneous/Mixed"]:
        if col not in nat_tbl:
            nat_tbl[col] = 0
    nat_tbl = nat_tbl[["Heterogeneous", "Homogeneous/Mixed"]]
    print("\n[6.1.2 / Tab.4] Natureza da interacao por dominio (calculado):")
    print(nat_tbl.to_string())
    tot = nat.value_counts()
    for k_, v in tot.items():
        print(f"   {k_}: {v}/{n} = {pct(v, n)}")
    print("   Homogeneous/Mixed:", ", ".join(nat[nat == 'Homogeneous/Mixed'].index))
    nat_tbl.to_csv(OUT / "rq1_nature_by_domain.csv")
    print("   Validacao Tab.4 / texto:")
    for d in DOMAINS:
        p = RQ1_TABLE4[d]
        c = (int(nat_tbl.loc[d, "Heterogeneous"]), int(nat_tbl.loc[d, "Homogeneous/Mixed"]))
        if p != c:
            report_check(f"Tab.4 {d}", p, c)
    for k_ in RQ1_NATURE_TEXT:
        report_check(f"texto {k_}", RQ1_NATURE_TEXT[k_], int(tot.get(k_, 0)))
    print(f"   Soma da Tab.4 no manuscrito: {sum(a for a, _ in RQ1_TABLE4.values())} het + "
          f"{sum(b for _, b in RQ1_TABLE4.values())} hom = "
          f"{sum(a + b for a, b in RQ1_TABLE4.values())} (esperado 18)")

    # ---- figuras
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
