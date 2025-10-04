# Візуалізація обходу бінарного дерева (DFS/BFS).

# Ітеративні алгоритми (стек для DFS, черга для BFS). 
# Кольори вузлів змінюються від темного до світлого залежно від порядку відвідування (бходу).


import uuid
from collections import deque
import matplotlib.pyplot as plt
import networkx as nx


# Базова модель вузла (як у Завданні 4) 
class Node:
    def __init__(self, key, color="#87CEEB"):  # skyblue за замовчуванням
        self.left = None
        self.right = None
        self.val = key
        self.color = color
        self.id = str(uuid.uuid4())  # унікальний id для графа


# Побудова графа з дерева й малювання 
def add_edges(graph, node, pos, x=0.0, y=0.0, layer=1):
    """Рекурсивне додавання ребер/вузлів для фігури (тільки побудова позицій)."""
    if node is None:
        return graph
    graph.add_node(node.id, color=node.color, label=node.val)
    if node.left:
        graph.add_edge(node.id, node.left.id)
        lx = x - 1 / (2 ** layer)
        pos[node.left.id] = (lx, y - 1)
        add_edges(graph, node.left, pos, x=lx, y=y - 1, layer=layer + 1)
    if node.right:
        graph.add_edge(node.id, node.right.id)
        rx = x + 1 / (2 ** layer)
        pos[node.right.id] = (rx, y - 1)
        add_edges(graph, node.right, pos, x=rx, y=y - 1, layer=layer + 1)
    return graph


def draw_tree(tree_root, title=""):
    """Малює дерево відповідно до поточних кольорів вузлів."""
    tree = nx.DiGraph()
    pos = {tree_root.id: (0, 0)}
    add_edges(tree, tree_root, pos)

    colors = [d["color"] for _, d in tree.nodes(data=True)]
    labels = {n: d["label"] for n, d in tree.nodes(data=True)}
    plt.clf()
    plt.title(title)
    nx.draw(
        tree,
        pos=pos,
        labels=labels,
        arrows=False,
        node_size=2000,
        node_color=colors,
        linewidths=1.5,
        with_labels=True,
        font_weight="bold",
    )
    plt.tight_layout()
    plt.draw()


# Допоміжні утиліти
def hex_to_rgb(hex_color):
    """'#RRGGBB' -> (R,G,B) у [0..255]"""
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))


def rgb_to_hex(rgb):
    """(R,G,B) -> '#RRGGBB'"""
    return "#{:02X}{:02X}{:02X}".format(*rgb)


def make_gradient(n, dark="#08306B", light="#DEEBF7"):
    """
    Генерує n HEX-кольорів від темного до світлого.
    За замовчуванням — від темно-синього до дуже світлого синього.
    """
    if n <= 0:
        return []
    r1, g1, b1 = hex_to_rgb(dark)
    r2, g2, b2 = hex_to_rgb(light)
    out = []
    for i in range(n):
        t = i / max(n - 1, 1)  # 0..1
        r = int(r1 + (r2 - r1) * t)
        g = int(g1 + (g2 - g1) * t)
        b = int(b1 + (b2 - b1) * t)
        out.append(rgb_to_hex((r, g, b)))
    return out


def count_nodes(root):
    """Рахую кількість вузлів ітеративно (щоб підготувати градієнт)."""
    if not root:
        return 0
    q = deque([root])
    cnt = 0
    while q:
        node = q.popleft()
        cnt += 1
        if node.left:
            q.append(node.left)
        if node.right:
            q.append(node.right)
    return cnt


def reset_colors(root, color="#87CEEB"):
    """Скидує кольори всіх вузлів (ітеративно)."""
    if not root:
        return
    q = deque([root])
    while q:
        node = q.popleft()
        node.color = color
        if node.left:
            q.append(node.left)
        if node.right:
            q.append(node.right)


#  Візуалізація обходів
def bfs_visualize(root, animate=True, pause=0.7,
                  dark="#0B3D91", light="#B3D4FF"):
    """
    Обхід у ширину (BFS) чергою. Кожен крок — новий колір від темного до світлого.
    """
    if root is None:
        return

    reset_colors(root)
    total = count_nodes(root)
    palette = make_gradient(total, dark, light)

    visited = set()
    order_index = 0
    q = deque([root])

    plt.figure(figsize=(9, 5))
    draw_tree(root, title="BFS: старт")

    while q:
        node = q.popleft()
        if node.id in visited:
            continue
        visited.add(node.id)

        # фарбує вузол відповідно до кроку
        node.color = palette[order_index]
        order_index += 1

        # малює крок
        draw_tree(root, title=f"BFS: крок {order_index}")
        if animate:
            plt.pause(pause)

        # додає сусідів у чергу
        if node.left:
            q.append(node.left)
        if node.right:
            q.append(node.right)

    # фінальний кадр
    draw_tree(root, title="BFS: завершено")
    plt.show()


def dfs_visualize(root, animate=True, pause=0.7,
                  dark="#00441B", light="#C7E9C0"):
    """
    Обхід у глибину (DFS) СТЕКОМ (preorder). Без рекурсії.
    Щоб класичний порядок був 'ліворуч-праворуч', спершу кладу правий.
    """
    if root is None:
        return

    reset_colors(root)
    total = count_nodes(root)
    palette = make_gradient(total, dark, light)

    visited = set()
    order_index = 0
    stack = [root]

    plt.figure(figsize=(9, 5))
    draw_tree(root, title="DFS: старт")

    while stack:
        node = stack.pop()
        if node.id in visited:
            continue
        visited.add(node.id)

        # фарбує вузол відповідно до кроку
        node.color = palette[order_index]
        order_index += 1

        # малює крок
        draw_tree(root, title=f"DFS: крок {order_index}")
        if animate:
            plt.pause(pause)

        # кладе в стек спочатку правого, потім лівого — щоб лівий обробився першим
        if node.right:
            stack.append(node.right)
        if node.left:
            stack.append(node.left)

    # фінальний кадр
    draw_tree(root, title="DFS: завершено")
    plt.show()


# DEMO
if __name__ == "__main__":
    # Те саме дерево, що й у Завданні 4:
    root = Node(0)
    root.left = Node(4)
    root.left.left = Node(5)
    root.left.right = Node(10)
    root.right = Node(1)
    root.right.left = Node(3)

    # BFS (черга). Можна поставити animate=False, якщо не потрібна покрокова анімація
    bfs_visualize(root, animate=True, pause=0.6)

    # DFS (стек)
    dfs_visualize(root, animate=True, pause=0.6)
