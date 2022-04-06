import pandas as pd


class TimeGrabFromStr:
    def __init__(self, txt, file_date_time):
        """"First to separate times"""
        open_time_mid_index = txt.find(':')
        close_time_mid_index = txt.rfind(':')  # find from right
        if open_time_mid_index == close_time_mid_index:
            if 'since' in txt or 'trip' in txt:
                self.open_time_str = txt[:open_time_mid_index + 3]
                self.close_time_str = pd.NA
            else:
                self.close_time_str = txt[close_time_mid_index - 2:]
        else:
            self.open_time_str = txt[:open_time_mid_index + 3]
            self.close_time_str = txt[close_time_mid_index - 2:]

        # ***then dates***
        self.date_separators = ['/', '-']
        date_separator_index_list = []
        date_sep_index_list_final = []

        for pos, letter in enumerate(txt):
            if letter in self.date_separators:
                date_separator_index_list.append(pos)

        list_length = len(date_separator_index_list)
        if list_length > 0:
            it = iter(range(1, list_length))
            count = 1
            for i in it:
                if date_separator_index_list[i] - date_separator_index_list[i - 1] <= 4:  # max possible gap for
                    # date separator indexes of the same date = 4
                    date_sep_index_list_final += [date_separator_index_list[i - 1], date_separator_index_list[i]]
                    date_separator_index_list[i - 1] = 0  # for safety purpose
                    date_separator_index_list[i] = 0
                    i = next(it)  # jumps once here, next in for to make two jumps
                    # i = next(it)
        #             date_sep_index_list_final found
        #             now time to decide what times and dates are they actually

        if len(date_sep_index_list_final) == 2:  # only one date is found
            try:
                self.close_date_str = txt[
                                      date_separator_index_list[0] - 2:date_separator_index_list[
                                                                           1] + 4 + 1]  # dd/mm/yyyy
            except IndexError:
                self.close_date_str = txt[date_separator_index_list[0] - 2:date_separator_index_list[1] + 2 + 1]  #
                # dd/mm/yy
            self.open_date_str = self.close_date_str

        elif len(date_sep_index_list_final) == 4:
            try:
                self.open_date_str = txt[
                                     date_separator_index_list[0] - 2:date_separator_index_list[
                                                                          1] + 4 + 1]  # dd/mm/yyyy
            except IndexError:
                self.open_date_str = txt[date_separator_index_list[0] - 2:date_separator_index_list[1] + 2 + 1]  #
                # dd/mm/yy
            try:
                self.close_date_str = txt[
                                      date_separator_index_list[2] - 2:date_separator_index_list[
                                                                           3] + 4 + 1]  # dd/mm/yyyy
            except IndexError:
                self.close_date_str = txt[date_separator_index_list[2] - 2:date_separator_index_list[3] + 2 + 1]  #
                # dd/mm/yy

        if len(date_sep_index_list_final) == 0:  # if no date mentioned take the file date
            self.open_date_str = str(file_date_time.replace(day=file_date_time.day - 1).date())  # original date is 1
            # day old
            self.close_date_str = str(file_date_time.replace(day=file_date_time.day - 1).date())

    text = 'm) Siddhirganj 210 MW Gt2 was shut down at 01:07(06/05/2021) due to gas shortage and was   synchronized at ' \
           '08:28(06-05-2021). '
    a = 5
    b = 8
