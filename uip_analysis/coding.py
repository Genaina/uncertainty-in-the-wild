"""Codificacao automatica (baseada em regras) dos campos brutos do CSV.

Cada funcao recebe o DataFrame bruto (indexado por ID) e devolve um DataFrame/Series
codificado. As regras seguem a Secao 3.4 do paper (Operational Coding Rules) e sao
deliberadamente conservadoras: evidencia ausente NAO e tratada como evidencia negativa.
"""
import re
import pandas as pd
from common import is_blank

# ----------------------------------------------------------------- interacoes
CATS = ["dominance", "conflict", "augmentation", "independence"]
STEMS = {
    "dominance": r"dominan\w*|dominat\w*",
    "conflict": r"conflict\w*",
    "augmentation": r"augment\w*",
    "independence": r"independen\w*",
}
DEFS = [
    r"no uncertainty from any source affects (?:the )+(?:uncertainty from )?another source",
    r"one source of uncertainty dominates the other, and reducing the uncertainty from the "
    r"dominant source necessarily reduces the other\.?",
    r"uncertainties highly correlated with each other \(no dominance\)\.?\s*reduction of one of "
    r"them positively affects the reduction of the other\.?",
    r"reduction of uncertainty from one source may increase uncertainty from another one\.?",
]


def _strip_template(text: str) -> str:
    t = re.sub(r"\s+", " ", str(text))
    for d in DEFS:
        t = re.sub(d, " ", t, flags=re.I)
    return t


def code_interactions(raw: pd.DataFrame) -> pd.DataFrame:
    """Retorna, por caso e categoria, um de: 'explicit', 'tentative', 'template', ''.

    - explicit  : a categoria aparece seguida de conteudo especifico do caso
    - tentative : marcada com '(?)', '(Possible)' ou usada so como adjetivo, ex. 'Conflict (dominant)'
    - template  : o contribuidor so devolveu as definicoes do template (rotulo sem conteudo)
    - ''        : sem evidencia (ou marcada 'N/A in this case')
    """
    label_re = re.compile(r"(?:\(\d\)\s*)?(?:independence|dominance|augmentation|conflict)\b", re.I)
    rank = {"": 0, "template": 0, "tentative": 1, "explicit": 2}
    rows = {}
    for cid, text in raw["Uncertainty Interaction Category"].items():
        t = _strip_template(text)
        res = {c: "" for c in CATS}
        empty = set()
        for cat, stem in STEMS.items():
            for m in re.finditer(stem, t, flags=re.I):
                window = t[m.end():m.end() + 80]
                before = t[max(0, m.start() - 20):m.start()]
                tail = re.sub(r"^[\s:;|\-\(\)\?\+]*", "", window)
                if re.match(r"n/?a\b", tail, re.I):
                    continue
                if tail == "" or label_re.match(tail):
                    # rotulo vazio; excecao: '<A> x <B> ? Label' (conteudo vem ANTES do rotulo)
                    if tail == "" and "\u00d7" in before + t[max(0, m.start() - 80):m.start()]:
                        state = "explicit"
                    elif re.match(r"^\s*\(\?\)", window):
                        state = "tentative"
                    else:
                        empty.add(cat)
                        continue
                else:
                    tentative = bool(re.match(r"^\s*\(\?\)", window)) or "possible" in before.lower() \
                        or before.rstrip().endswith("(")
                    state = "tentative" if tentative else "explicit"
                if rank[state] > rank[res[cat]]:
                    res[cat] = state
        if not any(res[c] for c in CATS):          # so rotulos vazios -> resposta de template
            for c in empty:
                res[c] = "template"
        rows[cid] = res
    return pd.DataFrame(rows).T[CATS]


def interaction_flags(coded: pd.DataFrame, mode: str) -> pd.DataFrame:
    """mode='strict': so 'explicit'; 'lenient': explicit+tentative; 'paper': +template."""
    ok = {"strict": {"explicit"}, "lenient": {"explicit", "tentative"},
          "paper": {"explicit", "tentative", "template"}}[mode]
    return coded.isin(ok)


# ------------------------------------------------------------- heterogeneidade
def code_nature(raw: pd.DataFrame) -> pd.Series:
    def f(t):
        t = str(t).lower()
        if "homogeneous" in t and "heterogeneous" not in t:
            return "Homogeneous/Mixed"
        if "homogeneous" in t and "heterogeneous" in t:
            return "Homogeneous/Mixed"
        return "Heterogeneous"
    return raw["Uncertainty Nature"].map(f)


