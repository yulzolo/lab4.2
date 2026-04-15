# list.py
class ListNode:
    """Узел двусвязного списка"""

    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None


class DoublyLinkedList:
    """Двусвязный список на Python"""

    def __init__(self):
        self.head = None
        self.tail = None
        self.count = 0

    def insert(self, index, value):
        """Вставка элемента по индексу"""
        if index < 0 or index > self.count:
            raise IndexError("Неверный индекс")

        new_node = ListNode(value)

        if self.count == 0:
            self.head = self.tail = new_node
        elif index == 0:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node
        elif index == self.count:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node
        else:
            current = self.head
            for _ in range(index):
                current = current.next
            new_node.prev = current.prev
            new_node.next = current
            current.prev.next = new_node
            current.prev = new_node

        self.count += 1

    def delete(self, index):
        """Удаление элемента по индексу"""
        if self.count == 0 or index < 0 or index >= self.count:
            raise IndexError("Неверный индекс")

        current = self.head
        for _ in range(index):
            current = current.next

        if current.prev:
            current.prev.next = current.next
        else:
            self.head = current.next

        if current.next:
            current.next.prev = current.prev
        else:
            self.tail = current.prev

        self.count -= 1

    def get_element(self, index):
        """Получение элемента по индексу"""
        if index < 0 or index >= self.count:
            return None
        current = self.head
        for _ in range(index):
            current = current.next
        return current.data

    def get_count(self):
        """Количество элементов"""
        return self.count