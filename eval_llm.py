import argparse
from collections import defaultdict
import json
import time
from ollama import chat


SYSTEM_PROMPT = (
    "You are a medical decision classifier. Determine whether the patient question "
    "is medically true, false, or uncertain.\n"
    "Criteria:\n"
    "- true: Medically and clinically true according to standard medical guidelines.\n"
    "- false: Medically false, unsafe misconception, or contraindicated.\n"
    "- uncertain: Clinically uncertain, mixed evidence, or depends on patient workup.\n"
    'Respond with only a JSON string: "true", "false", or "uncertain".'
)

DECISION_SCHEMA = {"type": "string", "enum": ["true", "false", "uncertain"]}


def load_dataset(filepath="med_decisions.json"):
    """Load evaluation questions from a JSON file."""
    with open(filepath, "r") as f:
        return json.load(f)


def parse_decision(text):
    """Accept only a complete label or a schema-constrained JSON string."""
    cleaned = text.strip().lower()
    if cleaned in {"true", "false", "uncertain"}:
        return cleaned
    try:
        cleaned = json.loads(cleaned)
    except json.JSONDecodeError:
        pass
    if not isinstance(cleaned, str):
        return "unknown"
    if cleaned in {"true", "false", "uncertain"}:
        return cleaned

    return "unknown"


def query_llm_model(question, model="medgemma"):
    """Query the Ollama LLM model and return prediction, raw response, and timing."""
    start_time = time.perf_counter()
    response = chat(
        model=model,
        format=DECISION_SCHEMA,
        options={"temperature": 0},
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": question},
        ],
    )
    elapsed_time = time.perf_counter() - start_time
    raw_content = response.message.content.strip()
    predicted = parse_decision(raw_content)
    if predicted == "unknown":
        raise ValueError(f"Model returned an invalid decision: {raw_content!r}")
    return predicted, raw_content, elapsed_time


def save_summary(
    correct,
    total,
    total_time,
    specialty_stats,
    details,
    output_file="evaluation_llm_results.json",
):
    """Save evaluation summary and per-question details to a JSON file."""
    by_specialty = {}
    for specialty, stats in sorted(specialty_stats.items()):
        c = stats["correct"]
        n = stats["total"]
        by_specialty[specialty] = {
            "correct": c,
            "total": n,
            "accuracy": (c / n * 100) if n > 0 else 0.0,
        }

    results = {
        "summary": {
            "correct": correct,
            "total": total,
            "accuracy": (correct / total * 100) if total > 0 else 0.0,
            "average_query_time": (total_time / total) if total > 0 else 0.0,
            "total_time": total_time,
            "by_specialty": by_specialty,
        },
        "details": details,
    }

    with open(output_file, "w") as f:
        json.dump(results, f, indent=2)


def evaluate(dataset, model="medgemma"):
    """Run evaluation across all items in the dataset and track stats per specialty."""
    correct = 0
    total = 0
    total_time = 0.0
    specialty_stats = defaultdict(lambda: {"correct": 0, "total": 0})
    details = []

    print(f"Loaded {len(dataset)} questions. Starting evaluation with model '{model}'...\n")

    for item in dataset:
        question = item["question"]
        ground_truth = item["answer"].lower()
        specialty = item.get("specialty", "General")

        predicted, raw_response, elapsed_time = query_llm_model(question, model=model)
        total_time += elapsed_time

        is_correct = predicted == ground_truth
        if is_correct:
            correct += 1
            specialty_stats[specialty]["correct"] += 1
        total += 1
        specialty_stats[specialty]["total"] += 1

        details.append({
            "question": question,
            "specialty": specialty,
            "ground_truth": ground_truth,
            "predicted": predicted,
            "is_correct": is_correct,
            "elapsed_time": elapsed_time,
            "raw_response": raw_response,
        })

        print(f"Q: [{specialty}] {question}")
        print(f"  Truth: {ground_truth} | Predicted: {predicted} ({'MATCH' if is_correct else 'MISMATCH'})")
        print(f"  Time: {elapsed_time:.3f}s")
        print(f"  Response: {raw_response}\n")

    save_summary(correct, total, total_time, specialty_stats, details)


def main():
    parser = argparse.ArgumentParser(description="Evaluate an Ollama LLM on med_decisions.json.")
    parser.add_argument(
        "--model", "-m", default="medgemma", help="Ollama model name (default: medgemma)"
    )
    args = parser.parse_args()

    dataset = load_dataset("med_decisions.json")
    evaluate(dataset, model=args.model)


if __name__ == "__main__":
    main()
