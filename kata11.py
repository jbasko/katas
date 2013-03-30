"""
    2013-03-30 String Calculator
    http://craftsmanship.sv.cmu.edu/katas/string-calculator

    >>> add('')
    0
    >>> add('1')
    1
    >>> add('10')
    10
    >>> add('1,2')
    3
    >>> add('10,3')
    13
    >>> add('10,10,10,5')
    35
"""
import re
from unittest.case import TestCase


def add(s):
    numbers = []
    if s.startswith("//"):
        delimiter = s[2]
        delimiter_pattern = re.compile(re.escape(delimiter))
        s = s.split("\n")[1]
    else:
        delimiter_pattern = re.compile(",|\n")

    negative_values = []
    for n in delimiter_pattern.split(s):
        if n:
            if int(n) < 0:
                negative_values.append(n)
            elif int(n) > 1000:
                continue
            else:
                numbers.append(int(n))

    if negative_values:
        raise NegativeNotAllowed(','.join(negative_values))
    return sum(numbers)


class NegativeNotAllowed(Exception):
    pass


class AddTest(TestCase):

    def test_newline_is_valid_delimiter(self):
        self.assertEqual(6, add("1\n2,3"))

    def test_alternative_delimiter(self):
        self.assertEqual(6, add("//:\n1:2:3"))

    def test_negatives_not_allowed(self):
        self.assertRaises(NegativeNotAllowed, add, '-1')

        try:
            add('-1,-2,3,-4')
            self.fail()
        except NegativeNotAllowed as exception:
            self.assertEqual('-1,-2,-4', exception.message)

    def test_ignore_numbers_greater_than_1000(self):
        self.assertEqual(2, add('1001,2'))

    def test_multichar_delimiter(self):
        self.assertEqual(6, add("//***\n1***2***3"))
