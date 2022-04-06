import multiprocessing


def my_index(x, y, z):
    for i in y:
        x[i] = z[i]


if __name__ == '__main__':
    x = [0, 0, 0]
    y = [0, 1, 2]
    z = [0, 11, 22]
    cpu_nos = multiprocessing.cpu_count()
    with multiprocessing.Pool(processes=2) as pool:
        # pool.starmap(f, [(1, strt), (2, strt)])
        pool.starmap(my_index, [[[1, 2], 1], [[3, 4], 5]])
    # print(f'finished in {time.perf_counter()-strt} seconds')
