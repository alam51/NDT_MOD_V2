import datetime
import traceback

import pandas as pd
from dateutil.parser import parse as DateParse
from openpyxl.utils.cell import coordinate_from_string, column_index_from_string
import utils


class EwicDoD:
    def __init__(self, path, xl_file_name):
        self.path = path
        self.date = DateParse(xl_file_name + '00:00', dayfirst=True, yearfirst=False, fuzzy=True)
        # self.t = pd.date_range(start=self.date, periods=24, freq='1H')
        n_cols = 14
        cols = []
        for col in range(n_cols):
            cols.append(col)
        self.df = pd.read_excel(path + '\\' + xl_file_name, sheet_name='EWIC', header=None, index_col=None,
                                usecols=cols,
                                skiprows=None, nrows=32)
        self.times = utils.slice_excel_df(self.df, 'A6', 'A31')
        for pos, time in enumerate(self.times.iloc[:, 0]):
            try:
                self.times.iloc[pos, 0] = DateParse(xl_file_name + str(time), dayfirst=True, yearfirst=False,
                                                    fuzzy=True)
            except:
                if '24' in str(time):
                    self.times.iloc[pos, 0] = self.date + datetime.timedelta(days=1)
                else:
                    print(f'could not parse time on {time} of {self.date.date()} ')
                continue
        self.times.columns = ['Time']
        self.ghora_amps = utils.slice_excel_df(self.df, 'B6', 'B31')
        self.ghora_amps.columns = ['Ghora_Amps']
        self.ish_mw = utils.slice_excel_df(self.df, 'C6', 'C31')
        self.ish_mw.columns = ['Ish_MW']
        self.ashu_mw = utils.slice_excel_df(self.df, 'E6', 'E31')
        self.ashu_mw.columns = ['Ashu_MW']
        self.siraj_mw = utils.slice_excel_df(self.df, 'G6', 'G31')
        self.siraj_mw.columns = ['Siraj_MW']
        self.ghora_meter_diff = None
        self.ish_meter_diff = None
        self.ashu_meter_diff = None
        self.siraj_meter_diff = None
        try:
            self.ghora_meter_diff = float(utils.excel_loc(self.df, 'N8')) + float(utils.excel_loc(self.df, 'N10'))
        except:
            print(f'Error occured on reading ghora_meter_diff on {self.date}')
        try:
            self.ish_meter_diff = float(utils.excel_loc(self.df, 'N14')) + float(utils.excel_loc(self.df, 'N16'))
        except:
            print(f'Error occured on reading ish_meter_diff on {self.date}')
        try:
            self.ashu_meter_diff = float(utils.excel_loc(self.df, 'N20')) + float(utils.excel_loc(self.df, 'N22'))
        except:
            print(f'Error occured on reading ashu_meter_diff on {self.date}')
        try:
            self.siraj_meter_diff = float(utils.excel_loc(self.df, 'N26')) + float(utils.excel_loc(self.df, 'N28'))
        except:
            print(f'Error occured on reading siraj_meter_diff on {self.date}')
        meter_diff_dict = {
            'Ghora_Exp': [self.ghora_meter_diff],
            'Ish_Imp': [self.ish_meter_diff],
            'Ashu_Exp': [self.ashu_meter_diff],
            'Siraj_Imp': [self.siraj_meter_diff]
        }
        self.meter_diff_df = pd.DataFrame(data=meter_diff_dict, index=[self.date])
        for pos, val in enumerate(self.ghora_amps.iloc[:, 0]):
            try:
                if self.ish_mw.iloc[pos, 0] > 0:
                    self.ghora_amps.iloc[pos, 0] *= -1
                    # ind.append(pos)
            # self.mw_dict = {'Ghora_A': self.ghor
            except Exception as e:
                print(f'Error in {self.date}')
                print(f'Message:\n{traceback.print_exc()}')

        self.mw_df = pd.concat([self.times, self.ghora_amps, self.ish_mw, self.ashu_mw, self.siraj_mw], axis=1)
        self.mw_df.set_index('Time', inplace=True)

# Ewic_1 = EwicDoD(f'F:\IMD\MOD\April\ZT', '06-04-2021 Zone Total.xlsx')
# # print(Ewic_1.df.to_string())
# print(Ewic_1.mw_df.to_string())
# print(Ewic_1.ashu_meter_diff)
# print(Ewic_1.siraj_meter_diff)
