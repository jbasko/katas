
LOOKUP = {
    'i': 1,
    'v': 5,
    'x': 10,
    'l': 50,
    'c': 100,
    'd': 500,
    'm': 1000,
}


def to_decimal(roman: str):

    roman = roman.lower()

    # First, group all consecutive identical digits.

    groups = [
        [roman[0], LOOKUP[roman[0]]],
    ]

    for i in range(1, len(roman)):
        unit = LOOKUP[roman[i]]
        if roman[i] == groups[-1][0]:
            groups[-1][1] += unit
        else:
            groups.append([roman[i], unit])

    if len(groups) == 1:
        return groups[0][1]

    # Go through groups in reverse order.
    # If a smaller unit precedes a greater one then the
    # smaller unit's group represents value to reduce
    # the total value by: IX = 10 - 1.

    value = groups[-1][1]

    for i in range(len(groups) - 2, -1, -1):
        g = groups[i]
        g_unit = LOOKUP[g[0]]
        h = groups[i + 1]
        h_unit = LOOKUP[h[0]]
        if g_unit < h_unit:
            value -= g[1]
        else:
            value += g[1]

    return value


def test_all():

    assert 1 == to_decimal('i')
    assert 1 == to_decimal('I')

    assert 5 == to_decimal('v')
    assert 10 == to_decimal('x')
    assert 50 == to_decimal('l')

    assert 2 == to_decimal('ii')
    assert 3 == to_decimal('iii')
    assert 6 == to_decimal('vi')
    assert 7 == to_decimal('vii')
    assert 8 == to_decimal('viii')
    assert 18 == to_decimal('xviii')
    assert 78 == to_decimal('LXXVIII')

    assert 4 == to_decimal('iv')
    assert 9 == to_decimal('ix')

    assert 14 == to_decimal('xiv')
    assert 16 == to_decimal('xvi')

    assert 49 == to_decimal('XLIX')
    assert 89 == to_decimal('LXXXIX')
    assert 99 == to_decimal('XCIX')

    assert 890 == to_decimal('DCCCXC')


if __name__ == '__main__':
    test_all()
