from collections import defaultdict
import json
import time
import ollama


def load_dataset(filepath="med_decisions.json"):
    """Load evaluation questions from a JSON file."""
    with open(filepath, "r") as f:
        return json.load(f)


def query_decision_model(question, model="pplx-decider-flash"):
    """Query the Ollama System One decision model and return predictions with timing."""
    start_time = time.perf_counter()
    response = ollama.systemone(
        model=model,
        state=question,
        questions={
            "medical_decision": {
                "type": "choice",
                "instructions": "Is this patient question medically true, false, or uncertain?",
                "criteria": {
                    "true": "Medically and clinically true according to standard medical guidelines.",
                    "false": "Medically false, unsafe misconception, or contraindicated.",
                    "uncertain": "Clinically uncertain, mixed evidence, or depends on patient workup.",
                },
            },
        },
    )
    elapsed_time = time.perf_counter() - start_time
    answer = response.answers["medical_decision"]
    return answer.choice, answer.probabilities, elapsed_time


def save_summary(correct, total, total_time, specialty_stats, details, output_file="evaluation_results.json"):
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


def evaluate(dataset):
    """Run evaluation across all items in the dataset and track stats per specialty."""
    correct = 0
    total = 0
    total_time = 0.0
    specialty_stats = defaultdict(lambda: {"correct": 0, "total": 0})
    details = []

    print(f"Loaded {len(dataset)} questions. Starting evaluation...\n")

    for item in dataset:
        question = item["question"]
        ground_truth = item["answer"].lower()
        specialty = item.get("specialty", "General")

        predicted, probabilities, elapsed_time = query_decision_model(question)
        total_time += elapsed_time

        is_correct = (predicted == ground_truth)
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
            "probabilities": probabilities,
        })

        print(f"Q: [{specialty}] {question}")
        print(f"  Truth: {ground_truth} | Predicted: {predicted} ({'MATCH' if is_correct else 'MISMATCH'})")
        print(f"  Time: {elapsed_time:.3f}s")
        print(f"  Probabilities: {probabilities}\n")

    save_summary(correct, total, total_time, specialty_stats, details)


def main():
    dataset = load_dataset("med_decisions.json")
    evaluate(dataset)


if __name__ == "__main__":
    main()
