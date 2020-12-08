"""
2020-12-08 evening
Print all prime numbers from 1 to N
"""


def get_primes(n: int):
    half = (n + 2) // 2
    sieve = [True] * (n + 1)
    for k in range(2, half):
        if not sieve[k]:
            continue
        for f in range(k * 2, n + 1, k):
            sieve[f] = False

    for i, s in enumerate(sieve):
        if s and i > 1:
            yield i


if __name__ == "__main__":
    print(list(get_primes(1000)))
