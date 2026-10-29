"""RQ4 - Mecanismos de deteccao/representacao/analise/prevencao/mitigacao e condicoes (Sec. 6.4)"""
import pandas as pd
from common import load_raw, OUT, pct, compare_sets, cases_to_str
from coding import (code_preparedness, code_strategy, code_lifecycle, code_applicability,
                    code_tradeoffs)
from paper_reported import (RQ4_TABLE8, RQ4_TABLE9, RQ4_TABLE10, RQ4_TABLE11, RQ4_TABLE12)


def _compare_table(title, computed: pd.DataFrame, paper: dict, n, rename=None):
    print(f"\n{title}")
    rows = []
    for dim in paper:
        col = (rename or {}).get(dim, dim)
        got = set(computed.index[computed[col]]) if col in computed else set()
        pap = set(paper[dim])
        j = len(got & pap) / max(1, len(got | pap))
        rows.append({"dimension": dim, "n_calc": len(got), "n_paper": len(pap), "jaccard": round(j, 2),
                     "calc_cases": cases_to_str(got), "paper_cases": cases_to_str(pap)})
        compare_sets(f"{dim} (calc={len(got)}, paper={len(pap)})", pap, got)
    return pd.DataFrame(rows)


def run(raw=None):
    raw = load_raw() if raw is None else raw
    n = len(raw)
    print("=" * 72, "\nRQ4 - Solution space\n" + "=" * 72)

    # ---- 6.4.1 preparedness (Tab.8)
    prep = code_preparedness(raw)
    prep.to_csv(OUT / "rq4_preparedness_per_case.csv")
    print("\n[Tab.8] Preparedness -- n de casos com a capacidade reportada (calculado):")
    for k, v in prep.sum().sort_values(ascending=False).items():
        print(f"   {k:<15} {v:>2}/{n} = {pct(v, n)}")
    reported = raw["Level of Preparedness"].map(lambda t: isinstance(t, str) and "blank" not in t.lower()[:12])
    print(f"   Casos que preencheram o campo Preparedness: {int(reported.sum())}/{n} "
          f"(ausentes: {cases_to_str(raw.index[~reported])})")
    t8 = _compare_table("   Comparacao com a Tab.8 do paper:", prep, RQ4_TABLE8, n)
    t8.to_csv(OUT / "rq4_table8_comparison.csv", index=False)

    # ---- 6.4.5 strategy (Tab.12)
    strat = code_strategy(raw)
    strat.to_csv(OUT / "rq4_strategy_per_case.csv")
    print("\n[Tab.12] Strategy -- casos com estrategia reportada (calculado):")
    for k, v in strat.sum().items():
        print(f"   {k:<15} {v:>2}/{n}")
    t12 = _compare_table("   Comparacao com a Tab.12 do paper:", strat, RQ4_TABLE12, n)
    t12.to_csv(OUT / "rq4_table12_comparison.csv", index=False)

    # ---- 6.4.3 lifecycle
    life = code_lifecycle(raw)
    life.to_csv(OUT / "rq4_lifecycle_per_case.csv", header=["lifecycle"])
    print("\n[6.4.3] Lifecycle stage (campo bruto):")
    for k, v in life.value_counts().items():
        print(f"   {k:<13} {v:>2}/{n}  {cases_to_str(life.index[life == k])}")
    rep = life[life != "not reported"]
    print(f"   Entre os {len(rep)} casos que reportam: both = {(rep == 'both').sum()}, "
          f"runtime-only = {(rep == 'runtime').sum()}, design-only = {(rep == 'design-time').sum()}")
    print("   Tab.10 (atividades de ciclo de vida) e analyst-derived; contagens do paper:")
    for k, v in RQ4_TABLE10.items():
        print(f"   {k:<26} {len(v):>2} casos")

    # ---- 6.4.2 applicability (Tab.9) -- referencia = paper; cross-check por palavra-chave
    app = code_applicability(raw)
    app.to_csv(OUT / "rq4_applicability_keywords_per_case.csv")
    t9 = _compare_table("\n[Tab.9] Applicability conditions (cross-check por palavras-chave; "
                        "referencia = analise manual do paper):", app, RQ4_TABLE9, n)
    t9.to_csv(OUT / "rq4_table9_comparison.csv", index=False)
    filled = raw["Applicability Conditions"].map(lambda t: isinstance(t, str) and
                                                 "blank" not in t.lower()[:12] and "not provided" not in t.lower())
    print(f"   Casos com campo Applicability preenchido: {int(filled.sum())}/{n}")

    # ---- 6.4.4 trade-offs (Tab.11)
    tr = code_tradeoffs(raw)
    tr.to_csv(OUT / "rq4_tradeoffs_keywords_per_case.csv")
    t11 = _compare_table("\n[Tab.11] Trade-offs (cross-check por palavras-chave):", tr, RQ4_TABLE11, n)
    t11.to_csv(OUT / "rq4_table11_comparison.csv", index=False)
    filled_t = raw["Trade-offs"].map(lambda t: isinstance(t, str) and
                                     "blank" not in t.lower()[:12] and "not provided" not in t.lower())
    print(f"   Casos com campo Trade-offs preenchido: {int(filled_t.sum())}/{n} "
          f"(sem preenchimento: {cases_to_str(raw.index[~filled_t])})")

    # ---- cobertura da informacao de solution-space (importante p/ ameacas a validade)
    cov = pd.DataFrame({"preparedness": reported, "applicability": filled, "lifecycle": life != "not reported",
                        "tradeoffs": filled_t, "strategy": strat.any(axis=1)})
    cov["n_fields"] = cov.sum(axis=1)
    cov.to_csv(OUT / "rq4_solution_space_coverage.csv")
    print("\n[Cobertura] Campos do solution-space preenchidos por caso:")
    print(cov["n_fields"].value_counts().sort_index().to_string())
    print("   Casos com 0-1 campos:", cases_to_str(cov.index[cov.n_fields <= 1]))
    return {"prep": prep, "strat": strat, "life": life, "cov": cov}


if __name__ == "__main__":
    run()
