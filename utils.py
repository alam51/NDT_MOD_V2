import mysql.connector

import os
import re
from calendar import monthrange

import pandas as pd
from openpyxl.utils.cell import coordinate_from_string, column_index_from_string
from dateutil.parser import parse as date_parse


CONNECTOR = mysql.connector.connect(user='root', password='pgcb1234',
                                    host='127.0.0.1',
                                    database='ois')


def slice_excel_df(df, from_, to):
    """excel file must be read by pd.read_excel(file, index-col=None, header=none)"""
    # xy = coordinate_from_string('A4')
    col_from, row_from = coordinate_from_string(from_)
    col_from = column_index_from_string(col_from)
    col_to, row_to = coordinate_from_string(to)
    col_to = column_index_from_string(col_to)
    i = col_to
    row_from, col_from, row_to, col_to = [(i - 1) for i in [row_from, col_from, row_to, col_to]]
    """"you can not use 'iloc' as it may curtail data like a = range(1,2) = [1] """
    """"This does not happen in case of 'loc'"""
    df1 = df.loc[row_from:row_to, col_from:col_to]
    return df1.reset_index(drop=True)


def excel_loc(df, xl_loc):
    """excel file must be read by pd.read_excel(file, index-col=None, header=none)"""
    col, row = coordinate_from_string(xl_loc)
    col = column_index_from_string(col)
    """"you can not use 'iloc' as it may curtail data like a = range(1,2) = [1] """
    """"This does not happen in case of 'loc'"""
    return df.loc[row - 1, col - 1]


def files_parser_from_folder(year, month, file_path):
    """excel file must be read by pd.read_excel(file, index-col=None, header=none)"""
    days_of_month = monthrange(year, month)[1]
    files = os.listdir(file_path)
    valid_file_list = []
    days = []

    for file in files:
        try:
            date = date_parse(file, fuzzy=True, dayfirst=True, yearfirst=False)
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


def time_grab_from_str(txt):
    # txt = str(txt).lower()
    date_separators = ['/', '-']
    date_separator_index_list = []
    date_sep_index_list_final = []

    for pos, letter in enumerate(txt):
        if letter in date_separators:
            date_separator_index_list.append(pos)

    list_length = len(date_separator_index_list)
    if list_length > 0:
        it = iter(range(1, list_length))
        count = 1
        for i in it:
            if date_separator_index_list[i] - date_separator_index_list[i - 1] <= 4:  # max possible gap from date seps
                # = 4
                date_sep_index_list_final += [date_separator_index_list[i - 1], date_separator_index_list[i]]
                date_separator_index_list[i - 1] = 0  # for safety purpose
                date_separator_index_list[i] = 0
                i = next(it)  # jumps once here, next in for to make two jumps
                # i = next(it)
    if len(date_sep_index_list_final) == 2:
        close_date_str = txt[date_separator_index_list[0] - 2:date_separator_index_list[1]]


text = 'm) Siddhirganj 210 MW Gt2 was shut down at 01:07(06/05/2021) due to gas shortage and was   synchronized at ' \
       '08:28(06-05-2021). '
a = 5
# b = time_grab_from_str(text)
# c = 4
