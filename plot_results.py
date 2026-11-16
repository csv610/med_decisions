import json
from collections import defaultdict
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def load_evaluation_results(filepath="evaluation_results.json"):
    """Load evaluation results from JSON."""
    with open(filepath, "r") as f:
        return json.load(f)


def calculate_specialty_accuracy(results):
    """Compute per-specialty accuracy from evaluation details."""
    specialty_stats = defaultdict(lambda: {"correct": 0, "total": 0})
    for item in results.get("details", []):
        specialty = item.get("specialty", "General")
        specialty_stats[specialty]["total"] += 1
        if item.get("is_correct"):
            specialty_stats[specialty]["correct"] += 1
    return specialty_stats


def plot_specialty_accuracy(specialty_stats, output_file="accuracy_by_specialty.png"):
    """Plot accuracy per specialty and save to an image file."""
    if not specialty_stats:
        print("No specialty data to plot.")
        return

    specialties = sorted(specialty_stats.keys())
    accuracies = [
        (specialty_stats[s]["correct"] / specialty_stats[s]["total"] * 100)
        if specialty_stats[s]["total"] > 0
        else 0.0
        for s in specialties
    ]

    plt.figure(figsize=(10, 6))
    bars = plt.bar(specialties, accuracies, color="#3b82f6", edgecolor="#1d4ed8", width=0.55)
    plt.xlabel("Speciality", fontsize=12, fontweight="bold")
    plt.ylabel("Accuracy (%)", fontsize=12, fontweight="bold")
    plt.title("Evaluation Accuracy by Medical Speciality", fontsize=14, fontweight="bold", pad=12)
    plt.ylim(0, 105)
    plt.xticks(rotation=45, ha="right", fontsize=10)
    plt.grid(axis="y", linestyle="--", alpha=0.5)

    for bar, acc in zip(bars, accuracies):
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 1.5,
            f"{acc:.1f}%",
            ha="center",
            va="bottom",
            fontsize=9,
        )

    plt.tight_layout()
    plt.savefig(output_file, dpi=300)
    plt.close()
    print(f"Plot successfully saved to {output_file}")


def main():
    data = load_evaluation_results("evaluation_results.json")
    stats = calculate_specialty_accuracy(data)
    plot_specialty_accuracy(stats, "accuracy_by_specialty.png")


if __name__ == "__main__":
    main()
