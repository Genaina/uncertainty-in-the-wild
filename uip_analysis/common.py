"""Utilidades comuns: carga do CSV bruto, parsing de campos e codificacao automatica.

O CSV bruto usa ';' como separador e codificacao cp1252. Ha linhas vazias no final.
"""
import re
from pathlib import Path
import pandas as pd

BASE = Path(__file__).parent
RAW = BASE / "data" / "artifacts_case_studies_raw_corrected.csv"  # CS11/CS12 corrigidos (ver README)
OUT = BASE / "output"
OUT.mkdir(exist_ok=True)

# Dominio PRIMARIO conforme Tabela 3 / Figura 1 do paper (o CSV bruto tem CS5 como
# 'Healthcare/Robotics'; o paper o classifica como Robotics).
PAPER_DOMAIN = {
    "CS1": "IT/Cloud", "CS2": "Aerospace", "CS3": "IT/Cloud", "CS4": "Smart City",
    "CS5": "Robotics", "CS6": "Automotive", "CS7": "Automotive", "CS8": "IT/Cloud",
    "CS9": "IT/Cloud", "CS10": "IT/Cloud", "CS11": "Healthcare", "CS12": "Robotics",
    "CS13": "IT/Cloud", "CS14": "Automotive", "CS15": "IT/Cloud", "CS16": "Automotive",
    "CS17": "Automotive", "CS18": "Robotics",
}

TEMPLATE_DEFS = [  # frases-modelo copiadas do template de coleta
    r"no uncertainty from any source affects the+ ?(?:uncertainty from )?(?:another|any other)? ?source",
    r"one source of uncertainty dominates the other, and reducing[^.]*\.",
    r"uncertainties highly correlated with each other \(no dominance\)\.?[^.]*\.",
    r"reduction of uncertainty from one source may increase uncertainty from another one\.?",
]


def load_raw() -> pd.DataFrame:
    df = pd.read_csv(RAW, sep=";", encoding="cp1252", engine="python")
    df = df.dropna(subset=["ID"]).copy()
    df["ID"] = df["ID"].str.strip()
    df = df.set_index("ID")
    df["domain"] = pd.Series(PAPER_DOMAIN)
    return df


def is_blank(text) -> bool:
    if text is None or (isinstance(text, float) and pd.isna(text)):
        return True
    t = str(text).strip().lower()
    return t in {"", "nan", "not provided", "not provided.", "n/a"} or \
        bool(re.match(r"^(field (left )?blank|field blank)\.?$", t))


def cases_to_str(ids):
    return ", ".join(sorted(ids, key=lambda s: int(s[2:])))


def pct(n, d):
    return f"{100 * n / d:.1f}%"


def report_check(label, paper_value, computed_value):
    flag = "OK " if paper_value == computed_value else "DIFF"
    print(f"   [{flag}] {label}: paper={paper_value}  calculado={computed_value}")


def by_domain(flags: pd.Series, domain: pd.Series, domains):
    """Conta casos com flag=True por dominio, na ordem 'domains'."""
    s = flags.groupby(domain).sum().reindex(domains).fillna(0).astype(int)
    return s


def compare_sets(name, paper_ids, computed_ids):
    p, c = set(paper_ids), set(computed_ids)
    if p == c:
        print(f"   [OK  ] {name}: {cases_to_str(c)}")
    else:
        print(f"   [DIFF] {name}:\n          paper    = {cases_to_str(p)}\n"
              f"          calculado= {cases_to_str(c)}\n"
              f"          so no paper = {cases_to_str(p - c) or '-'} | so no calculo = {cases_to_str(c - p) or '-'}")
