"""RQ3 - Impactos operacionais e como sao caracterizados/avaliados (Sec. 6.3)"""
import pandas as pd
from common import load_raw, OUT, pct, by_domain, compare_sets, report_check, cases_to_str
from coding import code_impact, IMPACT_DIMS
from paper_reported import DOMAINS, RQ3_TEXT, RQ3_TABLE6, RQ3_TABLE7


def run(raw=None):
    raw = load_raw() if raw is None else raw
    n, dom = len(raw), raw["domain"]
    print("=" * 72, "\nRQ3 - Impactos operacionais\n" + "=" * 72)
    imp = code_impact(raw)
    imp.drop(columns=["dims"]).to_csv(OUT / "rq3_impact_coding_per_case.csv")

    # ---- 6.3.1 multi-dimensional vs generico/template
    cls = imp["impact_class"].value_counts()
    print("\n[6.3.1] Impacto multi-dimensional vs generico/template (regra Sec. 3.4 #4):")
    for k, v in cls.items():
        print(f"   {k}: {v}/{n} = {pct(v, n)}")
    print("   Generico/Template:", cases_to_str(imp.index[imp.impact_class == "Generic/Template"]))
    for k in RQ3_TEXT:
        report_check(f"texto {k}", RQ3_TEXT[k], int(cls.get(k, 0)))
    tab = pd.crosstab(dom, imp["impact_class"]).reindex(DOMAINS).fillna(0).astype(int)
    for c in ["Multi-dimensional", "Generic/Template"]:
        if c not in tab:
            tab[c] = 0
    tab = tab[["Multi-dimensional", "Generic/Template"]]
    tab.to_csv(OUT / "rq3_impact_class_by_domain.csv")
    print("\n[Tab.6] por dominio (calculado):")
    print(tab.to_string())
    for d in DOMAINS:
        c = (int(tab.loc[d, "Multi-dimensional"]), int(tab.loc[d, "Generic/Template"]))
        if c != RQ3_TABLE6[d]:
            report_check(f"Tab.6 {d}", RQ3_TABLE6[d], c)
    print(f"   Soma Tab.6 impressa: multi={sum(a for a, _ in RQ3_TABLE6.values())}, "
          f"generico={sum(b for _, b in RQ3_TABLE6.values())} (texto diz 15 / 3)")

    # ---- 6.3.2 dimensoes de qualidade afetadas (Tab.7)
    print("\n[Tab.7] Dimensoes de qualidade afetadas -- palavras-chave sobre o campo Impact")
    print("   (Tab.7 do paper e analyst-derived; aqui mostramos o que o TEXTO bruto sustenta)")
    rows = []
    for d in IMPACT_DIMS:
        got = {c for c, ds in imp["dims"].items() if d in ds}
        paper = set(RQ3_TABLE7.get(d, []))
        j = len(got & paper) / max(1, len(got | paper))
        rows.append({"dimension": d, "n_text": len(got), "n_paper": len(paper),
                     "jaccard": round(j, 2), "text_cases": cases_to_str(got),
                     "paper_cases": cases_to_str(paper)})
        print(f"   {d:<28} texto={len(got):>2}  paper={len(paper):>2}  Jaccard={j:.2f}")
        print(f"      citados no paper sem evidencia textual: {cases_to_str(paper - got) or '-'}")
    pd.DataFrame(rows).to_csv(OUT / "rq3_quality_dimensions.csv", index=False)

    nd = imp["n_dims"]
    print(f"\n   Qualidades distintas por caso (palavras-chave): media={nd.mean():.1f}, "
          f"casos com >=2: {(nd >= 2).sum()}/{n}")
    return imp


if __name__ == "__main__":
    run()
