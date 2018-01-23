"""
    2013-04-01 Decode Ways
    http://craftsmanship.sv.cmu.edu/katas/decode-ways

    >>> ways('1')
    1
    >>> ways('9')
    1
    >>> ways('12')
    2
    >>> ways('121')
    3
    >>> ways('128')
    2
    >>> ways('102')
    1
    >>> ways('20')
    1
    >>> ways('201')
    1
    >>> ways('210')
    1
    >>> ways('2101')
    1
    >>> ways('281')
    1
    >>> ways('181')
    2
    >>> ways('101010')
    1
    >>> ways('261')
    2
    >>> ways('271')
    1
"""


def ways(s):

    # represents all the combinations of last characters in valid decodings,
    # the length of fringe is the number of ways the sequence can be decoded.
    # None means that the next character should be the first digit of a new number, i.e. not "0"
    fringe = [None]

    for c in s:
        new_fringe = []
        for f in fringe:

            if c != '0':
                if c in ['1', '2']:
                    new_fringe.append(c)
                else:
                    new_fringe.append(None)

            if f is not None:
                if f == '1':
                    # ends two-digit number "1c"
                    new_fringe.append(None)
                elif f == '2':
                    if c not in ['7', '8', '9']:
                        # ends two-digit number '2c'
                        new_fringe.append(None)
                    else:
                        # 27, 28, 29 are invalid
                        pass

        fringe = new_fringe

    return len(fringe)



