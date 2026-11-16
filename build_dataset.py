#!/usr/bin/env python3
"""
build_dataset.py: Compile, validate, and export the synthetic medical decision dataset.

Dataset specifications:
- 41 recognized medical specialties.
- Exactly 100 high-quality patient questions per specialty (40 true, 40 false, 20 uncertain).
- 4100 total question-answer items.
- Ternary ground-truth outcomes: "true", "false", "uncertain".
- 80% True/False and 20% Uncertain distribution across the dataset.
- Target output files:
    1. med_decisions.json (primary, with question, answer, specialty, explanation)
    2. med_decisions_minimal.json (strictly question and answer fields)
"""

import json
import sys
from pathlib import Path
from collections import Counter

# Import specialty data modules
from data_catalog import (
    cardiology,
    pulmonology,
    gastroenterology,
    endocrinology,
    neurology,
    nephrology,
    oncology,
    infectious_diseases,
    rheumatology,
    dermatology,
    psychiatry,
    pediatrics,
    obgyn,
    reproductive_medicine,
    orthopedics,
    ophthalmology,
    ent,
    urology,
    allergy_immunology,
    geriatrics,
    emergency_medicine,
    family_medicine,
    hematology,
    general_surgery,
    radiology,
    palliative_care,
    pmr,
    clinical_pharmacology,
    anesthesiology,
    medical_genetics,
    pathology,
    sleep_medicine,
    critical_care,
    neurosurgery,
    vascular_cardiothoracic_surgery,
    plastic_reconstructive_surgery,
    oral_maxillofacial_dentistry,
    clinical_nutrition,
    occupational_travel_medicine,
    radiation_oncology_nuclear_med,
    transplant_medicine,
)

MODULES = [
    cardiology,
    pulmonology,
    gastroenterology,
    endocrinology,
    neurology,
    nephrology,
    oncology,
    infectious_diseases,
    rheumatology,
    dermatology,
    psychiatry,
    pediatrics,
    obgyn,
    reproductive_medicine,
    orthopedics,
    ophthalmology,
    ent,
    urology,
    allergy_immunology,
    geriatrics,
    emergency_medicine,
    family_medicine,
    hematology,
    general_surgery,
    radiology,
    palliative_care,
    pmr,
    clinical_pharmacology,
    anesthesiology,
    medical_genetics,
    pathology,
    sleep_medicine,
    critical_care,
    neurosurgery,
    vascular_cardiothoracic_surgery,
    plastic_reconstructive_surgery,
    oral_maxillofacial_dentistry,
    clinical_nutrition,
    occupational_travel_medicine,
    radiation_oncology_nuclear_med,
    transplant_medicine,
]

VALID_ANSWERS = {"true", "false", "uncertain"}


def build_and_validate():
    all_items = []
    seen_questions = set()
    specialty_stats = {}

    print(f"Loaded {len(MODULES)} medical specialty modules.")

    for mod in MODULES:
        specialty_name = getattr(mod, "SPECIALTY", mod.__name__)
        questions = getattr(mod, "QUESTIONS", None)

        if not isinstance(questions, list):
            raise ValueError(f"Module {mod.__name__} has invalid or missing QUESTIONS list.")

        if len(questions) != 100:
            raise ValueError(f"Specialty '{specialty_name}' has {len(questions)} questions (expected 100).")

        counts = Counter()
        for idx, item in enumerate(questions, start=1):
            q_text = item.get("question", "").strip()
            ans = item.get("answer", "").strip().lower()
            explanation = item.get("explanation", "").strip()

            if not q_text:
                raise ValueError(f"[{specialty_name} #{idx}] Question text is empty.")

            if ans not in VALID_ANSWERS:
                raise ValueError(f"[{specialty_name} #{idx}] Invalid answer: '{ans}'. Must be one of {VALID_ANSWERS}")

            if not explanation:
                raise ValueError(f"[{specialty_name} #{idx}] Missing explanation.")

            if q_text.lower() in seen_questions:
                raise ValueError(f"Duplicate question detected: '{q_text}'")

            seen_questions.add(q_text.lower())
            counts[ans] += 1

            all_items.append({
                "question": q_text,
                "answer": ans,
                "specialty": specialty_name,
                "explanation": explanation
            })

        specialty_stats[specialty_name] = counts

    total_count = len(all_items)
    overall_counts = Counter(item["answer"] for item in all_items)

    print("\n" + "=" * 70)
    print("DATASET COMPILATION & VALIDATION SUMMARY")
    print("=" * 70)
    print(f"{'Specialty':<35} | {'True':<6} | {'False':<6} | {'Uncertain':<9} | {'Total':<5}")
    print("-" * 70)

    for spec, c in specialty_stats.items():
        print(f"{spec:<35} | {c['true']:<6} | {c['false']:<6} | {c['uncertain']:<9} | {sum(c.values()):<5}")

    print("-" * 70)
    print(f"{'OVERALL TOTALS':<35} | {overall_counts['true']:<6} | {overall_counts['false']:<6} | {overall_counts['uncertain']:<9} | {total_count:<5}")
    print("=" * 70)

    # Save primary dataset: med_decisions.json
    out_path = Path("med_decisions.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(all_items, f, indent=2, ensure_ascii=False)
    print(f"\n[OK] Wrote primary dataset to: {out_path.resolve()} ({out_path.stat().st_size} bytes)")

    # Save minimal dataset: med_decisions_minimal.json (strictly question and answer)
    minimal_items = [{"question": item["question"], "answer": item["answer"]} for item in all_items]
    minimal_path = Path("med_decisions_minimal.json")
    with open(minimal_path, "w", encoding="utf-8") as f:
        json.dump(minimal_items, f, indent=2, ensure_ascii=False)
    print(f"[OK] Wrote minimal dataset to: {minimal_path.resolve()} ({minimal_path.stat().st_size} bytes)")

    # Verify reload
    with open(out_path, "r", encoding="utf-8") as f:
        reloaded = json.load(f)
        assert len(reloaded) == 4100, f"Expected 4100 items in json, got {len(reloaded)}"

    print("\n[SUCCESS] All 4100 questions across 41 specialties validated and exported successfully!")


if __name__ == "__main__":
    build_and_validate()
