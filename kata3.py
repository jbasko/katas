"""
    2013-03-27
    prime numbers from 1 to N
"""

N = 1000
numbers = [True] * (N + 1)

for i in range(2, N + 1):
    if numbers[i]:
        x = 2
        while i * x <= N:
            numbers[i * x] = False
            x += 1

print [i for i in range(len(numbers)) if i > 0 and numbers[i]]