# ---------------------------------------------------------------------- span
def code_abstraction(raw: pd.DataFrame) -> pd.Series:
    """Cross-layer vs Same/Partial (Sec. 3.4, regra 3)."""
    def f(t):
        if is_blank(t):
            return "Same/Partial"          # CS10: sem campo -> mesmo nivel (ver %comentario do .tex)
        s = str(t).lower()
        if re.search(r"\bsame\b", s):
            return "Same/Partial"
        return "Cross-layer"
    return raw["Abstraction Gap"].map(f)


# -------------------------------------------------------------------- impacto
IMPACT_DIMS = {
    "Safety": r"collision|safety|false (alarm|positive)|emergenc|catastroph|crash",
    "Performance": r"latenc|response time|throughput|replanning|tracking|performance|overhead|delay|number of adaptations|duration",
    "Reliability & Availability": r"downtime|recover|telemetry|sla|availab|reliab|disruption|violation",
    "Mission Success": r"mission|task success|continuity",
    "Human Factors & Trust": r"fatigue|trust|workload|takeover|human",
    "Resource Efficiency / Cost": r"cost|energy|resource|bandwidth|overhead|sustainab|utiliz",
}


def code_impact(raw: pd.DataFrame) -> pd.DataFrame:
    rows = {}
    for cid, t in raw["Impact"].items():
        s = str(t)
        generic = bool(re.search(r"generic", s, re.I))
        dims = [d for d, p in IMPACT_DIMS.items() if re.search(p, s, re.I)]
        rows[cid] = {"generic_marker": generic, "dims": dims, "n_dims": len(dims)}
    out = pd.DataFrame(rows).T
    out["impact_class"] = out["generic_marker"].map(
        lambda g: "Generic/Template" if g else "Multi-dimensional")
    return out


# --------------------------------------------------------- fontes de incerteza
SOURCE_TYPES = {
    "Measurement": r"measurement|measure", "Occurrence": r"occurr?ence",
    "Design": r"design", "Behavior": r"behaviou?r", "Belief": r"belief|epistemic",
    "Spatio-temporal": r"spatio-?temporal|spatiotemporal",
}
SOURCE_CATS = {
    "Model": r"\bmodel", "Adaptation functions": r"adaptation function",
    "Goals": r"\bgoals?\b|utility", "Environment": r"environment",
    "Resources": r"resource|managed system|battery|energy",
    "Human": r"human|user|patient|driver",
}


def code_sources(raw: pd.DataFrame):
    types, cats = {}, {}
    for cid, t in raw["Uncertainty Sources (verbatim)"].items():
        s = str(t)
        types[cid] = {k: bool(re.search(p, s, re.I)) for k, p in SOURCE_TYPES.items()}
        cats[cid] = {k: bool(re.search(p, s, re.I)) for k, p in SOURCE_CATS.items()}
    return pd.DataFrame(types).T, pd.DataFrame(cats).T


# ------------------------------------------------------------- mecanismos RQ2
MECHANISMS = {
    "Propagation": r"propagat|transform|cascad|flows? into|affects? .*(decision|goal)",
    "Amplification": r"amplif|reinforc|jointly increase|correlated|augment",
    "Dominance": r"dominan|dominat",
    "Trade-off / Conflict": r"conflict|trade-?off|increase[s]? (?:uncertainty|instability|overhead)",
}


def code_mechanisms(raw: pd.DataFrame) -> pd.DataFrame:
    rows = {}
    for cid in raw.index:
        txt = " ".join(str(raw.loc[cid, c]) for c in
                       ["Uncertainty Interaction Category", "Impact", "Trade-offs", "Abstraction Gap"])
        txt = _strip_template(txt)
        rows[cid] = {k: bool(re.search(p, txt, re.I)) for k, p in MECHANISMS.items()}
    return pd.DataFrame(rows).T


# ------------------------------------------------------------- preparedness RQ4
PREP_LABELS = {
    "Awareness": r"awareness", "Prevention": r"prevention",
    "Detectability": r"detect(?:ability|ion)", "Representation": r"representation",
    "Understanding": r"comprehension(?:/analy[sz]ability)?|understanding|analy[sz]ability",
    "Mitigation": r"mitigation",
}
NEGATIVE = r"^(?:\s*[:\-]?\s*)?(?:no\b|cannot|unknown|\(?blank\)?|not (?:provided|specified)|none)"


def _prep_segments(text: str):
    t = re.sub(r"\s+", " ", str(text))
    pat = "|".join(f"(?P<{k}>{v})" for k, v in PREP_LABELS.items())
    ms = list(re.finditer(rf"\b(?:{pat})\s*:", t, flags=re.I))
    segs = {}
    for i, m in enumerate(ms):
        key = next(k for k in PREP_LABELS if m.group(k))
        end = ms[i + 1].start() if i + 1 < len(ms) else len(t)
        segs[key] = t[m.end():end].strip()
    return segs


