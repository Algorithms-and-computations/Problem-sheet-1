import random

N = 10000000


def calculate_pi(N):
    hits = 0

    for i in range(N):
        x = random.random()  # Between 0.0 and 1.0
        y = random.random()  # Between 0.0 and 1.0
        if x**2 + y**2 < 1:
            hits += 4

    return hits / N


pi = calculate_pi(N)
print(pi)
