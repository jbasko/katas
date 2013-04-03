"""
    2013-04-03 Google Question #1: reverse adjacent nodes in a linked list
    http://learn.hackerearth.com/questions/?company=Google
"""
from unittest.case import TestCase


class Node(object):

    def __init__(self, value, next_node=None):
        self.value = value
        self.next_node = next_node

    def __str__(self):
        next_value = self.next_node.value if self.next_node else 'None'
        return '[{}->{}]'.format(self.value, next_value)


class List(object):

    def __init__(self):
        self.head = None

    def append(self, value):
        new_node = Node(value)
        if self.head:
            tail = self.head
            while tail.next_node:
                tail = tail.next_node
            tail.next_node = new_node
        else:
            self.head = new_node

    def __str__(self):
        values = []
        current = self.head
        while current:
            values.append(str(current.value))
            current = current.next_node
        return '[' + ' '.join(values) + ']'


def reverse_adjacent_nodes(llist):
    """
    1 -> 2 -> 3 -> 4 -> 5
    1 = current
    2 = next_node
    3 = next_next_node
    None -> next_node
    next_node -> current
    current -> next_next_node
    """
    current = llist.head
    previous = None
    while current:
        if current.next_node:
            next_node = current.next_node
            next_next_node = next_node.next_node

            if previous:
                # break temporarily
                previous.next_node = None

            # break temporarily
            current.next_node = None

            next_node.next_node = current
            current.next_node = next_next_node
            if previous:
                previous.next_node = next_node

            previous = current
            current = next_next_node

            if previous == llist.head:
                llist.head = next_node
        else:
            break


class ListTest(TestCase):

    def test_creates_and_prints_list(self):
        linked_list = List()
        self.assertEqual('[]', str(linked_list))
        linked_list.append(2)
        linked_list.append(3)
        self.assertEqual('[2 3]', str(linked_list))

    def test_reverses_adjacent_nodes(self):
        b = List()
        for i in range(1, 6):
            b.append(i)

        self.assertEqual('[1 2 3 4 5]', str(b))

        reverse_adjacent_nodes(b)
        self.assertEqual('[2 1 4 3 5]', str(b))

        b = List()
        reverse_adjacent_nodes(b)
        self.assertEqual('[]', str(b))

        b = List()
        b.append(1)
        reverse_adjacent_nodes(b)
        self.assertEqual('[1]', str(b))

        b = List()
        b.append(1)
        b.append(2)
        reverse_adjacent_nodes(b)
        self.assertEqual('[2 1]', str(b))

        b = List()
        b.append(1)
        b.append(2)
        b.append(3)
        b.append(4)
        reverse_adjacent_nodes(b)
        self.assertEqual('[2 1 4 3]', str(b))
