import datetime
import pandas as pd
from dateutil.parser import parse as DateParse
from openpyxl.utils.cell import coordinate_from_string, column_index_from_string
import utils


class Outage:
    def __init__(self, path, xl_file_name):
        self.path = path
        self.date = DateParse(xl_file_name + '00:00', dayfirst=True, yearfirst=False, fuzzy=True)
        # self.t = pd.date_range(start=self.date, periods=24, freq='1H')
        n_cols = 30  # number of columns to read form 1st column
        cols = []
        for col in range(n_cols):
            cols.append(col)
        self.df = pd.read_excel(path + '\\' + xl_file_name, sheet_name='P1', header=None, index_col=None,
                                usecols=cols,
                                skiprows=55,  # number of rows to skip from the beginning
                                nrows=None)  # read up to last row
        # self.serials = utils.slice_excel_df(self.df, 'A57', 'H30')
        self.serials = []
        self.outage_txt = []
        self.open_times = []
        self.close_times = []

        """Find Serials"""
        start_col = 0
        for pos, i in enumerate(self.df.iloc[:, start_col]):
            if ')' in str(i):
                self.serials.append(i[:i.find(')')])  # if i== 'aa)' , serial.append('aa')
                txt = i
                if ')' not in str(self.df.iloc[pos + 1, start_col]):
                    txt += str(self.df.iloc[pos + 1, start_col])
                    if ')' not in str(self.df.iloc[pos + 2, start_col]):
                        txt += str(self.df.iloc[pos + 2, start_col])
                self.outage_txt.append(txt)

        """Find Outage close & open times, texts"""
        for pos, text in enumerate(self.outage_txt):
            open_time_mid_index = text.find(':')
            close_time_mid_index = text.rfind(':')  # find from right
            dt = str(self.date)
            try:
                close_time_str = dt[dt.find(' ')] + text[close_time_mid_index - 2:close_time_mid_index + 2]
                open_time_str = dt[dt.find(' ')] + text[open_time_mid_index - 2:open_time_mid_index + 2]
                if close_time_str != open_time_str:
                    self.close_times.append(DateParse(close_time_str, dayfirst=True, yearfirst=False, fuzzy=True))
                    self.open_times.append(DateParse(open_time_str, dayfirst=True, yearfirst=False, fuzzy=True))

                # When only one time is found
                elif 'since' in text:
                    self.open_times.append(DateParse(open_time_str, dayfirst=True, yearfirst=False, fuzzy=True))
                    self.close_times.append(pd.NA)
                else:
                    self.close_times.append(DateParse(close_time_str, dayfirst=True, yearfirst=False, fuzzy=True))
                    self.open_times.append(pd.NA)
            except ValueError:
                print(f'could not process outage text for the text "{text}"\ndate: {self.date}')
                self.close_times.append(pd.NA)
                self.open_times.append(pd.NA)

        self.outage_df = pd.DataFrame({
            'Serial': self.serials,
            'Open Time': self.open_times,
            'Close Time': self.close_times,
            'Text': self.outage_txt
        })
        #
        #         self.outage_txt.append(txt)
        #
        # for pos, time in enumerate(self.times.iloc[:, 0]):
        #     try:
        #         self.times.iloc[pos, 0] = DateParse(xl_file_name + str(time), dayfirst=True, yearfirst=False,
        #                                             fuzzy=True)
        #     except:
        #         if '24' in str(time):
        #             self.times.iloc[pos, 0] = self.date + datetime.timedelta(days=1)
        #         else:
        #             print(f'could not parse time on {time} of {self.date.date()} ')
        #             continue
        # self.times.columns = ['Time']
        # self.ghora_amps = utils.slice_excel_df(self.df, 'I5', 'I30')
        # self.ghora_amps.columns = ['Ghora_Amps']
        # self.ish_mw = utils.slice_excel_df(self.df, 'J5', 'J30')
        # self.ish_mw.columns = ['Ish_MW']
        # self.ashu_mw = utils.slice_excel_df(self.df, 'L5', 'L30')
        # self.ashu_mw.columns = ['Ashu_MW']
        # self.siraj_mw = utils.slice_excel_df(self.df, 'N5', 'N30')
        # self.siraj_mw.columns = ['Siraj_MW']
        # self.ghora_meter_diff = None
        # self.ish_meter_diff = None
        # self.ashu_meter_diff = None
        # self.siraj_meter_diff = None
        # try:
        #     self.ghora_meter_diff = float(utils.excel_loc(self.df, 'U7')) + float(utils.excel_loc(self.df, 'U9'))
        # except:
        #     print(f'Error occured on reading ghora_meter_diff on {self.date}')
        # try:
        #     self.ish_meter_diff = float(utils.excel_loc(self.df, 'U13')) + float(utils.excel_loc(self.df, 'U15'))
        # except:
        #     print(f'Error occured on reading ish_meter_diff on {self.date}')
        # try:
        #     self.ashu_meter_diff = float(utils.excel_loc(self.df, 'U19')) + float(utils.excel_loc(self.df, 'U21'))
        # except:
        #     print(f'Error occured on reading ashu_meter_diff on {self.date}')
        # try:
        #     self.siraj_meter_diff = float(utils.excel_loc(self.df, 'N25')) + float(utils.excel_loc(self.df, 'N27'))
        # except:
        #     print(f'Error occured on reading siraj_meter_diff on {self.date}')
        # meter_diff_dict = {
        #     'Ghora_Exp': [self.ghora_meter_diff],
        #     'Ish_Imp': [self.ish_meter_diff],
        #     'Ashu_Exp': [self.ashu_meter_diff],
        #     'Siraj_Imp': [self.siraj_meter_diff]
        # }
        # self.meter_diff_df = pd.DataFrame(data=meter_diff_dict, index=[self.date])
        # for pos, val in enumerate(self.ghora_amps.iloc[:, 0]):
        #     if self.ish_mw.iloc[pos, 0] > 0:
        #         self.ghora_amps.iloc[pos, 0] *= -1
        #         # ind.append(pos)
        # # self.mw_dict = {'Ghora_A': self.ghor
        #
        # self.mw_df = pd.concat([self.times, self.ghora_amps, self.ish_mw, self.ashu_mw, self.siraj_mw], axis=1)
        # self.mw_df.set_index('Time', inplace=True)
