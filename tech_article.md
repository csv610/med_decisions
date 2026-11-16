# Empirical Evaluation of a System-1 Probabilistic Decision Model for Tri-State Clinical Question Verification Across 41 Medical Specialties

**Keywords:** Clinical Decision Support, Medical Claim Verification, System-1 Inference, Probability Calibration, Selective Prediction, Error Asymmetry, Tri-State Classification

---

## Abstract

Automated triage of patient-facing medical questions requires both discrete clinical judgment and well-calibrated uncertainty estimates. In this paper, we present a comprehensive empirical evaluation of `pplx-decider-flash`, a System-1 probabilistic decision model accessed via `ollama.systemone`, on `med_decisions.json`—a benchmark of 4,100 patient-oriented medical questions spanning 41 clinical specialties (100 questions per specialty). Each question is classified into one of three clinically grounded states: `true` (40.0%), `false` (40.0%), or `uncertain` (20.0%). Across all 4,100 sequential queries, the model achieves **92.20% overall accuracy** (3,780/4,100; 95% Wilson CI: [91.33%, 92.98%]) and a **90.44% Macro-F1** (95% bootstrap CI: [89.46%, 91.38%]), with a mean per-query latency of **1.0483 s** (median 1.0435 s, p95 1.0518 s).

Per-class analysis reveals pronounced performance differences: `true` achieves 96.48% F1 (98.66% recall) and `false` achieves 92.38% F1 (93.17% recall), whereas `uncertain` drops to 82.44% F1 (77.32% recall). Error directionality is strongly asymmetric: 47 `false` items (2.87% of `false`) are misclassified as `true` compared to only 3 `true` items (0.18% of `true`) misclassified as `false`, and misclassified `uncertain` items are predicted as `false` 2.80 times more frequently than `true` (137 vs. 49 cases). Calibration analysis demonstrates that `pplx-decider-flash` is consistently underconfident on this benchmark (Expected Calibration Error = 0.0766, multiclass Brier score = 0.1300): empirical accuracy exceeds mean predicted confidence across all six probability bins. In selective prediction experiments, thresholding at confidence $\tau \ge 0.90$ retains 50.24% coverage (2,060 queries) at **99.56% accuracy** with a single `false` $\rightarrow$ `true` error, while thresholding at $\tau \ge 0.95$ retains 30.05% coverage (1,232 queries) at **99.84% accuracy** with zero `false` $\rightarrow$ `true` errors. Conversely, accuracy on the 49.76% of queries below $\tau = 0.90$ falls to 84.75%. Because this study evaluates a single model on one structured dataset without external baselines, comparative claims against generative reasoning models are out of scope. Within these bounds, the findings indicate that `pplx-decider-flash` is unsuitable for autonomous clinical deployment—due to 320 total errors, 47 false-to-true endorsements, and 22.68% missed uncertainty—but exhibits calibration and latency properties compatible with a confidence-gated front-end filter when paired with mandatory secondary review.

---

## 1. Introduction

Patient-facing clinical question answering and health-information triage systems must routinely distinguish among three qualitatively different epistemic states: claims that align with established medical guidelines (`true`), claims that reflect unsafe misconceptions or contraindications (`false`), and questions whose answers depend on patient-specific diagnostic workup or mixed clinical evidence (`uncertain`). Treating medical triage as a purely binary (`true`/`false`) problem risks forcing definitive answers onto clinically ambiguous scenarios, whereas open-ended generative responses often obscure the underlying decision commitment behind hedging language and variable latency.

In recent inference architectures, dedicated "System-1" decision interfaces—such as `ollama.systemone`—bypass autoregressive chain-of-thought generation to emit a structured categorical choice alongside a normalized probability distribution over predefined criteria. In principle, exposing calibrated probabilities at low, predictable latency enables selective prediction: high-confidence queries can be resolved rapidly, while ambiguous or low-confidence queries are routed to slower "System-2" reasoning models, retrieval-augmented guideline verification, or human clinicians.

However, empirical validation is required before any such model can be considered for clinical workflows. Specifically, four quantitative questions govern practical viability:
1. **Class-Conditional Accuracy and Macro Balance**: Does the model maintain reliable recall on the minority `uncertain` class rather than collapsing onto binary `true`/`false` predictions?
2. **Clinical Safety Asymmetry**: How frequently does the model commit high-severity `false` $\rightarrow$ `true` errors (endorsing a false or contraindicated premise) relative to lower-severity `true` $\rightarrow$ `false` errors?
3. **Cross-Specialty Consistency**: Is performance uniform across medical domains, or does accuracy degrade in high-acuity, multi-system, or preference-sensitive specialties?
4. **Calibration and Selective Risk-Coverage**: Are predicted probabilities sufficiently well calibrated—and separated between correct and incorrect predictions—to support confidence-based abstention without retaining hidden high-confidence failures?

