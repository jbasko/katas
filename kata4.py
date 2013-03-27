"""
    convert romans to decimals
    2013-03-27 evening
"""
from unittest.case import TestCase


def to_decimal(roman_numeral):
    if not roman_numeral:
        raise ValueError

    if len(roman_numeral) <= 1:
        return _decimal(roman_numeral)

    def _decimal_at(i):
        return _decimal(roman_numeral[i])

    def is_increasing_at(i):
        if i < 1:
            raise ValueError
        return _decimal_at(i) > _decimal_at(i - 1)

    def is_decreasing_at(i):
        if i < 1:
            raise ValueError
        return _decimal_at(i) < _decimal_at(i - 1)

    def is_stable_at(i):
        if i < 1:
            raise ValueError
        return _decimal_at(i) == _decimal_at(i - 1)

    parts = [_decimal_at(0)]

    was_increasing = _decimal_at(1) > _decimal_at(0)
    was_decreasing = _decimal_at(1) < _decimal_at(0)

    for i in range(1, len(roman_numeral)):

        if is_increasing_at(i):
            parts[-1] = _decimal_at(i) - parts[-1]
            was_increasing = False
            was_decreasing = False
            continue
        else:
            if was_increasing:
                parts[-1] *= -1
            parts.append(_decimal_at(i))

        was_increasing = is_increasing_at(i) or (was_increasing and is_stable_at(i))
        was_decreasing = is_decreasing_at(i) or (was_decreasing and is_stable_at(i))

    return sum(parts)


def _decimal(roman_digit):
    basics = {
        'i': 1,
        'v': 5,
        'x': 10,
        'l': 50,
        'c': 100,
        'd': 500,
        'm': 1000,
    }
    if roman_digit.lower() not in basics:
        raise ValueError
    return basics[roman_digit.lower()]


class RomansToDecimalsTest(TestCase):
    def test_all(self):
        self.assertRaises(ValueError, to_decimal, None)
        self.assertRaises(ValueError, to_decimal, 'z')
        self.assertRaises(ValueError, to_decimal, 'iz')

        self.assertEqual(1, to_decimal('i'))
        self.assertEqual(1, to_decimal('I'))

        self.assertEqual(5, to_decimal('v'))
        self.assertEqual(10, to_decimal('x'))
        self.assertEqual(50, to_decimal('l'))

        self.assertEqual(2, to_decimal('ii'))
        self.assertEqual(3, to_decimal('iii'))
        self.assertEqual(6, to_decimal('vi'))
        self.assertEqual(7, to_decimal('vii'))
        self.assertEqual(8, to_decimal('viii'))
        self.assertEqual(18, to_decimal('xviii'))
        self.assertEqual(78, to_decimal('LXXVIII'))

        self.assertEqual(4, to_decimal('iv'))
        self.assertEqual(9, to_decimal('ix'))

        self.assertEqual(14, to_decimal('xiv'))
        self.assertEqual(16, to_decimal('xvi'))

        self.assertEqual(49, to_decimal('XLIX'))
        self.assertEqual(89, to_decimal('LXXXIX'))
        self.assertEqual(99, to_decimal('XCIX'))

        self.assertEqual(890, to_decimal('DCCCXC'))