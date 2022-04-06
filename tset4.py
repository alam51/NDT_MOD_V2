import os

folder_dir = r'G:\My Drive\Monthly_Report\2021\October\DOD\October2021'
file_absolute_path_list = [os.path.join(folder_dir, file)
                           for file in os.listdir(folder_dir)
                           if file.endswith('.xlsm') and '~' not in file]
print(file_absolute_path_list)
