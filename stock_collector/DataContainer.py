import openpyxl
import os
import pandas as pd


class DataSaver:
    def __init__(self, stock_name, stock_code, all_data, value_ave_data_list):
        self.stock_name = stock_name
        self.stock_code = stock_code
        self.all_data = all_data
        self.value_ave_data_list = value_ave_data_list
        self.current_directory = os.getcwd()

    def output_all_data(self):
        file_name = 'stock_detail.xlsx'
        sheet_nm = f'{self.stock_name}_{self.stock_code}'

        if file_name in os.listdir(self.current_directory):
            # 既存ファイルに追記
            with pd.ExcelWriter(file_name, mode='a') as writer:
                writer.book = openpyxl.load_workbook(file_name)
                self.all_data.to_excel(writer, sheet_name=sheet_nm,
                                       header=True, index=False, encoding='cp932')
        else:
            # 新規ファイルを作成
            self.all_data.to_excel(file_name, sheet_name=sheet_nm,
                                   header=True, index=False, encoding='cp932')

    def output_ave_data(self):
        file_name = 'stock_info.xlsx'
        value_ave_data = pd.concat(self.value_ave_data_list)
        if file_name in os.listdir(self.current_directory):
            # 既存ファイルに追記
            wb = openpyxl.load_workbook(file_name)
            sheet = wb.worksheets[0]
            val = value_ave_data.values.tolist()

            row_length = len(val)
            for i in range(0, row_length):
                sheet.append(val[i])

            wb.save(file_name)

        else:
            # 新規ファイルを作成
            value_ave_data.to_excel(file_name, sheet_name='stock_info',
                                    header=True, index=False, encoding='cp932')
            # self.value_ave_data_list.clear()


if __name__ == '__main__':
    pass
