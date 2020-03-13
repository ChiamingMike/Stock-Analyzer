from urllib import request
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import configparser as config
import datetime
import openpyxl
import os
import pandas as pd
import time


class LinkCreater:
    def __init__(self):
        self.config = config.ConfigParser()
        self.config.read('setting.ini')
        self.stock_code_list = self.config.get('stock_code', 'code').split(',')
        self.period = self.config.get('stock_code', 'period')
        self.url_list = list()

    def make_link(self):
        for stock_code in self.stock_code_list:
            url = 'https://kabutan.jp/stock/kabuka?code=' + \
                stock_code + '&ashi=' + self.period + '&page=1'
            self.url_list.append(url)

        return self.stock_code_list, self.url_list


class DataParser:
    def __init__(self, stock_code, url):
        self.stock_code = stock_code
        self.url = url
        self.url_list = list()
        self.stock_name = str()

    def find_target_url_list(self):
        print(f'Collecting urls relating {self.stock_code}...')
        self.url_list.append(self.url)

        while True:
            html = request.urlopen(self.url)
            soup = BeautifulSoup(html, 'html.parser')
            pager = soup.find('li', string='次へ＞')

            if bool(pager) is False:
                self.stock_name = soup.find('h2').contents[1]
                print(f'Completed collecting urls relating {self.stock_code}')
                break

            if bool(pager) is True:
                next_page = pager.a.get('href')
                self.url = 'https://kabutan.jp/stock/kabuka' + next_page
                self.url_list.append(self.url)
                time.sleep(3)

        return self.stock_name, self.url_list

    def parse_data(self, url_list):
        data_container = list()

        for url in url_list:
            tables = pd.read_html(url)
            data_container.append(tables[5])
        data = pd.concat(data_container)

        return data


class DataHandler:
    def __init__(self, all_data, stock_name, stock_code):
        self.stock_name = stock_name
        self.stock_code = stock_code
        self.open = all_data[['始値']].values
        self.high = all_data[['高値']].values
        self.low = all_data[['安値']].values
        self.close = all_data[['終値']].values

    def calculate_data(self):
        value_ave_data = pd.DataFrame({
            'Name': [self.stock_name],
            'Code': [self.stock_code],
            'Open(ave)': [int(sum(self.open) / len(self.open))],
            'High(ave)':	[int(sum(self.high) / len(self.high))],
            'Low(ave)': [int(sum(self.low) / len(self.low))],
            'Close(ave)': [int(sum(self.close) / len(self.close))]
        })

        return value_ave_data


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
    print(datetime.datetime.now())
    l_creater = LinkCreater()
    stock_code_list, url_list = l_creater.make_link()
    value_ave_data_list = list()
    for num, url in enumerate(url_list):
        print(num, url)
        l_finder = DataParser(stock_code_list[num], url)
        stock_name, url_list = l_finder.find_target_url_list()
        all_data = l_finder.parse_data(url_list)
        d_handler = DataHandler(
            all_data, stock_name, stock_code_list[num])
        value_ave_data_df = d_handler.calculate_data()
        value_ave_data_list.append(value_ave_data_df)
        d_saver = DataSaver(
            stock_name, stock_code_list[num], all_data, value_ave_data_list)
        d_saver.output_all_data()
        d_saver.output_ave_data()
        value_ave_data_list.clear()
    print(datetime.datetime.now())
