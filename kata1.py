"""
    Find the length of longest montonous contiguous substring.
    2013-03-26
"""


def longest_monotonous_substring(s):
    if len(s) <= 1:
        return len(s)

    max_length = 1
    length = 1
    is_increasing = int(s[1]) > int(s[0])
    is_decreasing = int(s[1]) < int(s[0])

    for i in range(1, len(s)):
        current = int(s[i])
        previous = int(s[i - 1])
        if current > previous and is_increasing:
            length += 1
        elif current < previous and is_decreasing:
            length += 1
        else:
            length = 1 if current == previous else 2
            is_decreasing = current < previous
            is_increasing = current > previous

        if length > max_length:
            max_length = length

    return max_length


def test_all():
    assert longest_monotonous_substring('') == 0
    assert longest_monotonous_substring('1') == 1
    assert longest_monotonous_substring('11') == 1
    assert longest_monotonous_substring('111') == 1
    assert longest_monotonous_substring('12') == 2
    assert longest_monotonous_substring('123') == 3
    assert longest_monotonous_substring('123456789') == 9
    assert longest_monotonous_substring('987654321') == 9
    assert longest_monotonous_substring('012300000') == 4
    assert longest_monotonous_substring('21') == 2
    assert longest_monotonous_substring('321') == 3
    assert longest_monotonous_substring('0321') == 3
    assert longest_monotonous_substring('013876543') == 6