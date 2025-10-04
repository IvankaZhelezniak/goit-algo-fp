# Візуалізація піраміди

# Наступний код виконує побудову бінарних дерев. Виконай аналіз коду, щоб зрозуміти, як він працює.
# Використовуючи як базу цей код, побудуйте функцію, що буде візуалізувати бінарну купу.
# 👉🏻 Примітка. Суть завдання полягає у створенні дерева із купи.
# Функція візуалізує бінарну купу.


# функція, що візуалізує бінарну купу як дерева.

import uuid
import heapq
import networkx as nx
import matplotlib.pyplot as plt


# Вузол і допоміжні функції для малювання дерева 

class Node:
    def __init__(self, key, color="skyblue"):
        self.left = None
        self.right = None
        self.val = key
        self.color = color                 # колір вузла на малюнку
        self.id = str(uuid.uuid4())        # унікальний ідентифікатор вузла


def add_edges(graph, node, pos, x=0.0, y=0.0, layer=1):
    """
    Рекурсивно додає вузли/ребра у граф NetworkX і рахує координати для візуалізації.
    """
    if node is None:
        return graph

    graph.add_node(node.id, color=node.color, label=node.val)

    # ліва дитина
    if node.left:
        graph.add_edge(node.id, node.left.id)
        lx = x - 1 / (2 ** layer)
        pos[node.left.id] = (lx, y - 1)
        add_edges(graph, node.left, pos, x=lx, y=y - 1, layer=layer + 1)

    # права дитина
    if node.right:
        graph.add_edge(node.id, node.right.id)
        rx = x + 1 / (2 ** layer)
        pos[node.right.id] = (rx, y - 1)
        add_edges(graph, node.right, pos, x=rx, y=y - 1, layer=layer + 1)

    return graph


def draw_tree(tree_root, title="Binary Tree"):
    """
    Малює дерево з коренем tree_root за допомогою NetworkX + Matplotlib.
    """
    tree = nx.DiGraph()
    pos = {tree_root.id: (0, 0)}
    add_edges(tree, tree_root, pos)

    colors = [data["color"] for _, data in tree.nodes(data=True)]
    labels = {n: data["label"] for n, data in tree.nodes(data=True)}

    plt.figure(figsize=(9, 6))
    nx.draw(tree, pos=pos, labels=labels, arrows=False,
            node_size=2500, node_color=colors, font_size=12)
    plt.title(title)
    plt.axis("off")
    plt.tight_layout()
    plt.show()


# Побудова ДЕРЕВА з масиву-купи

def heap_list_to_tree(heap_list, node_colors=None):
    """
    Перетворює масив-подання купи (array heap) на дерево з об'єктів Node.

    :param heap_list: список у форматі купи (індекси: i -> left 2i+1, right 2i+2)
    :param node_colors: список/словник кольорів вузлів (опційно)
    :return: корінь дерева (Node)
    """
    if not heap_list:
        raise ValueError("Порожня купа – нічого візуалізувати.")

    # створення всіх вузлів
    nodes = []
    for i, val in enumerate(heap_list):
        color = "skyblue"
        if node_colors is not None:
            if isinstance(node_colors, dict):
                color = node_colors.get(i, color)
            elif isinstance(node_colors, (list, tuple)) and i < len(node_colors):
                color = node_colors[i]
        nodes.append(Node(val, color=color))

    # з’єднує батьків з дітьми (індекси купи)
    n = len(nodes)
    for i in range(n):
        li = 2 * i + 1
        ri = 2 * i + 2
        if li < n:
            nodes[i].left = nodes[li]
        if ri < n:
            nodes[i].right = nodes[ri]

    return nodes[0]  # корінь — елемент з індексом 0


# Головна функція візуалізації купи

def draw_heap(iterable, as_max=False, title=None, node_colors=None):
    """
    Будує купу з iterable за допомогою heapq та візуалізує її як дерево.

    :param iterable: будь-яка послідовність значень
    :param as_max: False -> мін-купа (heapq за замовчуванням),
              True  -> макс-купа (реалізую через інверсію знаку)
    :param title: заголовок графіка
    :param node_colors: кастомні кольори вузлів (список/словник у відповідності з індексами)
    """
    data = list(iterable)

    # heapq надає мін-купу. Для макс-купи інвертуємо знак елементів.
    if as_max:
        tmp = [-x for x in data]
        heapq.heapify(tmp)
        heap_list = [-x for x in tmp]  # повертає знак, але структура індексів – валідна купа
        default_title = "Max-Heap (via sign inversion)"
    else:
        heap_list = data[:]
        heapq.heapify(heap_list)
        default_title = "Min-Heap"

    root = heap_list_to_tree(heap_list, node_colors=node_colors)
    draw_tree(root, title=title or default_title)


#  DEMO 
if __name__ == "__main__":
    # Приклад даних
    values = [7, 12, 3, 18, 1, 9, 15, 2]

    # Мін-купа
    draw_heap(values, as_max=False, title="Мін-купа")

    # Макс-купа
    draw_heap(values, as_max=True, title="Макс-купа")


# heapq.heapify перетворює список на мін-купу на місці.
# draw_heap збирає масив-купу, далі heap_list_to_tree з’єднує вузли за індексами i -> 2i+1, 2i+2, і врешті draw_tree малює дерево.
# Прапор as_max=True робить макс-купу через інверсію знаків (класичний трюк для heapq).