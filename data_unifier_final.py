from os import walk
from os.path import splitext
from os.path import join

import pandas as pd
from utils import slice_excel_df, excel_loc
foodir2 = r"F:\Load\test\11-09-2021.xlsx"
foodir = r"F:\Load\test\13-09-2021.xlsx"
barlist = list()


class Excel2SlicedDF:
    """
    series_cell_2D_array = [ [start_cell_1,end_cell_1] , [start_cell_2,end_cell_2] ]
    insert 'time cell' value if date_or_datetime_cell contains a date
    """
    def __init__(self, absolute_file_path, sheet_name, series_cell_range_2D_array,date_or_date_time_cell, time_cell = ''):

        raw_df = pd.read_excel(absolute_file_path, sheet_name=sheet_name, header=None, index_col=None)
        df_sliced = pd.DataFrame()
        for series_ranges in series_cell_range_2D_array:
            df_sliced_part = slice_excel_df(raw_df, series_ranges[0], series_ranges[1])
            """axis=1 (must)"""
            df_sliced = pd.concat([df_sliced, df_sliced_part],
                                  join='outer', axis=1)

        """resetting the column names"""
        df_sliced.columns = list(range(0, len(df_sliced.columns)))
        # date = slice_excel_df(raw_df, date_or_date_time_cell, date_or_date_time_cell)
        date_time = excel_loc(raw_df, date_or_date_time_cell)
        # time = slice_excel_df(raw_df, time_cell, time_cell)
        if time_cell != '':
            time = excel_loc(raw_df, time_cell)
            df_sliced['Datetime'] = date_time.replace(hour=time.hour, minute=time.minute, second=time.second)
        else:
            df_sliced['Datetime'] = date_time
        df_sliced.set_index('Datetime', inplace=True)
        df_sliced.columns = list(range(0, len(df_sliced.columns)))

        # df = pd.concat([df, df_sliced], join='outer')
        self.df_processed = df_sliced
        # df.to_excel('op.xlsx')


class DataUnifierLS:
    def __init__(self, folder_path, file_type):
        self.file_path_list = []
        df = pd.DataFrame()
        for root, dirs, files in walk(folder_path):
            try:
                for file in files:
                    file_path = join(root, file)

                    file_name = splitext(file_path)[1].lower()
                    if file_name == file_type.lower() and '~' not in file_name:
                        wb = pd.ExcelFile(file_path)
                        sheet_names = wb.sheet_names
                        for name_raw in sheet_names:
                            try:
                                name = str(name_raw).lower()
                                # if 'shed' in name or ('1' in name and 'sheet' in name):
                                if 'shed' in name:
                                    sheet_name = name_raw
                                    print(file_path)
                                    # raw_df = pd.read_excel(file_path, sheet_name=sheet_name, header=None, index_col=None)
                                    # df_sliced = slice_excel_df(raw_df, 'E16', 'L16')
                                    # df_sliced['date'] = slice_excel_df(raw_df, 'B7', 'B7')
                                    # df_sliced.set_index('date', inplace=True)
                                    df_sliced = Excel2SlicedDF(file_path, sheet_name,
                                                               [['C7', 'C7'], ['E16', 'L16']], 'B7', 'B13').df_processed
                                    df = pd.concat([df, df_sliced], join='outer', axis=0)

                                elif '1' in name and 'sheet' in name:
                                    sheet_name = name_raw
                                    print(file_path)
                                    # raw_df = pd.read_excel(file_path, sheet_name=sheet_name, header=None, index_col=None)
                                    # df_sliced = slice_excel_df(raw_df, 'F16', 'O16')
                                    # df_sliced['date'] = slice_excel_df(raw_df, 'C7', 'C7')
                                    # df_sliced.set_index('date', inplace=True)
                                    df_sliced = Excel2SlicedDF(file_path, sheet_name,
                                                               [['D7', 'D7'], ['F16', 'G16'], ['I16', 'J16'], ['L16', 'O16']],
                                                               date_or_date_time_cell='C7').df_processed

                                    df = pd.concat([df, df_sliced], join='outer')
                            except:
                                print(f'error in {file_path}')
            except:
                print(f'path error in {file_path}')

        self.df_processed = df
        # df.to_excel('op.xlsx')

class DataUnifierDOD:
    def __init__(self, folder_path, file_type):
        self.file_path_list = []
        df = pd.DataFrame()
        for root, dirs, files in walk(folder_path):
            try:
                for file in files:
                    file_path = join(root, file)

                    file_name = splitext(file_path)[1].lower()
                    if file_name == file_type.lower() and '~' not in file_name:
                        wb = pd.ExcelFile(file_path)
                        sheet_names = wb.sheet_names
                        for name_raw in sheet_names:
                            try:
                                name = str(name_raw).lower()
                                # if 'shed' in name or ('1' in name and 'sheet' in name):
                                if 'cast' in name:
                                    sheet_name = name_raw
                                    print(file_path)
                                    # raw_df = pd.read_excel(file_path, sheet_name=sheet_name, header=None, index_col=None)
                                    # df_sliced = slice_excel_df(raw_df, 'E16', 'L16')
                                    # df_sliced['date'] = slice_excel_df(raw_df, 'B7', 'B7')
                                    # df_sliced.set_index('date', inplace=True)
                                    df_sliced = Excel2SlicedDF(file_path, sheet_name,
                                                               [['F191', 'F191'], ['H207', 'H207'],
                                                                ['E125', 'E125'], ['I193', 'I193']], 'D180', 'H181').df_processed
                                    df = pd.concat([df, df_sliced], join='outer', axis=0)

                                # elif '1' in name and 'sheet' in name:
                                #     sheet_name = name_raw
                                #     print(file_path)
                                #     # raw_df = pd.read_excel(file_path, sheet_name=sheet_name, header=None, index_col=None)
                                #     # df_sliced = slice_excel_df(raw_df, 'F16', 'O16')
                                #     # df_sliced['date'] = slice_excel_df(raw_df, 'C7', 'C7')
                                #     # df_sliced.set_index('date', inplace=True)
                                #     df_sliced = Excel2SlicedDF(file_path, sheet_name,
                                #                                [['D7', 'D7'], ['F16', 'G16'], ['I16', 'J16'], ['L16', 'O16']],
                                #                                date_or_date_time_cell='C7').df_processed
                                #
                                #     df = pd.concat([df, df_sliced], join='outer')
                            except:
                                print(f'error in {file_path}')
            except:
                print(f'path error in {file_path}')

        self.df_processed = df
        # df.to_excel('op.xlsx')

# LoadShed1 = Excel2SlicedDF(foodir, 'Load Shed', [['C7', 'C7'], ['E16', 'L16']], 'B7', 'B13')
# LoadShed2 = Excel2SlicedDF(foodir2, 'Sheet1', [['F16', 'G16'], ['I16', 'J16'], ['L16', 'O16']], date_or_date_time_cell='C7')

# print(LoadShed1.df_processed)
# print(LoadShed2.df_processed)
a = 5
# folder_path_ls = r'F:\Load\test1'
# folder_path = r'F:\Load\test1'
# df = DataUnifierLS(folder_path_ls, '.xlsx').df_processed
folder_path_dod = r'F:\NOD\DOD\to_minister'
df = DataUnifierDOD(folder_path_dod, '.xlsm').df_processed

df.to_excel('res_dod.xlsm')

