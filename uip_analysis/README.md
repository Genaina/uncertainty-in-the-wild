# Scripts de análise RQ1–RQ4 — "Uncertainty in the Wild"

Reproduz, a partir de `data/artifacts_case_studies_raw.csv`, as análises das Seções 6.1–6.4 do manuscrito
e **valida cada número contra o que está impresso no paper** (`[OK]` / `[DIFF]`).

## Dados
`data/artifacts_case_studies_raw_corrected.csv` = CSV original com o conteudo (colunas Uncertainty Sources..Strategy) das linhas CS11 e CS12 trocado para alinhar ao Summary/dominio (CS11=BSN, CS12=Lab Sample). O original esta em `data/..._ORIGINAL.csv`.

## Uso
```bash
pip install pandas matplotlib
python run_all.py        # roda RQ1..RQ4, imprime o relatório e salva em output/
python rq1.py            # ou cada RQ isoladamente
```

## Arquivos
| Arquivo | Conteúdo |
|---|---|
| `common.py` | leitura do CSV (`;`, cp1252), mapa de domínios do paper, helpers de comparação |
| `coding.py` | codificação automática por regras (Seção 3.4 do paper) |
| `paper_reported.py` | números/listas de casos impressos no paper, só para validação |
| `rq1.py` | categorias de interação (dominance/conflict/augmentation/independence), heterogeneidade, Fig. 1 e Fig. 3, Tab. 4 |
| `rq2.py` | cross-layer vs same-level (Tab. 5), categorias/tipos de fonte, mecanismos causais |
| `rq3.py` | impacto multidimensional vs genérico (Tab. 6), dimensões de qualidade (Tab. 7) |
| `rq4.py` | preparedness (Tab. 8), applicability (Tab. 9), lifecycle (Tab. 10), trade-offs (Tab. 11), strategy (Tab. 12) |

## Três critérios para as categorias de interação (RQ1)
- `strict`: só evidência explícita escrita pelo contribuidor
- `lenient`: + marcações tentativas (`(?)`, `(Possible)`, `Conflict (dominant)`)
- `paper`: + respostas só-template (CS4, CS7, CS8, CS14 devolveram apenas as definições do template)

## O que é totalmente reproduzível e o que não é
- **Reproduzido pelo CSV**: independence (4), heterogêneo/homogêneo (16/2), cross-layer/same (14/4), impacto genérico (15/3), lifecycle.
- **Analyst-derived** (Tab. 7, 9, 10, 11 e partes da 8 e 12): dependem de interpretação manual. Os scripts dão um cross-check por palavras-chave com Jaccard; divergências ali indicam interpretação, não erro.

## Divergências encontradas entre o paper e os dados
1. **Sec. 6.1.1 (17/16/15/4)** não bate com a Fig. 3 (somas 13/14/14) nem com o CSV (critério paper: 12/14/14; strict: 6/10/9). Só independence (4) confere.
2. **Tab. 4**: soma 15+3, texto diz 16/2. O CSV dá Robotics 3/0 (o `\added{1}` parece resíduo de edição).
3. **Tab. 5**: soma 17 (não 18). Pelo comentário `%Cross-layer` do .tex e pelo CSV: IT/Cloud 6/1 e Robotics 3/0.
4. **Tab. 6**: soma 10/8, mas o texto diz 15/3. Pelo CSV (marcador "generic"): Auto 4/1, IT 5/2, Robotics 3/0, Healthcare 1/0, Smart City 1/0, Aerospace 1/0.
5. **CS11 × CS12**: a Tab. 3 descreve CS11 = BSN e CS12 = Lab Sample Logistics, mas o CSV (e as citações no texto, p.ex. "battery uncertainty (CS11)", "body sensor networks (CS12)") têm o contrário.
6. **Respostas só-template** (CS4, CS7, CS8, CS14) entram nas contagens de categorias sem evidência específica do caso.
