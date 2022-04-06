import multiprocessing
from multiprocessing import Pool
import time
from functools import partial
# start = time.perf_counter()

# def f(x, start):
#     # time.sleep(0.1)
#     print(f'{x}^{x} = {x ** x}\n  Time elapsed = {time.perf_counter() - start} \n')


def f1(x, y, start):
    # time.sleep(0.1)
    print(f'{x}^{y} = {x ** y}\n  Time elapsed = {time.perf_counter() - start} \n')


if __name__ == '__main__':
    strt = time.perf_counter()
    # start 4 worker processes
    cpu_nos = multiprocessing.cpu_count()
    params = []
    for i in range(10000+1):
        params.append([i, i, strt])
    with Pool(processes=cpu_nos) as pool:
        # pool.starmap(f, [(1, strt), (2, strt)])
        # pool.map(partial(f1, start=strt), params)
        pool.starmap(f1, params)
    print(f'finished in {time.perf_counter()-strt} seconds')
    print(f'Number of cores: {multiprocessing.cpu_count()}')

