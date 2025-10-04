# Функція, яка реалізує реверсування однозв'язного списку, яка змінює посилання між вузлами. 
# Алгоритм сортування (функція) для однозв'язного списку.
# Функція, що об'єднує два відсортовані однозв'язні списки в один відсортований список. 

# feat(linked-list): Реалізовано однозв’язний список:
# - reverse(): реверсування списку in-place (зміна посилань .next)
# - sort(): сортування списку алгоритмом merge sort (O(n log n))
# - merge_two_sorted_lists(): об'єднання двох відсортованих списків у один


# Однозв'язний список 
class Node:
    def __init__(self, data=None):
        self.data = data   # значення вузла
        self.next = None   # посилання на наступний вузол (за замовчуванням немає)


class LinkedList:
    def __init__(self, iterable=None):
        self.head = None         # голова списку (перший вузол)
        if iterable:
            for x in iterable:
                self.insert_at_end(x)

    # базові операції
    def insert_at_beginning(self, data):
        n = Node(data)
        # нове посилання нового вузла на поточну голову:
        n.next = self.head          # <- зміна посилання
        # Головою стає новий вузол:
        self.head = n        # (посилання head змінилось)

    def insert_at_end(self, data):
        n = Node(data)
        if not self.head:
            self.head = n
            return
        cur = self.head
        while cur.next:
            cur = cur.next
        # Останній вузол тепер вказує на новий:
        cur.next = n                 # <- зміна посилання

    def to_list(self):
        out = []
        cur = self.head
        while cur:
            out.append(cur.data)
            cur = cur.next
        return out

    # 1) Реверсування списку (in-place)
    # Ідея: ітеруємось і для кожного вузла розвертаємо стрілку .next у зворотний бік.
    # Складність: O(n) за часом, O(1) за пам'яттю
    def reverse(self):
        prev = None
        cur = self.head
        while cur:
            nxt = cur.next    # зберігаємо посилання
            cur.next = prev   # розвертаємо лінк
            prev = cur        # зсуваємо вказівники
            cur = nxt         # рухаємось далі праворуч
        self.head = prev      # голова тепер там, де був "хвіст"

    # 2) Сортування однозв'язного списку МЕРДЖ-СОРТОМ (merge sort)
    # Підходить для однозв'язних: не потребує випадкового доступу, тільки робота з посиланнями.
    # Складність: O(n log n), пам'ять O(log n) за рекурсивну глибину
    def sort(self):
        self.head = self._merge_sort(self.head)

    def _merge_sort(self, head):
        # База рекурсії: 0 або 1 вузол — уже відсортовано
        if head is None or head.next is None:
            return head

        # розділяємо список навпіл (slow/fast) і розриваємо
        slow, fast = head, head.next
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
        
        # mid — початок правої половини
        mid = slow.next
        slow.next = None       # тут "рвемо" посилання, тепер це два окремі списки

        left = self._merge_sort(head)
        right = self._merge_sort(mid)
        return self._merge_sorted_heads(left, right)

    @staticmethod
    def _merge_sorted_heads(a, b):
        """Зливаю 2 відсортовані підсписки (голови a і b), повертаю голову.
        Працюю тільки посиланнями: перекидаю вузли в новий порядок без створення масивів."""

        dummy = Node()   # технічний вузол-«сторож»
        tail = dummy     # кінець зібраного списку

        # Поки обидві частини мають елементи — завжди приєдную менший
        while a and b:
            if a.data <= b.data:
                tail.next = a         # <- приєднала "a" після tail (зміна посилання)
                a = a.next            # зсуваю "голову" лівої частини
            else:
                tail.next = b         # <- приднала "b" після tail (зміна посилання)
                b = b.next            # зсуваю "голову" правої частини
            tail = tail.next          # хвіст нової послідовності зсувається на доданий вузол

        # Приєдную "хвіст" тієї частини, що залишилась
        tail.next = a if a else b      # <- одним рядком перекинула решту посилань

        return dummy.next              # пропускаю «сторожа» і повертаю справжню голову


# 3) Об'єднання двох відсортованих однозв'язних списків 
# Повертає НОВИЙ список, що містить елементи у відсортованому порядку.
# Використовую той самий механізм злиття (_merge_sorted_heads).
def merge_two_sorted_lists(list1: LinkedList, list2: LinkedList) -> LinkedList:
    merged = LinkedList()
    # Тут не копіюю дані — просто перекидаю посилання між вузлами:
    merged.head = LinkedList._merge_sorted_heads(list1.head, list2.head)  # <- злиття посиланнями
    return merged


#  приклад використання
if __name__ == "__main__":
    ll = LinkedList([5, 1, 7, 3, 2])
    print("Початковий:", ll.to_list())          # [5, 1, 7, 3, 2]

    ll.reverse()
    print("Після reverse():", ll.to_list())     # [2, 3, 7, 1, 5]

    ll.sort()
    print("Після sort():", ll.to_list())        # [1, 2, 3, 5, 7]

    a = LinkedList([1, 4, 6])
    b = LinkedList([2, 3, 5, 7])
    merged = merge_two_sorted_lists(a, b)
    print("Злиття двох відсортованих:", merged.to_list())  # [1,2,3,4,5,6,7]