def code_preparedness(raw: pd.DataFrame) -> pd.DataFrame:
    """True se o contribuidor reporta a capacidade (conteudo nao-vazio e nao-negativo).

    'Limited'/'Partial' contam como presentes (capacidade parcial, como na Tabela 8).
    Texto sem rotulos (CS5: 'mitigation level reached ...') -> so Mitigation.
    """
    neg = re.compile(NEGATIVE + r"|have not|not thought|not yet", re.I)
    rows = {}
    for cid, t in raw["Level of Preparedness"].items():
        res = {k: False for k in PREP_LABELS}
        if not is_blank(t) and "blank" not in str(t).lower()[:12]:
            segs = _prep_segments(t)
            for k, v in segs.items():
                if v and not neg.search(v) and not re.match(r"^\(?blank", v, re.I):
                    res[k] = True
            if not segs and re.search(r"mitigation", str(t), re.I):
                res["Mitigation"] = True
        rows[cid] = res
    return pd.DataFrame(rows).T


STRAT_LABELS = ["Detection", "Representation", "Analysis", "Mitigation"]


def _strategy_segments(text: str):
    t = re.sub(r"\s+", " ", str(text))
    ms = list(re.finditer(r"\b(Detection|Representation|Analysis|Mitigation)\s*:", t))
    out = {}
    for i, m in enumerate(ms):
        end = ms[i + 1].start() if i + 1 < len(ms) else len(t)
        seg = t[m.end():end].strip()
        out[m.group(1)] = bool(seg) and not re.match(
            r"^(unknown|blank|not specified|\(blank\)|n/a)", seg, re.I)
    return out


def code_strategy(raw: pd.DataFrame) -> pd.DataFrame:
    rows = {}
    for cid, t in raw["Strategy"].items():
        rows[cid] = {k: False for k in STRAT_LABELS}
        if not is_blank(t):
            rows[cid].update(_strategy_segments(t))
    return pd.DataFrame(rows).T[STRAT_LABELS]


# -------------------------------------------------------------- applicability
APPLIC = {
    "Architectural Assumptions": r"architectur|decentrali|central coordinator|reconfiguration|layers?\b|control architecture|framework structured",
    "Infrastructure Requirements": r"bus|fram|communication|infrastructure|sensing capab|multi-sensor|storage",
    "Observability Requirements": r"observab|sensing|measur|metrics are available|detect|monitor|confidence",
    "Model Availability": r"model",
    "Adaptation Capability": r"adaptive|adaptation|controllable|alternative configurations|switch|reconfig|safe mode",
    "Operational Scope": r"enabling scope|failure-driven|contexts|restricted",
}


def code_applicability(raw: pd.DataFrame) -> pd.DataFrame:
    rows = {}
    for cid, t in raw["Applicability Conditions"].items():
        rows[cid] = {k: (False if is_blank(t) or "not provided" in str(t).lower()
                         else bool(re.search(p, str(t), re.I))) for k, p in APPLIC.items()}
    return pd.DataFrame(rows).T


# ------------------------------------------------------------------ lifecycle
def code_lifecycle(raw: pd.DataFrame) -> pd.Series:
    def f(t):
        if is_blank(t) or "blank" in str(t).lower():
            return "not reported"
        s = str(t).lower()
        d = bool(re.search(r"design|pre-release", s))
        r = bool(re.search(r"run-?time|runtime|run time", s))
        if re.search(r"\bboth\b", s) or (d and r):
            return "both"
        return "design-time" if d else ("runtime" if r else "not reported")
    return raw["Lifecycle Stage"].map(f)


# ------------------------------------------------------------------ trade-offs
TRADEOFFS = {
    "Robustness vs Resource Consumption": r"robustness|redundan|overhead|resource|memory utili|computational|energy cost|cost",
    "Safety vs Performance": r"safety|mission completion|conservative|flexibility|traffic instab",
    "Responsiveness vs Stability": r"responsiveness|stability|instabil|oscillat|replanning|adaptation frequency|volatility",
    "Autonomy vs Assurance": r"autonomy|assurance|guarantee|explainab",
    "Sensitivity vs False Positives": r"false (alarm|positive)|sensitivity|filtering",
}


def code_tradeoffs(raw: pd.DataFrame) -> pd.DataFrame:
    rows = {}
    for cid, t in raw["Trade-offs"].items():
        rows[cid] = {k: (False if is_blank(t) or "not provided" in str(t).lower()
                         else bool(re.search(p, str(t), re.I))) for k, p in TRADEOFFS.items()}
    return pd.DataFrame(rows).T
