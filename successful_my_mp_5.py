import multiprocessing as mp
from multiprocessing import Pool
import time
from functools import partial


def f(list_x, y, z, a):
    # time.sleep(0.1)
    print(f'sum of list = {sum(list_x)}\n  y^z = {y ** z} char = {a}\n')
    return a, z


if __name__ == '__main__':
    # strt = time.perf_counter()
    # start 4 worker processes
    cpu_nos = mp.cpu_count()
    val = [[[1, 2], 2, 2, 'a'], [[3, 4], 5, 5, 'b'], [[5, 4], 2, 5, 'c']]
    with Pool(processes=mp.cpu_count()) as pool:
        # pool.starmap(f, [(1, strt), (2, strt)])
        a = pool.starmap(f, val)
    # print(f'finished in {time.perf_counter()-strt} seconds')
    print(a)