To answer these questions objectively, we analyze the evaluation pipeline implemented in [eval_decisions.py](file:///Users/csv610/Projects/MyBooks/Medical/DecisionModels/eval_decisions.py) and its complete 4,100-item output log in [evaluation_results.json](file:///Users/csv610/Projects/MyBooks/Medical/DecisionModels/evaluation_results.json). This paper restricts its claims strictly to observed metrics from this single-model evaluation; it does not benchmark competing models, evaluate multi-turn clinical dialogues, or measure outcomes in live patient populations.

---

## 2. Experimental Setup and Evaluation Harness

### 2.1 System-1 Decision Interface and Prompting Schema

The evaluation harness in [eval_decisions.py](file:///Users/csv610/Projects/MyBooks/Medical/DecisionModels/eval_decisions.py) loads the benchmark dataset via `load_dataset("med_decisions.json")` and iterates sequentially over each item using `query_decision_model(question, model="pplx-decider-flash")`. Each query invokes `ollama.systemone` with the patient question passed as `state` and a single `choice` specification named `medical_decision`:

- **Instruction**: *"Is this patient question medically true, false, or uncertain?"*
- **Criteria**:
  - `true`: *"Medically and clinically true according to standard medical guidelines."*
  - `false`: *"Medically false, unsafe misconception, or contraindicated."*
  - `uncertain`: *"Clinically uncertain, mixed evidence, or depends on patient workup."*

For every query, the API returns `answer.choice` (the predicted label in `{"true", "false", "uncertain"}`) and `answer.probabilities` (a 3-element probability dictionary summing to 1.0). Wall-clock latency is recorded per query using `time.perf_counter()` immediately before and after the `ollama.systemone` call. The script aggregates overall accuracy, mean query time, total elapsed time, and per-specialty accuracy into a `summary` object, while storing per-question records (`question`, `specialty`, `ground_truth`, `predicted`, `is_correct`, `elapsed_time`, `probabilities`) under `details` in [evaluation_results.json](file:///Users/csv610/Projects/MyBooks/Medical/DecisionModels/evaluation_results.json).

### 2.2 Benchmark Dataset Characteristics

The evaluated dataset in [evaluation_results.json](file:///Users/csv610/Projects/MyBooks/Medical/DecisionModels/evaluation_results.json) contains **4,100 questions** partitioned uniformly across **41 medical specialties**, with exactly **100 questions per specialty**. The ground-truth class distribution is fixed at a 40/40/20 ratio:
- **`true`**: 1,640 questions (40.00%)
- **`false`**: 1,640 questions (40.00%)
- **`uncertain`**: 820 questions (20.00%)

Question lengths range from **6 to 30 words**, with a mean of **17.48 words**. Notably, question length is virtually identical between correctly classified items (mean 17.48 words) and misclassified items (mean 17.47 words), indicating that raw surface length is not a confounding driver of model errors.

### 2.3 Evaluation Metrics

Beyond the summary accuracy figures produced by [eval_decisions.py](file:///Users/csv610/Projects/MyBooks/Medical/DecisionModels/eval_decisions.py), we compute a comprehensive suite of classification, uncertainty, calibration, and operational metrics from `details`:

1. **Per-Class and Macro Metrics**: Precision, recall, and F1-score for each class $c \in \{\text{true}, \text{false}, \text{uncertain}\}$, along with unweighted Macro-F1 to prevent the 40/40/20 prior from masking minority-class degradation.
2. **Confusion Matrix Analysis**: Full $3 \times 3$ counts to quantify directional error rates, specifically distinguishing `false` $\rightarrow$ `true` endorsements from `true` $\rightarrow$ `false` rejections and `uncertain` collapses.
3. **Uncertainty and Margin Metrics**:
   - *Top-1 Confidence*: $\hat{p} = \max_c p(c \mid x)$.
   - *Probability Margin*: $M(x) = p_{(1)}(x) - p_{(2)}(x)$, the difference between the highest and second-highest predicted class probabilities.
   - *Shannon Entropy*: $H(x) = -\sum_{c} p(c \mid x) \ln p(c \mid x)$ (in nats; maximum $\ln 3 \approx 1.0986$ nats for a uniform distribution).
4. **Calibration Metrics**:
   - *Multiclass Brier Score* (Brier, 1950): $\text{BS} = \frac{1}{N} \sum_{i=1}^{N} \sum_{c} (p_{i,c} - y_{i,c})^2$, where $y_{i,c} \in \{0, 1\}$ is the one-hot ground-truth indicator.
   - *Expected Calibration Error (ECE)* (Guo et al., 2017): Computed across six confidence bins—$[0.0, 0.5)$, $[0.5, 0.6)$, $[0.6, 0.7)$, $[0.7, 0.8)$, $[0.8, 0.9)$, and $[0.9, 1.0]$—as $\text{ECE} = \sum_{b=1}^{6} \frac{|B_b|}{N} |\text{acc}(B_b) - \text{conf}(B_b)|$.
5. **Selective Prediction (Risk-Coverage)** (Geifman & El-Yaniv, 2017): For confidence thresholds $\tau \in \{0.00, 0.50, 0.60, 0.70, 0.75, 0.80, 0.85, 0.90, 0.95\}$, we measure *coverage* (fraction of queries with $\hat{p} \ge \tau$), *accepted accuracy*, *accepted `false` $\rightarrow$ `true` error count*, and *rejected accuracy* (accuracy on the abstained subset $\hat{p} < \tau$).
6. **Uncertainty Bounds**: We report 95% Wilson score confidence intervals (Wilson, 1927) for binomial proportions (overall accuracy and per-specialty accuracies at $n = 100$) and 1,000-resample 95% bootstrap confidence intervals for Macro-F1, Brier score, and ECE.

### 2.4 Dataset Provenance and Reproducibility

As documented in [build_dataset.py](file:///Users/csv610/Projects/MyBooks/Medical/DecisionModels/build_dataset.py), `med_decisions.json` is a synthetic medical decision benchmark compiled and validated from 41 specialty-specific modules under `data_catalog/`, enforcing 100 unique questions per specialty and an exact 40/40/20 (`true`/`false`/`uncertain`) split. The software dependencies specified in [requirements.txt](file:///Users/csv610/Projects/MyBooks/Medical/DecisionModels/requirements.txt) are `ollama>=0.6.2`, `httpx>=0.28.1`, `numpy>=2.0.0`, and `matplotlib>=3.8.0`. For full reproducibility, we note that [eval_decisions.py](file:///Users/csv610/Projects/MyBooks/Medical/DecisionModels/eval_decisions.py) and [evaluation_results.json](file:///Users/csv610/Projects/MyBooks/Medical/DecisionModels/evaluation_results.json) do not log the underlying hardware specifications, exact Ollama server version, or model weight digest/quantization of `pplx-decider-flash`.

---

## 3. Overall Classification Performance and Error Asymmetry

### 3.1 Aggregate and Per-Class Results

Across all 4,100 queries, `pplx-decider-flash` correctly classifies **3,780 items** and misclassifies **320 items**, yielding an overall accuracy of **92.20%** (92.195%) and a **Macro-F1 of 90.44%**. Table 1 reports the ground-truth support, predicted counts, and per-class precision, recall, and F1-score.

| Class | Ground Truth | Predicted | Precision (%) | Recall (%) | F1-Score (%) | TP | FP | FN |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `true` | 1,640 (40.00%) | 1,714 (41.80%) | 94.40 | 98.66 | 96.48 | 1,618 | 96 | 22 |
| `false` | 1,640 (40.00%) | 1,668 (40.68%) | 91.61 | 93.17 | 92.38 | 1,528 | 140 | 112 |
| `uncertain` | 820 (20.00%) | 718 (17.51%) | 88.30 | 77.32 | 82.44 | 634 | 84 | 186 |
| **Total / Macro** | **4,100 (100%)** | **4,100 (100%)** | **91.44 (avg)** | **89.72 (avg)** | **90.44 (macro)** | **3,780** | **320** | **320** |

The 1.76-percentage-point gap between overall accuracy (92.20%) and Macro-F1 (90.44%) is driven primarily by the `uncertain` class. While `true` achieves 98.66% recall (missing only 22 of 1,640 items) and `false` achieves 93.17% recall (missing 112 of 1,640 items), `uncertain` achieves only **77.32% recall** (missing 186 of 820 items). Moreover, the model under-predicts `uncertain` in aggregate (718 predictions, or 17.51% of the dataset, compared to the 20.00% ground-truth base rate), shifting probability mass toward `true` (41.80% predicted) and `false` (40.68% predicted).

### 3.2 Confusion Matrix and Clinical Risk Asymmetry

Table 2 details the full $3 \times 3$ confusion matrix.

| Ground Truth $\backslash$ Predicted | `true` | `false` | `uncertain` | Row Total |
| :--- | :---: | :---: | :---: | :---: |
| **`true`** | **1,618** (98.66%) | 3 (0.18%) | 19 (1.16%) | 1,640 |
| **`false`** | 47 (2.87%) | **1,528** (93.17%) | 65 (3.96%) | 1,640 |
| **`uncertain`** | 49 (5.98%) | 137 (16.71%) | **634** (77.32%) | 820 |
| **Column Total** | **1,714** | **1,668** | **718** | **4,100** |

Three structural error patterns emerge from Table 2:
1. **Asymmetric Binary Inversion (`false` $\rightarrow$ `true` vs. `true` $\rightarrow$ `false`)**: Direct polarity flips between `true` and `false` account for 50 of the 3,280 binary ground-truth items (1.52%). However, these flips are heavily skewed: `true` $\rightarrow$ `false` occurs only **3 times** (0.18% of `true`), whereas `false` $\rightarrow$ `true` occurs **47 times** (2.87% of `false`)—a 15.7-fold asymmetry. From a clinical safety perspective, endorsing a false, unsafe, or contraindicated claim as `true` represents the highest-severity failure mode.
2. **Asymmetric Collapse of `uncertain` (`uncertain` $\rightarrow$ `false` vs. `uncertain` $\rightarrow$ `true`)**: Of the 186 misclassified `uncertain` items, **137 (73.66% of `uncertain` errors; 16.71% of all `uncertain` items)** are predicted as `false`, whereas **49 (26.34% of `uncertain` errors; 5.98% of all `uncertain` items)** are predicted as `true`. When the model fails to recognize clinical ambiguity, it defaults nearly **2.80 times** more often to `false` than `true`.
3. **Conservative Deferral on Binary Items**: When the model errs on `true` or `false` items without inverting polarity, it shifts them into `uncertain` (19 `true` $\rightarrow$ `uncertain`, 65 `false` $\rightarrow$ `uncertain`). While counted as classification errors under strict 3-way accuracy, deferring a binary item to `uncertain` is clinically safer than polarity inversion, as it signals ambiguity rather than false certainty.

---

## 4. Cross-Specialty Performance Analysis

To assess whether performance is uniform across clinical domains, Table 3 presents the complete per-specialty breakdown across all 41 specialties ($n = 100$ questions each, including 20 `uncertain` items per specialty unless otherwise noted). For each specialty, we report overall accuracy, the count of safety-critical `false` $\rightarrow$ `true` errors, the `uncertain` error count, and the mean top-1 predicted confidence.

| Specialty | Accuracy (%) | `false` $\rightarrow$ `true` | `uncertain` Errors | Mean Top-1 Conf. |
| :--- | :---: | :---: | :---: | :---: |
| Clinical Nutrition & Obesity Medicine | 98.00 | 1 | 1 / 20 | 0.859 |
| Urology | 98.00 | 1 | 1 / 20 | 0.872 |
| Dermatology | 97.00 | 1 | 2 / 20 | 0.890 |
| Physical Medicine & Rehabilitation | 97.00 | 0 | 0 / 20 | 0.841 |
| Reproductive Medicine & Infertility | 97.00 | 1 | 0 / 20 | 0.872 |
| Rheumatology | 97.00 | 2 | 1 / 20 | 0.875 |
| Ophthalmology | 96.00 | 0 | 2 / 20 | 0.863 |
| Clinical Pharmacology & Medication Safety | 95.00 | 2 | 2 / 20 | 0.855 |
| Oral & Maxillofacial Surgery & Dentistry | 95.00 | 0 | 2 / 20 | 0.835 |
| Orthopedics | 95.00 | 0 | 3 / 20 | 0.864 |
| Geriatrics | 94.00 | 0 | 2 / 20 | 0.830 |
| Infectious Diseases | 94.00 | 1 | 5 / 20 | 0.876 |
| Sleep Medicine | 94.00 | 0 | 2 / 20 | 0.807 |
| Anesthesiology & Pain Medicine | 93.00 | 2 | 0 / 20 | 0.812 |
| Cardiology | 93.00 | 2 | 2 / 20 | 0.831 |
| Endocrinology | 93.00 | 0 | 6 / 20 | 0.874 |
| General Surgery | 93.00 | 0 | 6 / 20 | 0.859 |
| Hematology | 93.00 | 3 | 4 / 20 | 0.842 |
| Obstetrics & Gynecology | 93.00 | 2 | 2 / 20 | 0.845 |
| Otolaryngology (ENT) | 93.00 | 1 | 5 / 20 | 0.848 |
| Pediatrics | 93.00 | 1 | 4 / 20 | 0.871 |
| Psychiatry | 93.00 | 0 | 7 / 20 | 0.884 |
| Pulmonology | 93.00 | 1 | 5 / 20 | 0.857 |
| Gastroenterology | 92.00 | 0 | 4 / 20 | 0.850 |
| Plastic & Reconstructive Surgery | 92.00 | 3 | 4 / 20 | 0.820 |
| Radiation Oncology & Nuclear Medicine | 92.00 | 0 | 5 / 20 | 0.811 |
| Occupational, Environmental & Travel Medicine | 91.00 | 1 | 7 / 20 | 0.863 |
| Transplant Medicine | 91.00 | 2 | 4 / 20 | 0.809 |
| Vascular & Cardiothoracic Surgery | 91.00 | 0 | 5 / 20 | 0.814 |
| Neurosurgery | 90.00 | 0 | 5 / 20 | 0.837 |
| Oncology | 90.00 | 0 | 6 / 20 | 0.865 |
| Radiology & Diagnostic Imaging | 90.00 | 4 | 6 / 20 | 0.801 |
| Emergency Medicine & Acute Toxicology | 89.00 | 0 | 11 / 20 | 0.897 |
| Neurology | 89.00 | 1 | 10 / 20 | 0.860 |
| Allergy & Clinical Immunology | 87.00 | 1 | 9 / 20 | 0.843 |
| Family Medicine & Preventive Care | 87.00 | 3 | 5 / 20 | 0.814 |
| Medical Genetics & Genomics | 87.00 | 1 | 12 / 20 | 0.862 |
| Nephrology | 87.00 | 2 | 10 / 20 | 0.853 |
| Pathology & Laboratory Medicine | 87.00 | 4 | 8 / 20 | 0.825 |
| Critical Care & Intensive Care Medicine | 86.00 | 1 | 5 / 20 | 0.800 |
| Palliative & Supportive Care | 85.00 | 3 | 6 / 20 | 0.778 |

### 4.1 Domain-Level Observations

![Classification Accuracy Across All 41 Medical Specialties](file:///Users/csv610/Projects/MyBooks/Medical/DecisionModels/figures/fig3_specialty_accuracy.png)

With $n = 100$ questions per specialty, 95% Wilson score confidence intervals span $[76.72\%, 90.69\%]$ at 85.00% accuracy, $[86.25\%, 96.57\%]$ at 93.00% accuracy, and $[93.00\%, 99.45\%]$ at 98.00% accuracy (Figure 3). Consequently, small differences of 1–3 percentage points fall well within sampling variance and should not be over-interpreted. Nevertheless, three broader patterns stand out across Table 3:

1. **High-Performing Guideline-Codified Specialties ($\ge 95\%$)**: Ten specialties reach 95.00%–98.00% accuracy, led by Clinical Nutrition & Obesity Medicine (98.00%) and Urology (98.00%), followed by Dermatology, Physical Medicine & Rehabilitation, Reproductive Medicine & Infertility, and Rheumatology (all 97.00%). In Physical Medicine & Rehabilitation and Reproductive Medicine & Infertility, the model achieves 20/20 (100%) accuracy on `uncertain` items.
2. **Lower-Performing Specialties ($\le 89\%$)**: Nine specialties fall below 90.00%, with Palliative & Supportive Care lowest at **85.00%** (and lowest mean confidence at 0.778) and Critical Care & Intensive Care Medicine at **86.00%** (mean confidence 0.800). These domains frequently involve individualized goals-of-care trade-offs or unstable multi-organ physiology.
3. **Concentration of `uncertain` Errors vs. `false` $\rightarrow$ `true` Errors**: Specialties with the highest `uncertain` error counts are Medical Genetics & Genomics (12/20), Emergency Medicine & Acute Toxicology (11/20), Nephrology (10/20), Neurology (10/20), and Allergy & Clinical Immunology (9/20). Notably, Emergency Medicine & Acute Toxicology has the **highest mean confidence (0.897)** of all 41 specialties despite an 89.00% accuracy and 11/20 `uncertain` errors—indicating localized overconfidence on acute-care ambiguity. Meanwhile, `false` $\rightarrow$ `true` errors peak at 4/100 in Pathology & Laboratory Medicine and Radiology & Diagnostic Imaging, and 3/100 in Family Medicine & Preventive Care, Hematology, Palliative & Supportive Care, and Plastic & Reconstructive Surgery.

---

## 5. Probability Calibration, Uncertainty Structure, and Selective Prediction

### 5.1 Bin-Wise Calibration Analysis

A central requirement for confidence-gated triage is that predicted probabilities reflect empirical correctness. Across all 4,100 items, the **multiclass Brier score is 0.1300** (95% bootstrap CI: [0.1215, 0.1390]) and the **Expected Calibration Error (ECE) is 0.0766** (95% bootstrap CI: [0.0693, 0.0836]). Table 4 reports sample counts, mean predicted confidence, empirical accuracy, and the calibration gap ($\text{Accuracy} - \text{Confidence}$) across six probability bins, visualized in Figure 1.

![Reliability Diagram Across Six Confidence Bins](file:///Users/csv610/Projects/MyBooks/Medical/DecisionModels/figures/fig1_reliability_diagram.png)

| Confidence Bin | Count ($n$) | Dataset Share (%) | Mean Confidence | Empirical Accuracy (%) | Gap (Acc $-$ Conf) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| $[0.0, 0.5)$ | 141 | 3.44% | 0.4586 | 56.74% | +10.88% |
| $[0.5, 0.6)$ | 232 | 5.66% | 0.5507 | 63.79% | +8.72% |
| $[0.6, 0.7)$ | 333 | 8.12% | 0.6546 | 75.98% | +10.52% |
| $[0.7, 0.8)$ | 482 | 11.76% | 0.7548 | 89.83% | +14.35% |
| $[0.8, 0.9)$ | 852 | 20.78% | 0.8547 | 95.66% | +10.19% |
| $[0.9, 1.0]$ | 2,060 | 50.24% | 0.9532 | 99.56% | +4.24% |

In this evaluation, `pplx-decider-flash` is **strictly underconfident across every confidence bin**: empirical accuracy exceeds mean predicted confidence by +4.24 to +14.35 percentage points. From a risk-management standpoint, conservative (underconfident) calibration is preferable to overconfidence, as nominal confidence thresholds provide an empirical safety margin. Half of all predictions (2,060/4,100; 50.24%) fall in the $[0.9, 1.0]$ bin, where empirical accuracy reaches **99.56%**. Conversely, accuracy degrades monotonically across lower bins, falling to 56.74% when top-1 confidence is below 0.50.

### 5.2 Probability Entropy and Margin Separation

To examine how cleanly the predicted probability distributions separate correct from incorrect decisions—and how uncertainty varies by ground-truth class—Table 5 summarizes top-1 confidence, probability margin ($p_{(1)} - p_{(2)}$), and Shannon entropy ($H$).

| Subset | Count ($n$) | Top-1 Confidence (Mean / Median) | Margin $p_{(1)} - p_{(2)}$ (Mean / Median) | Shannon Entropy $H$ (Mean / Median) |
| :--- | :---: | :---: | :---: | :---: |
| **Correct Predictions** | 3,780 | 0.8635 / 0.9137 | 0.7649 / 0.8541 | 0.4104 / 0.3436 |
| **Incorrect Predictions** | 320 | 0.6310 / 0.6179 | 0.3499 / 0.3269 | 0.8001 / 0.8179 |
| **Ground Truth: `true`** | 1,640 | — | 0.8510 (mean) | 0.2860 (mean) |
| **Ground Truth: `false`** | 1,640 | — | 0.7289 (mean) | 0.4656 (mean) |
| **Ground Truth: `uncertain`** | 820 | — | 0.5025 (mean) | 0.7009 (mean) |

Incorrect predictions exhibit nearly double the mean Shannon entropy of correct predictions (0.8001 vs. 0.4104 nats) and less than half the mean probability margin (0.3499 vs. 0.7649). Across ground-truth classes, `true` items are decided with the sharpest distributions (mean entropy 0.2860, margin 0.8510), followed by `false` (entropy 0.4656, margin 0.7289), while `uncertain` items elicit substantially flatter distributions (entropy 0.7009, margin 0.5025) even when classified correctly.

### 5.3 Selective Prediction (Risk-Coverage Trade-Off)

Table 6 and Figure 2 quantify the operational trade-off between automation coverage and residual error when abstaining below a confidence threshold $\tau$.

![Selective Prediction Risk-Coverage Curve](file:///Users/csv610/Projects/MyBooks/Medical/DecisionModels/figures/fig2_risk_coverage.png)

| Threshold $\tau$ | Coverage (%) | Accepted ($n$) | Accepted Accuracy (%) | Accepted `false` $\rightarrow$ `true` | Rejected ($n$) | Rejected Accuracy (%) |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| $\ge 0.00$ | 100.00% | 4,100 | 92.20% | 47 | 0 | — |
| $\ge 0.50$ | 96.56% | 3,959 | 93.46% | 33 | 141 | 56.74% |
| $\ge 0.60$ | 90.90% | 3,727 | 95.30% | 22 | 373 | 61.13% |
| $\ge 0.70$ | 82.78% | 3,394 | 97.20% | 10 | 706 | 68.13% |
| $\ge 0.75$ | 77.83% | 3,191 | 97.90% | 8 | 909 | 72.17% |
| $\ge 0.80$ | 71.02% | 2,912 | 98.42% | 5 | 1,188 | 76.94% |
| $\ge 0.85$ | 62.10% | 2,546 | 98.98% | 2 | 1,554 | 81.08% |
| $\ge 0.90$ | 50.24% | 2,060 | 99.56% | 1 | 2,040 | 84.75% |
| $\ge 0.95$ | 30.05% | 1,232 | 99.84% | 0 | 2,868 | 88.91% |

Table 6 illustrates a steep risk-coverage trade-off:
- Raising $\tau$ from $0.00$ to $0.80$ reduces coverage to 71.02% while cutting `false` $\rightarrow$ `true` errors by **89.4%** (from 47 down to 5) and raising accepted accuracy to **98.42%**.
- Raising $\tau$ to $0.90$ achieves **99.56% accuracy** with only **1** `false` $\rightarrow$ `true` error, but requires escalating **49.76% of all queries** (2,040 items, on which the model's unassisted accuracy is 84.75%).
- Eliminating all `false` $\rightarrow$ `true` errors in this dataset requires $\tau = 0.95$, which retains only **30.05% coverage** (1,232 items, 99.84% accuracy) and escalates 69.95% of traffic.

---

## 6. Inference Latency and Operational Profile

Total sequential execution time across all 4,100 queries in [evaluation_results.json](file:///Users/csv610/Projects/MyBooks/Medical/DecisionModels/evaluation_results.json) was **4,298.16 s** (71.64 minutes). Table 7 summarizes the per-query latency distribution.

| Statistic | Latency (seconds) |
| :--- | :---: |
| Minimum | 1.0275 |
| Median (p50) | 1.0435 |
| Mean | 1.0483 |
| Standard Deviation | 0.0616 |
| p90 | 1.0497 |
| p95 | 1.0518 |
| p99 | 1.2285 |
| Maximum | 4.5959 |

Under single-client sequential invocation, latency is highly deterministic: **97.83% of queries (4,011/4,100)** complete in $\le 1.10\text{ s}$, and the p50–p95 span is just 8.3 milliseconds (1.0435 s to 1.0518 s). Exactly **88 queries (2.15%)** fall in the 1.20–1.25 s range (accounting for the p99 of 1.2285 s), and only **1 query (0.02%)** exceeds 1.50 s (the 4.5959 s maximum, consistent with a single transient runtime or scheduling spike, as the second-slowest query is 1.2416 s).

Because [eval_decisions.py](file:///Users/csv610/Projects/MyBooks/Medical/DecisionModels/eval_decisions.py) issues queries sequentially without concurrency, these measurements characterize single-stream latency rather than multi-tenant throughput or queuing behavior under parallel clinical load.

---

## 7. Qualitative Error Taxonomy

To understand the mechanisms behind the 320 errors, we inspect both the 9 high-confidence errors ($\hat{p} \ge 0.90$) and representative lower-confidence failures.

### 7.1 Complete Enumeration of High-Confidence Errors ($\hat{p} \ge 0.90$)

Only **9 of 2,060** predictions with confidence $\ge 0.90$ (0.44%) are incorrect. Listing all nine reveals a striking structural pattern:

1. **Infectious Diseases (`false` $\rightarrow$ `true`, $\hat{p} = 0.9310$)**: *"Can you catch HIV from casual contact like hugging, sharing drinking glasses, or using a toilet seat?"* — This is the single `false` $\rightarrow$ `true` error above $\tau = 0.90$ and represents a severe public-health misinformation failure.
2. **Neurology (`uncertain` $\rightarrow$ `false`, $\hat{p} = 0.9171$)**: *"Can following a brain-healthy diet (like the Mediterranean or MIND diet) guarantee you will avoid Alzheimer's if it runs in your family?"*
3. **Neurology (`uncertain` $\rightarrow$ `false`, $\hat{p} = 0.9485$)**: *"Does taking monthly migraine-prevention injections (CGRP blockers) permanently cure migraines even after you stop taking them?"*
4. **Neurology (`uncertain` $\rightarrow$ `false`, $\hat{p} = 0.9033$)**: *"If someone experiences a single episode of nerve inflammation (clinically isolated syndrome), will they definitely develop multiple sclerosis?"*
5. **Infectious Diseases (`uncertain` $\rightarrow$ `false`, $\hat{p} = 0.9406$)**: *"Can taking a single dose of doxycycline right after a tick bite guarantee you will not catch any tick-borne illness?"*
6. **Emergency Medicine & Acute Toxicology (`uncertain` $\rightarrow$ `false`, $\hat{p} = 0.9023$)**: *"Does giving the clot-stabilizing drug tranexamic acid (TXA) improve survival in all patients who have suffered a severe traumatic brain injury?"*
7. **Emergency Medicine & Acute Toxicology (`uncertain` $\rightarrow$ `false`, $\hat{p} = 0.9552$)**: *"Does every patient with mild dehydration from vomiting and diarrhea require intravenous (IV) fluids rather than drinking an oral electrolyte solution?"*
8. **Medical Genetics & Genomics (`uncertain` $\rightarrow$ `false`, $\hat{p} = 0.9572$)**: *"If someone carries two copies of the APOE e4 gene, is it certain that they will develop Alzheimer's disease?"*
9. **Medical Genetics & Genomics (`uncertain` $\rightarrow$ `false`, $\hat{p} = 0.9332$)**: *"Can commercial 'epigenetic biological age' blood tests accurately predict how many years an individual has left to live?"*

Excluding the HIV error (#1), **all 8 remaining high-confidence errors (88.9%) are `uncertain` $\rightarrow$ `false`**. Every one of these eight questions contains a universal or absolute quantifier (*"guarantee"*, *"permanently cure"*, *"definitely"*, *"all patients"*, *"every patient"*, *"certain"*, *"accurately predict"*). Clinically, `pplx-decider-flash` treats such absolute guarantees as `false` (strictly falsified by exceptions), whereas the benchmark annotation labels them `uncertain` (reflecting probabilistic or patient-dependent outcomes). This highlights a systematic **rubric-boundary mismatch** rather than pure medical ignorance.

### 7.2 Negation and Polarity Sensitivity in `false` $\rightarrow$ `true` Errors (47 Cases)

Below $\tau = 0.90$, several `false` $\rightarrow$ `true` errors occur on questions with negative framing or double-negation semantics:
- *Cardiology* ($\hat{p} = 0.6418$): *"Does feeling completely healthy with no symptoms rule out having an enlarged aorta (an aortic aneurysm)?"* (GT = `false`, Predicted = `true`).
- *Cardiology* ($\hat{p} = 0.8061$): *"Can someone who is thin and physically fit never have dangerously high cholesterol?"* (GT = `false`, Predicted = `true`).
- *Pulmonology* ($\hat{p} = 0.7571$): *"Is a spirometry lung function test painful or dangerous to perform?"* (GT = `false`, Predicted = `true`).

In the first two examples, the phrases *"rule out"* and *"never"* invert the truth condition of the underlying clinical fact (asymptomatic aneurysms exist; thin individuals can have hypercholesterolemia). Fast single-pass classification appears vulnerable to these polarity inversions.

### 7.3 Rare `true` $\rightarrow$ `false` Errors and Regulatory Cutoffs (3 Cases)

Only three `true` items across all 1,640 positive examples were misclassified as `false`:
- *Allergy & Clinical Immunology* ($\hat{p} = 0.5820$): *"Is sesame legally recognized in the United States as a major food allergen that must be clearly listed on packaged food labels?"* — Sesame was added as the ninth major U.S. food allergen under the FASTER Act (effective January 1, 2023), pointing to a temporal or regulatory knowledge gap.
- *Pediatrics* ($\hat{p} = 0.7016$): *"Is it generally recommended to switch healthy children from whole milk to low-fat or skim milk around age 2?"*
- *Reproductive Medicine & Infertility* ($\hat{p} = 0.4343$, with $P(\text{uncertain}) = 0.3552$): *"Can taking high doses of pain relievers like ibuprofen around ovulation temporarily prevent an ovary from releasing an egg?"*

### 7.4 Lower-Confidence `uncertain` Boundary Cases

On `uncertain` items below $\tau = 0.90$, probability mass is typically split between `uncertain` and one binary pole:
- *Cardiology* (`uncertain` $\rightarrow$ `false`, $P(\text{false}) = 0.4596$ vs. $P(\text{uncertain}) = 0.3913$): *"Is lowering systolic blood pressure below 120 mmHg safe and beneficial for frail older adults over age 80?"*
- *Cardiology* (`uncertain` $\rightarrow$ `true`, $P(\text{true}) = 0.6447$ vs. $P(\text{uncertain}) = 0.3387$): *"Does testosterone replacement therapy in older men with low testosterone increase or decrease cardiovascular risk?"*
- *Gastroenterology* (`uncertain` $\rightarrow$ `true`, $P(\text{true}) = 0.5015$ vs. $P(\text{uncertain}) = 0.3940$): *"Can a mild attack of diverticulitis be safely treated with rest and fluids alone without taking antibiotics?"*

These cases reflect genuine clinical nuance—evolving trial evidence (e.g., SPRINT in frail elderly, TRAVERSE for testosterone, antibiotic-sparing uncomplicated diverticulitis)—where a single-pass classifier struggles to calibrate between emerging consensus and ongoing clinical uncertainty.

---

## 8. Discussion: Clinical Deployment Implications

### 8.1 Why Standalone Deployment Is Insufficient

Despite achieving 92.20% overall accuracy, `pplx-decider-flash` should not be deployed as an autonomous clinical decision-maker. An unassisted 7.80% error rate translates to 320 incorrect triage decisions per 4,100 queries, including 47 false-to-true endorsements (such as the high-confidence HIV transmission error) and 186 missed `uncertain` cases where nuanced workup or individualized clinical judgment is required.

### 8.2 Confidence-Gated Two-Tier Triage Architecture

The empirical risk-coverage curve (Table 6) supports a more defensible role: **confidence-gated pre-screening** within a two-tier pipeline:
- **Tier 1 (High-Confidence Fast Path)**: Queries with $\hat{p} \ge 0.90$ (50.24% of traffic) achieve 99.56% accuracy at ~1.05 s latency. For workflows requiring zero `false` $\rightarrow$ `true` errors in this benchmark, $\tau = 0.95$ retains 30.05% coverage at 99.84% accuracy.
- **Tier 2 (Escalation Path)**: Queries with $\hat{p} < \tau$—or predictions labeled `uncertain` regardless of confidence—are routed to a slower System-2 reasoning model, retrieval-augmented clinical guideline lookup (e.g., UpToDate/CDC/FDA sources to mitigate regulatory cutoffs), or human clinician review.

Even under a $\tau = 0.90$ gate, however, the presence of the $\hat{p} = 0.9310$ HIV error demonstrates that confidence thresholding reduces, but does not eliminate, high-severity failures. Production systems would additionally require rule-based or retrieval-backed safety checks on high-risk infectious, toxicological, and emergency topics, as well as explicit negation-normalization or re-verification for questions containing absolute quantifiers (*"never"*, *"rule out"*, *"guarantee"*).

---

## 9. Methodological Limitations and Threats to Validity

Several limitations constrain the generalizability of these results:

1. **Single-Model Evaluation Without Baselines**: [eval_decisions.py](file:///Users/csv610/Projects/MyBooks/Medical/DecisionModels/eval_decisions.py) evaluates only `pplx-decider-flash`. Without head-to-head comparisons against general-purpose instruction-tuned LLMs, chain-of-thought ("System-2") prompting, or domain-finetuned encoders on the same 4,100 questions, we cannot establish whether 92.20% accuracy and 0.0766 ECE represent an advance over alternative architectures.
2. **Synthetic / Curated Dataset Priors**: `med_decisions.json` enforces an artificial uniform distribution of 100 questions per specialty and an exact 40/40/20 class balance. Real-world patient portals exhibit heavily skewed specialty distributions, colloquial or misspelled phrasing, multi-part questions, and different base rates of ambiguity—all of which can shift both accuracy and ECE.
3. **Annotation Ambiguity on Absolute Quantifiers**: As shown in Section 7.1, 8 of the 9 high-confidence errors stem from a definitional tension between `false` and `uncertain` on questions containing universal quantifiers (*"guarantee"*, *"all patients"*). Ground-truth label noise or rubric ambiguity in `med_decisions.json` may therefore account for a portion of the observed `uncertain` error rate.
4. **Unweighted Clinical Risk**: Standard accuracy and Macro-F1 treat all errors equally, whereas clinical harm is highly non-uniform (e.g., `false` $\rightarrow$ `true` on HIV transmission vs. `uncertain` $\rightarrow$ `false` on a lifestyle guarantee).
5. **Sequential-Only Latency Measurement**: Latency was measured under single-client sequential execution; concurrent throughput, GPU memory contention, and tail latency under production traffic remain untested.

---

## 10. Related Work

Evaluating probabilistic reliability alongside classification accuracy draws on two established methodological traditions. First, proper scoring rules such as the Brier score (Brier, 1950) and bin-wise Expected Calibration Error (ECE) (Guo et al., 2017) have become standard diagnostics for assessing whether neural classifiers' predicted probabilities reflect empirical correctness—a prerequisite for clinical decision support where overconfidence can mask harmful errors. Second, selective prediction and risk-coverage analysis (Geifman & El-Yaniv, 2017) formalize how a model can trade coverage for higher accuracy by abstaining on low-confidence inputs, a pattern directly applicable to two-tier clinical triage. Our evaluation extends these frameworks to a tri-state (`true` / `false` / `uncertain`) medical verification interface (`ollama.systemone`) across 41 specialties.

---

## 11. Ethical Considerations and Intended Use

The benchmark `med_decisions.json` is a synthetic, offline dataset compiled by [build_dataset.py](file:///Users/csv610/Projects/MyBooks/Medical/DecisionModels/build_dataset.py) and contains no protected health information (PHI) or real patient records. The evaluated model, `pplx-decider-flash`, is not cleared or validated for clinical diagnosis, treatment selection, or autonomous patient-facing medical advice. As demonstrated by the 47 `false` $\rightarrow$ `true` errors—including a high-confidence failure on HIV casual-contact transmission—any downstream clinical workflow must treat model outputs strictly as preliminary triage signals subject to guideline-grounded verification and qualified clinician oversight.

---

## 12. Conclusion

On a 4,100-question tri-state benchmark spanning 41 medical specialties, `pplx-decider-flash` accessed via `ollama.systemone` achieves **92.20% accuracy** (95% Wilson CI: [91.33%, 92.98%]), **90.44% Macro-F1** (95% bootstrap CI: [89.46%, 91.38%]), and **1.0483 s** mean sequential latency. Its probability estimates are consistently underconfident (ECE = 0.0766, Brier = 0.1300), enabling selective prediction at **99.56% accuracy** across the 50.24% of queries with confidence $\ge 0.90$ and **99.84% accuracy** across the 30.05% of queries with confidence $\ge 0.95$. At the same time, the model exhibits a 22.68% miss rate on `uncertain` items, 47 `false` $\rightarrow$ `true` endorsements (including one high-confidence failure on HIV transmission), sensitivity to negation and universal quantifiers, and occasional regulatory knowledge gaps. Consequently, `pplx-decider-flash` is not suitable for standalone clinical decision-making, but warrants further investigation as a low-latency front-end filter in confidence-gated, retrieval-augmented, human-in-the-loop triage pipelines. Future work should benchmark System-1 deciders directly against System-2 reasoning models, evaluate calibration robustness on uncurated patient queries, and incorporate clinical-severity weighting into triage evaluation.

---

## References

- Brier, G. W. (1950). Verification of forecasts expressed in terms of probability. *Monthly Weather Review*, 78(1), 1–3.
- Geifman, Y., & El-Yaniv, R. (2017). Selective classification for deep neural networks. *Advances in Neural Information Processing Systems (NeurIPS)*, 30, 4878–4887.
- Guo, C., Pleiss, G., Sun, Y., & Weinberger, K. Q. (2017). On calibration of modern neural networks. *Proceedings of the International Conference on Machine Learning (ICML)*, 1321–1330.
- Wilson, E. B. (1927). Probable inference, the law of succession, and statistical inference. *Journal of the American Statistical Association*, 22(158), 209–212.
