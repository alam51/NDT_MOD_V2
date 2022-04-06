from os import walk
from os.path import splitext
from os.path import join

import pandas as pd
from utils import slice_excel_df, excel_loc
foodir = r"F:\Load\test\13-09-2021.xlsx"
barlist = list()


class Excel2DataFrame:
    """insert 'time cell' value if date_or_datetime_cell contains a date"""
    def __init__(self, absolute_file_path, sheet_name, series_start_cell, series_end_cell,date_or_date_time_cell, time_cell = ' '):
        raw_df = pd.read_excel(absolute_file_path, sheet_name=sheet_name, header=None, index_col=None)
        df_sliced = slice_excel_df(raw_df, series_start_cell, series_end_cell)

        # date = slice_excel_df(raw_df, date_or_date_time_cell, date_or_date_time_cell)
        date_time = excel_loc(raw_df, date_or_date_time_cell)
        # time = slice_excel_df(raw_df, time_cell, time_cell)
        time = excel_loc(raw_df, time_cell)
        df_sliced['Datetime'] = date_time.replace(hour=time.hour, minute=time.minute, second=time.second)
        df_sliced.set_index('Datetime', inplace=True)

        # df = pd.concat([df, df_sliced], join='outer')
        self.df_processed = df_sliced
        # df.to_excel('op.xlsx')


LoadShed1 = Excel2DataFrame(foodir, 'Load Shed', 'E16', 'K16', 'B7', 'B13')
print(LoadShed1.df_processed)
a = 5
