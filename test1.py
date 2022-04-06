import pandas as pd
import utils
path = r"F:\Load\load_shed\2020\April-2020\20-04-2020.xlsx"
df1 = pd.read_excel(path, index_col=None, header=None)
df_sliced1 = utils.slice_excel_df(df1, 'E16', 'L16')
df_sliced1['date'] = utils.slice_excel_df(df1, 'B7', 'B7')
df_sliced1.set_index('date', inplace=True)
# print(pd.concat([df_sliced1, df_sliced2], join='outer'))
# print(df_sliced1)
print(pd.ExcelFile(path).sheet_names)

