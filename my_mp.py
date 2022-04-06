import multiprocessing
import time



def do_something(a, b):
    print('Sleeping .1 second\n')
    time.sleep(1)
    # print(f'{time.perf_counter()- strt} seconds passed.  Sum = {a+b}\n')


if __name__ == '__main__':
    print(2)
    print(f'Number of CPU = {multiprocessing.cpu_count()}')
    strt = time.perf_counter()

    p1 = multiprocessing.Process(target=do_something, args=(0, 1))
    p2 = multiprocessing.Process(target=do_something, args=(0, 2))
    #
    p1.start()
    p2.start()
    #
    p1.join()
    p2.join()
    #
    finish = time.perf_counter()
    print(f'Finished in {round(finish - strt, 5)} seconds\n')
