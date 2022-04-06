import multiprocessing as mp
from functools import partial

import numpy as np
import openpyxl

import mod
import pandas as pd

if __name__ == '__main__':
    path = r'F:\IMD\MOD\March 2021_Final\March 2021_Final\March2021'
    days_of_month, files = mod.files_parser_from_folder(2021, 3, path)

    full_path_list = []
    for file in files:
        full_path_list.append([[path], [file]])

    # full_path_list = np.transpose(full_path_list)
    b = full_path_list

    print(full_path_list)
    a = full_path_list[0]
    cpu_nos = mp.cpu_count()
    with mp.Pool(processes=cpu_nos) as pool:
        # op_list = pool.map(partial(mod.data_parser_from_file2, file_path_fn=path), files)
        op_list = pool.starmap(mod.data_parser_from_file3, full_path_list)
        # p1 = mp.Process(target=mod.data_parser_from_file3, args=a)
    # print(op_list)

    wb_list = []
    for i in range(days_of_month + 1):
        wb = openpyxl.Workbook()
        wb_list.append(wb)

    for i in op_list:
        wb_list[i[0]] = i[1]

    for i in range(1, days_of_month+1):
        val = wb_list[i]['Forecast']['E3'].value
        print(f'Date: {val} \n')


