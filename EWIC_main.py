import multiprocessing as mp
import time
from pandas import ExcelWriter
import EWIC
import pandas as pd
import EWIC_2
import utils

if __name__ == '__main__':
    t1 = time.perf_counter()
    # path = r'G:\My Drive\Monthly_Report\2022\2.February\ZT'
    path = r'H:\My Drive\Monthly_Report\2022\7.July\DOD\July2022'
    days_of_month, files = utils.files_parser_from_folder(2022, 7, path)

    full_path_list = []
    for file in files:
        full_path_list.append([path, file])

    cpu_nos = mp.cpu_count()
    with mp.Pool(processes=cpu_nos) as pool:
        # op_list = pool.map(partial(mod.data_parser_from_file2, file_path_fn=path), files)
        # op_list = pool.starmap(mod.data_parser_from_file2, full_path_list)
        ewic_objects = pool.starmap(EWIC_2.EwicDoD, full_path_list)  # whether from DOD or ZT

    mw_df_list = []
    meter_diff_df_list = []
    for count, ewic_obj in enumerate(ewic_objects):
        mw_df_list.append(ewic_obj.mw_df)
        meter_diff_df_list.append(ewic_obj.meter_diff_df)

    mw_df = pd.concat(mw_df_list, axis=0)  # concat by rows
    meter_diff_df = pd.concat(meter_diff_df_list, axis=0)  # concat by rows
    for col in mw_df.columns:
        mw_df[col] = pd.to_numeric(mw_df[col], errors='coerce')
    for col in meter_diff_df.columns:
        meter_diff_df[col] = pd.to_numeric(meter_diff_df[col], errors='coerce')

    # mw_df.loc['Max Export'] = mw_df.max(axis=0)
    max_exp = mw_df.max(axis=0)
    max_exp_date = mw_df.idxmax(axis=0)

    max_imp = mw_df.min(axis=0)  # max import min max -ve export
    max_imp_date = mw_df.idxmin(axis=0)

    mw_df.loc['Max Export'] = max_exp
    mw_df.loc['Max Export Date'] = max_exp_date

    mw_df.loc['Max Import'] = max_imp
    mw_df.loc['Max Import Date'] = max_imp_date

    max_meter_diff = meter_diff_df.max(axis=0)
    max_meter_diff_date = meter_diff_df.idxmax(axis=0)

    min_meter_diff = meter_diff_df.min(axis=0)
    min_meter_diff_date = meter_diff_df.idxmin(axis=0)

    meter_diff_df.loc['Max'] = max_meter_diff
    meter_diff_df.loc['Max Date'] = max_meter_diff_date

    meter_diff_df.loc['Min'] = min_meter_diff
    meter_diff_df.loc['Min Date'] = min_meter_diff_date
    with ExcelWriter(path + '\\' + 'EWIC Readings Summary.xlsx') as writer:
        mw_df.to_excel(writer, sheet_name='MW')
        meter_diff_df.to_excel(writer, sheet_name='Energy Meter Diff')
    print(f'Number of cores of CPU Available = {mp.cpu_count()}')
    print(f'Number of cores of CPU Used = {cpu_nos}')
    print(f'Time elapsed: {time.perf_counter()}s')
    print(f'Saved at {path}\\EWIC Readings Summary.xlsx')
