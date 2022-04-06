from os import walk
from os.path import splitext
from os.path import join

import pandas as pd
from utils import slice_excel_df
foodir = r"F:\Load\load_shed"
barlist = list()


class LoadShed:
    def __init__(self, folder_path, file_type):
        self.file_path_list = []
        df = pd.DataFrame()
        for root, dirs, files in walk(folder_path):
          for file in files:
                file_path = join(root, file)

                file_name = splitext(file_path)[1].lower()
                if file_name == file_type.lower() and '~' not in file_name:
                    wb = pd.ExcelFile(file_path)
                    sheet_names = wb.sheet_names
                    for name_raw in sheet_names:
                        name = str(name_raw).lower()
                        # if 'shed' in name or ('1' in name and 'sheet' in name):
                        if 'shed' in name:
                            sheet_name = name_raw
                            print(file_path)
                            raw_df = pd.read_excel(file_path, sheet_name=sheet_name, header=None, index_col=None)
                            df_sliced = slice_excel_df(raw_df, 'E16', 'L16')
                            df_sliced['date'] = slice_excel_df(raw_df, 'B7', 'B7')
                            df_sliced.set_index('date', inplace=True)
                            df = pd.concat([df, df_sliced], join='outer')

                        elif  '1' in name and 'sheet' in name:
                            sheet_name = name_raw
                            print(file_path)
                            raw_df = pd.read_excel(file_path, sheet_name=sheet_name, header=None, index_col=None)
                            df_sliced = slice_excel_df(raw_df, 'F16', 'O16')
                            df_sliced['date'] = slice_excel_df(raw_df, 'C7', 'C7')
                            df_sliced.set_index('date', inplace=True)
                            df = pd.concat([df, df_sliced], join='outer')


        self.df_processed = df
        df.to_excel('op.xlsx')


LoadShed1 = LoadShed(foodir, '.xlsx')
a = 5
