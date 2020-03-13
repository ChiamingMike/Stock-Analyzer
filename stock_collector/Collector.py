import pandas as pd
import time

from bs4 import BeautifulSoup
import configparser as config
from urllib import request


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


if __name__ == '__main__':
    pass
