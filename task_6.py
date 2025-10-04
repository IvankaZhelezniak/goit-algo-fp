"""
Жадібний алгоритм та динамічне програмування
для вибору їжі з максимальною калорійністю в межах бюджету.

— greedy_algorithm: Жадібний алгоритм: бере страви у порядку спадання (калорії/вартість),
  поки не вичерпано бюджет (не гарантує оптимум).
— dynamic_programming: класичний 0/1 knapsack за калоріями, гарантує оптимум. 
  повертає назви страв, максимальні калорії та їхню загальну вартість при заданому бюджеті.
"""

from dataclasses import dataclass
from typing import Dict, List, Tuple


@dataclass(frozen=True)
class Item:
    name: str
    cost: int
    calories: int


def normalize_items(items_dict: Dict[str, Dict[str, int]]) -> List[Item]:
    """З перданого словника формую зручний список Item."""
    return [Item(name=k, cost=v["cost"], calories=v["calories"])
            for k, v in items_dict.items()]


def greedy_algorithm(items_dict: Dict[str, Dict[str, int]], budget: int) -> Tuple[List[str], int, int]:
    """
    Жадібний вибір за найбільшим ratio (calories / cost).
    Повертає (список_страв, сумарні_калорії, сумарна_вартість).
    """
    items = normalize_items(items_dict)

    # Сортую за: кращий ratio -> більше калорій -> дешевше -> назва (стабільність)
    items.sort(key=lambda it: (it.calories / it.cost, it.calories, -it.cost, it.name), reverse=True)

    chosen: List[str] = []
    total_cal = 0
    total_cost = 0

    for it in items:
        if total_cost + it.cost <= budget:
            chosen.append(it.name)
            total_cost += it.cost
            total_cal += it.calories

    return chosen, total_cal, total_cost


def dynamic_programming(items_dict: Dict[str, Dict[str, int]], budget: int) -> Tuple[List[str], int, int]:
    """
    ДП (0/1 knapsack) для максимізації калорій при обмеженні бюджету.
    Повертає (список_страв, сумарні_калорії, сумарна_вартість).
    Складність: O(n * budget) за часом та пам'яттю.
    """
    items = normalize_items(items_dict)
    n = len(items)

    # dp[i][w] = максимум калорій з перших i предметів при бюджеті w
    dp = [[0] * (budget + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        cost_i = items[i - 1].cost
        cal_i = items[i - 1].calories
        for w in range(budget + 1):
            # не беру i-й
            dp[i][w] = dp[i - 1][w]
            # беру i-й (якщо влізає)
            if cost_i <= w:
                cand = dp[i - 1][w - cost_i] + cal_i
                if cand > dp[i][w]:
                    dp[i][w] = cand

    # Відновлюю вибір (backtracking з dp)
    chosen: List[str] = []
    w = budget
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:  # предмет i-1 використаний
            chosen.append(items[i - 1].name)
            w -= items[i - 1].cost

    chosen.reverse()
    total_cal = dp[n][budget]
    total_cost = sum(items_dict[name]["cost"] for name in chosen)
    return chosen, total_cal, total_cost


#  DEMO
if __name__ == "__main__":
    items = {
        "pizza": {"cost": 50, "calories": 300},
        "hamburger": {"cost": 40, "calories": 250},
        "hot-dog": {"cost": 30, "calories": 200},
        "pepsi": {"cost": 10, "calories": 100},
        "cola": {"cost": 15, "calories": 220},
        "potato": {"cost": 25, "calories": 350},
    }

    budget = 100

    g_set, g_cal, g_cost = greedy_algorithm(items, budget)
    d_set, d_cal, d_cost = dynamic_programming(items, budget)

    print("Жадібний алгоритм:")
    print("  Обрано:", g_set)
    print("  Калорії:", g_cal, "  Вартість:", g_cost)

    print("\nДинамічне програмування (оптимум):")
    print("  Обрано:", d_set)
    print("  Калорії:", d_cal, "  Вартість:", d_cost)
