import configparser
import os
import pandas
import time

from bs4 import BeautifulSoup
from urllib import request


class UrlContainer(object):

    __instance = None
    __is_intialized = False

    def __new__(cls):
        """
        """
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)

        return cls.__instance

    def __init__(self) -> None:
        """
        """
        if self.__is_intialized is True:
            return None

        self.__is_intialized = True

        self.period = str()
        self.stock_codes = list()
        self.url_table = dict()
        self.conversion_table = dict()

        try:
            root = os.path.join(os.path.dirname(os.path.dirname(
                __file__)), 'conf', 'setting.ini')
            config = configparser.ConfigParser()
            config.read(root)
            section = 'stock_code'
            stock_codes = config.get(section, 'code').split(',')
            self.period = config.get(section, 'period')
        except Exception as e:
            print(e)
            pass  # error_msg
            return None

        self.stock_codes = list(set(stock_codes))
        self.create_url()

        return None

    def initialize_all_data(self) -> None:
        """
        """
        self.period = str()
        self.stock_codes = list()
        self.url_table = dict()
        self.conversion_table = dict()

        return None

    def create_url(self) -> None:
        """
        """
        OFFSET = 1
        for stock_code in self.stock_codes:
            url = f'https://kabutan.jp/stock/kabuka?code={stock_code}&ashi={self.period}&page={OFFSET}'
            self.url_table[stock_code] = [url]

        return None

    def accumulate_url(self) -> None:
        """
        """
        for stock_code in self.url_table.keys():

            while True:
                html = request.urlopen(self.url_table[stock_code][-1])
                soup = BeautifulSoup(html, 'html.parser')
                is_exist_pager = soup.find('li', string='次へ＞')
                if not bool(is_exist_pager):
                    stock_name = soup.find('h2').contents[1]
                    self.conversion_table[stock_code] = stock_name
                    print(
                        f'Completed collecting urls relating {stock_code} ( {stock_name} )')
                    break  # log_msg

                elif bool(is_exist_pager):
                    next_page = is_exist_pager.a.get('href')
                    next_url = f'https://kabutan.jp/stock/kabuka{next_page}'
                    self.url_table[stock_code].append(next_url)
                    # time.sleep(3)

        return None

    def get_stock_list(self) -> list:
        """
        """
        if self.stock_codes == list():
            print('failed to get stock_codes')  # error_msg

        return self.stock_codes

    def get_conversion_table(self, stock_code: str) -> str:
        """
        """
        return self.conversion_table.get(stock_code, str())

    def get_url_table(self) -> dict:
        """
        """
        return self.url_table


if __name__ == '__main__':
    pass
