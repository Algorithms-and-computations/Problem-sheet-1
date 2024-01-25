import random
from numba import jit, prange

N = 1000000000


# Compiled and parallelised
@jit(nopython=True, parallel=True)
def calculate_pi(N):
    hits = 0

    for i in prange(N):
        x = random.random()  # Between 0.0 and 1.0
        y = random.random()  # Between 0.0 and 1.0
        if x**2 + y**2 < 1:
            hits += 4

    return hits / N


# def calculate_pi(N):
#     hits = 0
#
#     for i in range(N):
#         x = random.random()  # Between 0.0 and 1.0
#         y = random.random()  # Between 0.0 and 1.0
#         if x**2 + y**2 < 1:
#             hits += 4
#
#     return hits / N


pi = calculate_pi(N)
print(pi)
