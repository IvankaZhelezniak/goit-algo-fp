# Використання методу Монте-Карло для моделювання кидків двох кубиків
# і порівняння емпіричних ймовірностей із аналітичними.


"""
Як запустити
У терміналі з папки проєкту:

python task_7.py                            # 500 000 кидків за замовчуванням
python task_7.py --trials 1000000           # інша кількість кидків
python task_7.py --trials 300000 --seed 42  # фіксована випадковість

Після запуску:
- у консоль виведеться таблиця та метрики;
- у поточній папці з’являться dice_probabilities.csv, dice_probabilities.png і readme.md.
"""

from __future__ import annotations

import argparse
import csv
import math
import random
from collections import Counter
from pathlib import Path

import matplotlib.pyplot as plt


def analytic_probabilities() -> dict[int, float]:
    """
    Аналітичні ймовірності сум 2..12 для двох чесних d6.
    Кількість способів отримати суму s: 1,2,3,4,5,6,5,4,3,2,1 (усього 36).
    """
    ways = {2: 1, 3: 2, 4: 3, 5: 4, 6: 5, 7: 6, 8: 5, 9: 4, 10: 3, 11: 2, 12: 1}
    return {s: c / 36.0 for s, c in ways.items()}


def simulate(trials: int, seed: int | None = None) -> Counter[int]:
    """
    Монте-Карло симуляція: кидаємо два кубики 'trials' разів.
    Повертаємо лічильник сум.
    """
    if seed is not None:
        random.seed(seed)
    cnt = Counter()
    for _ in range(trials):
        s = random.randint(1, 6) + random.randint(1, 6)
        cnt[s] += 1
    return cnt


def to_probabilities(counts: Counter[int], total: int) -> dict[int, float]:
    """Перетворює лічильники на ймовірності сум 2..12."""
    return {s: counts.get(s, 0) / float(total) for s in range(2, 13)}


def print_table(sim_p: dict[int, float], an_p: dict[int, float], counts: Counter[int], total: int) -> None:
    """Друк таблиці в консоль."""
    header = f"{'Сума':>4} | {'К-ть':>8} | {'Монте-Карло':>13} | {'Аналітика':>10} | {'Похибка':>9}"
    print(header)
    print("-" * len(header))
    for s in range(2, 13):
        c = counts.get(s, 0)
        sp = sim_p[s] * 100
        ap = an_p[s] * 100
        err = abs(sp - ap)
        print(f"{s:>4} | {c:>8} | {sp:>12.2f}% | {ap:>9.2f}% | {err:>8.2f}%")
    print("-" * len(header))
    # Підсумкові метрики
    mae = sum(abs(sim_p[s] - an_p[s]) for s in range(2, 13)) / 11.0
    rmse = math.sqrt(sum((sim_p[s] - an_p[s]) ** 2 for s in range(2, 13)) / 11.0)
    max_err = max(abs(sim_p[s] - an_p[s]) for s in range(2, 13))
    print(f"MAE:  {mae*100:.4f}%   RMSE: {rmse*100:.4f}%   MAX: {max_err*100:.4f}%  (тестів: {total})")


def save_csv(path: Path, sim_p: dict[int, float], an_p: dict[int, float], counts: Counter[int], total: int) -> None:
    """Зберігає результати у CSV."""
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["sum", "count", "sim_probability", "analytic_probability", "abs_error"])
        for s in range(2, 13):
            sp = sim_p[s]
            ap = an_p[s]
            w.writerow([s, counts.get(s, 0), sp, ap, abs(sp - ap)])


def save_plot(path: Path, sim_p: dict[int, float], an_p: dict[int, float]) -> None:
    """Будує та зберігає стовпчиковий графік."""
    sums = list(range(2, 13))
    sim_vals = [sim_p[s] * 100 for s in sums]
    an_vals = [an_p[s] * 100 for s in sums]

    plt.figure(figsize=(9, 5))
    width = 0.38
    x = range(len(sums))
    plt.bar([i - width / 2 for i in x], an_vals, width, label="Аналітика")
    plt.bar([i + width / 2 for i in x], sim_vals, width, label="Монте-Карло")
    plt.xticks(list(x), sums)
    plt.ylabel("Ймовірність, %")
    plt.xlabel("Сума на двох кубиках")
    plt.title("Ймовірності сум: аналітичні vs Монте-Карло")
    plt.legend()
    plt.tight_layout()
    plt.savefig(path, dpi=150)
    plt.close()


def save_readme(path: Path, trials: int, mae: float, rmse: float, max_err: float) -> None:
    """Короткі висновки у markdown."""
    text = f"""# Метод Монте-Карло — кидки двох кубиків

- Кількість симуляцій: **{trials:,}**
- Середня абсолютна похибка (MAE): **{mae*100:.4f}%**
- RMSE: **{rmse*100:.4f}%**
- Максимальне відхилення для однієї суми: **{max_err*100:.4f}%**

Емпіричні ймовірності добре збігаються з аналітичними (1/36, 2/36, …, 1/36).
Зі збільшенням кількості симуляцій похибки зменшуються відповідно до Закону великих чисел.

Файли:
- `dice_probabilities.csv` — таблиця з частотами та ймовірностями
- `dice_probabilities.png` — графік (аналітика vs Монте-Карло)
"""
    path.write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Монте-Карло для двох кубиків")
    parser.add_argument("--trials", type=int, default=500_000, help="кількість кидків (default: 500000)")
    parser.add_argument("--seed", type=int, default=None, help="фіксований seed для відтворюваності")
    args = parser.parse_args()

    # 1) Симуляція
    counts = simulate(args.trials, args.seed)
    sim_p = to_probabilities(counts, args.trials)
    an_p = analytic_probabilities()

    # 2) Друк таблиці та метрик
    print_table(sim_p, an_p, counts, args.trials)

    # 3) Збереження результатів
    out_dir = Path(".")
    csv_path = out_dir / "dice_probabilities.csv"
    png_path = out_dir / "dice_probabilities.png"

    save_csv(csv_path, sim_p, an_p, counts, args.trials)
    save_plot(png_path, sim_p, an_p)

    # 4) Висновки (readme.md)
    mae = sum(abs(sim_p[s] - an_p[s]) for s in range(2, 13)) / 11.0
    rmse = math.sqrt(sum((sim_p[s] - an_p[s]) ** 2 for s in range(2, 13)) / 11.0)
    max_err = max(abs(sim_p[s] - an_p[s]) for s in range(2, 13))
    save_readme(Path("readme.md"), args.trials, mae, rmse, max_err)


if __name__ == "__main__":
    main()

