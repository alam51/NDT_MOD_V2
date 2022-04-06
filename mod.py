import os
from calendar import monthrange
import openpyxl
import pandas as pd
import dateutil.parser as date_parser


def files_parser_from_folder(year, month, file_path):
    days_of_month = monthrange(year, month)[1]
    files = os.listdir(file_path)
    valid_file_list = []
    days = []

    for file in files:
        try:
            date = date_parser.parse(file, fuzzy=True, dayfirst=True)
            if date.year == year and date.month == month and '.xl' in file and '~' not in file:
                valid_file_list.append(file)
                days.append(date.day)
        except:
            pass

    if len(valid_file_list) == days_of_month:
        print('all files read successfully!!')
        return days_of_month, valid_file_list
    else:
        print(f'Files of the dates not found: \n{set(range(days_of_month + 1)) - set(days) - {0} }\n')
        print('Please terminate the program, insert the missing file in directory and run the '
              'program again ')


def data_parser_from_file(df_list_fn, file_path_fn, file_fn):
    date = date_parser.parse(file_fn, fuzzy=True, dayfirst=True)
    file_full_path = file_path_fn + '\\' + file_fn
    df_list_fn[date.day] = pd.read_excel(file_full_path, 'EWIC', header=None, index_col=None)


def data_parser_from_file2(file_path_fn, file_fn):
    date = date_parser.parse(file_fn[0], fuzzy=True, dayfirst=True)
    file_full_path = file_path_fn[0] + '\\' + file_fn[0]
    df = pd.read_excel(file_full_path, 'EWIC', header=None, index_col=None)
    return date.day, df


def data_parser_from_file3(file_path_fn, file_fn):
    date = date_parser.parse(file_fn[0], fuzzy=True, dayfirst=True)
    file_full_path = file_path_fn[0] + '\\' + file_fn[0]
    df = openpyxl.load_workbook(file_full_path, data_only=True)
    return date.day, df
