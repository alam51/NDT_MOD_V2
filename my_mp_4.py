import time
from functools import partial
strt = time.perf_counter()


def f(x, start):
    # time.sleep(0.1)
    print(f' {x}^{x} = {x ** x}\n  Time elapsed = {time.perf_counter() - start}s\n')


for i in range(10000):
    f(i, strt)

print(f'total time elapsed = {time.perf_counter() - strt}s\n')
