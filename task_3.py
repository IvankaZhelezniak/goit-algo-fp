# Дерева, алгоритм Дейкстри

# алгоритм Дейкстри для знаходження найкоротших шляхів у зваженому графі, використовуючи бінарну купу. 
# Створений граф, використані піраміди для оптимізації вибору вершин та обчислення найкоротших шляхів 
# від початкової вершини до всіх інших.

# Реалізація Дейкстри з бінарною купою (heapq) для пошуку найкоротших шляхів у зваженому графі.

from collections import defaultdict
import heapq

class Graph:
    def __init__(self, directed=False):
        # adj[u] = список пар (v, w) — ребра u->v з вагою w
        self.adj = defaultdict(list)
        self.directed = directed

    def add_edge(self, u, v, w: float):
        # Додаю ребро з вагою w (ваги мають бути невід’ємні). Для неорієнтованого графа додає обидва напрямки.
        if w < 0:
            raise ValueError("Алгоритм Дейкстри працює лише з невід’ємними вагами")
        
        # Гарантує наявність ключів у словнику для всіх вершин (навіть без вихідних ребер)
        _ = self.adj[u]
        _ = self.adj[v]
        
        # u -> v (з вагою w)
        self.adj[u].append((v, w))

        # якщо граф НЕорієнтований — додаю зворотне ребро v -> u
        if not self.directed:
            self.adj[v].append((u, w))

def dijkstra_heap(G: Graph, start):
    """
    Алгоритм Дейкстри з бінарною купою.
    Повертає кортеж (dist, parent), де:
      - dist[v]   — найкоротша відстань від start до v
      - parent[v] — попередник v у найкоротшому шляху (для відновлення маршруту)
    Складність: O((V + E) * log V).
    """
    # 1) Ініціалізація: усі відстані — нескінченність, start = 0
    dist = {v: float("inf") for v in G.adj}
    parent = {v: None for v in G.adj}
    if start not in dist:
        # Якщо стартова вершина відсутня в графі (навіть як "порожня"),
        # вважатимемо її ізольованою вершиною.
        dist[start] = 0.0
        parent[start] = None
        G.adj[start]  # створюю пустий список суміжності

    dist[start] = 0.0

    # 2) Пріоритетна черга (мін-купа). Кладу початковий запис (0, start).
    # Кортеж вигляду (поточна_відстань, вершина) — перший елемент кортежу є пріоритетом.
    pq = [(0.0, start)]  #  це і є бінарна купа з одним елементом

    while pq:
        # 3) Дістаю вершину з найменшою поточною відстанню (вершина зверху мін-купи).
        d, u = heapq.heappop(pq)

        # 3a) Якщо цей запис "застарів" (у словнику вже менша відстань) — пропускаю.
        if d != dist[u]:
            continue
        
        # 4) Релаксую всі ребра u -> v
        for v, w in G.adj[u]:
            # (захист від некоректних даних; Дейкстра — тільки для невід’ємних ваг)
            if w < 0:
                raise ValueError("Алгоритм Дейкстри вимагає невід’ємних ваг ребер")

            nd = d + w             # нова потенційна відстань до v через u
            if nd < dist.get(v, float("inf")):
                dist[v] = nd
                parent[v] = u

                # Додаю кандидата у МІН-КУПУ. Перший елемент кортежу (nd) — ключ пріоритету.
                # Оскільки heapq — мін-купа, зверху завжди опиниться вершина з найменшою nd.
                # Це і дає логарифмічну вартість вибору наступної "найближчої" вершини.
                # Я не оновлюємо існуючий елемент "на місці" (heapq цього не вміє),
                # просто пушу новий запис. Старий запис, якщо він є, стане "застарілим" і буде відсіяний перевіркою d != dist[u] при pop.
                heapq.heappush(pq, (nd, v))
    return dist, parent

def restore_path(parent, start, target):
    """
    Відновлює шлях start→target за за словником попередників parent.
    Повертає список вершин у порядку проходження або None, якщо цілі недосяжна."""
    if start == target:
        return [start]
    if target not in parent and target != start:
        return None

    path = []
    cur = target
    while cur is not None:
        path.append(cur)
        if cur == start:
            break
        cur = parent.get(cur)

    if not path or path[-1] != start:
        return None
    return list(reversed(path))

if __name__ == "__main__":
    # Приклад з конспекту (неорієнтований зважений граф)
    G = Graph(directed=False)
    G.add_edge('A', 'B', 5)
    G.add_edge('A', 'C', 10)
    G.add_edge('B', 'D', 3)
    G.add_edge('C', 'D', 2)
    G.add_edge('D', 'E', 4)

    start = input("Початкова вершина (наприклад, A): ").strip() or 'A'

    dist, parent = dijkstra_heap(G, start)

    print("\nНайкоротші відстані від", start)
    for v in sorted(dist):
        d = dist[v]
        print(f"  {v}: {'∞' if d == float('inf') else d}")

    print("\nШляхи:")
    for v in sorted(dist):
        path = restore_path(parent, start, v)
        if path is None:
            print(f"  {start} -> {v}: недосяжно")
        else:
            print(f"  {start} -> {v}: {' -> '.join(path)} (довжина {dist[v]})")
