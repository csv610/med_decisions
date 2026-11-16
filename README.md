# MedDecisions: Tri-State Clinical Question Verification Benchmark & Evaluation

A structured benchmark and empirical evaluation suite for tri-state (`true`, `false`, `uncertain`) clinical question verification across **41 medical specialties** (**4,100 questions** total), evaluating `pplx-decider-flash` via the `ollama.systemone` probabilistic decision interface.

For the full conference-length technical analysis, see [`tech_article.md`](tech_article.md).

---

## Key Results Summary

Evaluated sequentially on all 4,100 items in `med_decisions.json` (`40% true`, `40% false`, `20% uncertain`; 100 questions per specialty):

| Metric | Value | 95% Confidence Interval |
| :--- | :---: | :---: |
| **Overall Accuracy** | **92.20%** (3,780 / 4,100) | Wilson CI: `[91.33%, 92.98%]` |
| **Macro-F1** | **90.44%** | Bootstrap CI: `[89.46%, 91.38%]` |
| **Multiclass Brier Score** | **0.1300** | Bootstrap CI: `[0.1215, 0.1390]` |
| **Expected Calibration Error (ECE)** | **0.0766** | Bootstrap CI: `[0.0693, 0.0836]` |
| **Mean Sequential Latency** | **1.0483 s** | Median: `1.0435 s`, p95: `1.0518 s` |

### Per-Class Performance

| Class | Support | Precision | Recall | F1-Score |
| :--- | :---: | :---: | :---: | :---: |
| `true` | 1,640 (40%) | 94.40% | 98.66% | 96.48% |
| `false` | 1,640 (40%) | 91.61% | 93.17% | 92.38% |
| `uncertain` | 820 (20%) | 88.30% | 77.32% | 82.44% |

- **Confidence-Gated Selective Prediction**: Predictions with top-1 confidence $\ge 0.90$ cover **50.24%** of queries (2,060 / 4,100) at **99.56% accuracy** (1 `false` $\rightarrow$ `true` error). At $\ge 0.95$, coverage is **30.05%** (1,232 / 4,100) at **99.84% accuracy** with **0** `false` $\rightarrow$ `true` errors.
- **Safety Caveat**: Unassisted deployment yields 320 errors, including 47 `false` $\rightarrow$ `true` endorsements and 186 missed `uncertain` items. This benchmark and model are intended for research and confidence-gated triage analysis only, not autonomous clinical decision-making.

### Accuracy by Medical Specialty

| Specialty | Correct / Total | Accuracy |
| :--- | :---: | :---: |
| Clinical Nutrition & Obesity Medicine | 98 / 100 | 98.00% |
| Urology | 98 / 100 | 98.00% |
| Dermatology | 97 / 100 | 97.00% |
| Physical Medicine & Rehabilitation | 97 / 100 | 97.00% |
| Reproductive Medicine & Infertility | 97 / 100 | 97.00% |
| Rheumatology | 97 / 100 | 97.00% |
| Ophthalmology | 96 / 100 | 96.00% |
| Clinical Pharmacology & Medication Safety | 95 / 100 | 95.00% |
| Oral & Maxillofacial Surgery & Dentistry | 95 / 100 | 95.00% |
| Orthopedics | 95 / 100 | 95.00% |
| Geriatrics | 94 / 100 | 94.00% |
| Infectious Diseases | 94 / 100 | 94.00% |
| Sleep Medicine | 94 / 100 | 94.00% |
| Anesthesiology & Pain Medicine | 93 / 100 | 93.00% |
| Cardiology | 93 / 100 | 93.00% |
| Endocrinology | 93 / 100 | 93.00% |
| General Surgery | 93 / 100 | 93.00% |
| Hematology | 93 / 100 | 93.00% |
| Obstetrics & Gynecology | 93 / 100 | 93.00% |
| Otolaryngology (ENT) | 93 / 100 | 93.00% |
| Pediatrics | 93 / 100 | 93.00% |
| Psychiatry | 93 / 100 | 93.00% |
| Pulmonology | 93 / 100 | 93.00% |
| Gastroenterology | 92 / 100 | 92.00% |
| Plastic & Reconstructive Surgery | 92 / 100 | 92.00% |
| Radiation Oncology & Nuclear Medicine | 92 / 100 | 92.00% |
| Occupational, Environmental & Travel Medicine | 91 / 100 | 91.00% |
| Transplant Medicine | 91 / 100 | 91.00% |
| Vascular & Cardiothoracic Surgery | 91 / 100 | 91.00% |
| Neurosurgery | 90 / 100 | 90.00% |
| Oncology | 90 / 100 | 90.00% |
| Radiology & Diagnostic Imaging | 90 / 100 | 90.00% |
| Emergency Medicine & Acute Toxicology | 89 / 100 | 89.00% |
| Neurology | 89 / 100 | 89.00% |
| Allergy & Clinical Immunology | 87 / 100 | 87.00% |
| Family Medicine & Preventive Care | 87 / 100 | 87.00% |
| Medical Genetics & Genomics | 87 / 100 | 87.00% |
| Nephrology | 87 / 100 | 87.00% |
| Pathology & Laboratory Medicine | 87 / 100 | 87.00% |
| Critical Care & Intensive Care Medicine | 86 / 100 | 86.00% |
| Palliative & Supportive Care | 85 / 100 | 85.00% |

---

## Repository Structure

```text
.
├── build_dataset.py             # Compiles & validates the 41-specialty dataset from data_catalog/
├── data_catalog/                # 41 Python modules (100 questions each: 40 true, 40 false, 20 uncertain)
├── med_decisions.json           # Full dataset (question, answer, specialty, explanation)
├── med_decisions_minimal.json   # Minimal dataset (question, answer)
├── eval_decisions.py            # Sequential evaluation harness using ollama.systemone
├── evaluation_results.json      # Complete per-question predictions, probabilities, and timings
├── plot_results.py              # Visualization script
├── figures/                     # Publication figures (reliability diagram, risk-coverage, specialty CIs)
├── tech_article.md              # Full 10-page technical paper analyzing the evaluation results
└── requirements.txt             # Python dependencies
```

---

## Setup & Usage

### 1. Install Dependencies

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Requires a running [Ollama](https://ollama.com/) instance with `pplx-decider-flash` available via `ollama.systemone`.

### 2. Build & Validate Dataset

```bash
python3 build_dataset.py
```

Generates `med_decisions.json` and `med_decisions_minimal.json` from the 41 modules in `data_catalog/`.

### 3. Run Evaluation

```bash
python3 eval_decisions.py
```

Queries `pplx-decider-flash` on every item in `med_decisions.json` and writes aggregate metrics and per-question details to `evaluation_results.json`.

---

## Figures

- `figures/fig1_reliability_diagram.png` — 6-bin calibration reliability diagram (`ECE = 0.0766`).
- `figures/fig2_risk_coverage.png` — Selective prediction accuracy and `false` $\rightarrow$ `true` error count vs. coverage.
- `figures/fig3_specialty_accuracy.png` — Per-specialty accuracy with 95% Wilson confidence intervals across all 41 specialties.

---

## Disclaimer

`med_decisions.json` is a synthetic, offline benchmark containing no protected health information (PHI). Neither the dataset nor `pplx-decider-flash` is validated or cleared for clinical diagnosis, treatment selection, or autonomous patient-facing medical advice.
