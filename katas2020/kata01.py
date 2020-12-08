"""
    Find the length of longest monotonous contiguous substring.
    2020-12-08 morning
"""


def longest_monotonous_substring(s):
    length = len(s)
    if length < 2:
        return length

    longest, curr_incr, curr_decr = 0, 0, 0

    for i in range(0, length):
        if int(s[i]) == int(s[i - 1]):
            curr_incr += 1
            curr_decr += 1
        elif int(s[i]) < int(s[i-1]):
            curr_incr = 1
            curr_decr += 1
        else:
            curr_incr += 1
            curr_decr = 1
        longest = max(longest, curr_incr, curr_decr)

    return longest


def test_all():
    assert longest_monotonous_substring('') == 0
    assert longest_monotonous_substring('1') == 1
    assert longest_monotonous_substring('11') == 2
    assert longest_monotonous_substring('111') == 3
    assert longest_monotonous_substring('12') == 2
    assert longest_monotonous_substring('1223') == 4
    assert longest_monotonous_substring('1233') == 4
    assert longest_monotonous_substring('112233') == 6
    assert longest_monotonous_substring('123') == 3
    assert longest_monotonous_substring('123456789') == 9
    assert longest_monotonous_substring('987654321') == 9
    assert longest_monotonous_substring('012300000') == 6
    assert longest_monotonous_substring('21') == 2
    assert longest_monotonous_substring('321') == 3
    assert longest_monotonous_substring('0321') == 3
    assert longest_monotonous_substring('013876543') == 6

    # plateau
    assert longest_monotonous_substring('1233332221') == 8


if __name__ == "__main__":
    test_all()
