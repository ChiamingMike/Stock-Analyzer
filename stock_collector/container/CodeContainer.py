'''
Created on 2020/03/19

@author: ChiamingMike
'''

import configparser
import datetime
import os
import re
import pandas

from bs4 import BeautifulSoup
from urllib import request

from constant.Definition import UrlsDefinition
from logger.Log import log


class CodeContainer(object):

    def __init__(self, file_name: str) -> None:
        """
        """
        try:
            root = os.path.join(os.path.dirname(
                os.path.dirname(__file__)), 'conf', 'Setting.ini')
            config = configparser.ConfigParser()
            config.read(root)
            section = 'DEFAULT'
            stock_codes = re.sub(
                r'\s+', '', config.get(section, 'code')).split(',')
            self.stock_codes = sorted(list(set(stock_codes)))
        except Exception as e:
            log.w(e)
            log.w('Failed to get the information from setting.ini .')
            log.w('')
            return None

        execution_date = datetime.datetime.now().strftime('%Y%m')
        self.file_name = f'{execution_date}_{file_name}'
        self.file_path = os.path.join(os.path.dirname(
            os.path.dirname(__file__)), 'asset', self.file_name)

        return None

    def register_stock_codes(self, stock_codes) -> None:
        pass

    def register_conversion_table(self) -> None:
        pass

    def download_conversion_table(self) -> None:
        pass

    def get_stock_codes(self) -> list:
        """
        """
        if self.stock_codes == list():
            log.e('Failed to get a list of sotck codes.')
            log.e('Stock code doesn\'t exist.')
            log.e('')
            return list()

        return self.stock_codes

    def get_conversion_table(self) -> pandas.Series:
        """
        """
        if self.conversion_table.empty:
            log.e('Failed to get conversion table.')
            log.e('')
            return pandas.Series()

        return self.conversion_table

    def convert_into_name(self, stock_code: str) -> str:
        """
        """
        try:
            stock_name = self.conversion_table[stock_code]
        except Exception as e:
            log.e(e)
            log.e('Failed to convert code into name.')
            log.e('')
            return str()

        return stock_name


class JPCodeContainer(CodeContainer):

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

        self.stock_codes = list()
        file_name = 'JP_stock_list.xls'
        super().__init__(file_name)

        self.conversion_table = pandas.Series()

        if not os.path.isfile(self.file_path):
            self.download_conversion_table()

        self.register_conversion_table()

        return None

    def register_stock_codes(self, codes_list) -> None:
        """
        """
        pattern = re.compile(r'^(\d{4})$')
        codes = [code for code in self.stock_codes if pattern.match(code)]
        stock_codes = [code for code in codes if code in codes_list]
        if stock_codes == list():
            log.e('Failed to create URL.')
            log.e('Valid Stock code doesn\'t exist.')
            log.e('')
            return None
        else:
            self.stock_codes = stock_codes
            stock_codes = ', '.join(stock_codes)
            log.i(f'Found {len(self.stock_codes)} valid codes.')
            log.i(f'STOCK CODE: {stock_codes}')
            log.i('')

            return None

        return None

    def register_conversion_table(self) -> None:
        """
        """
        if not os.path.isfile(self.file_path)\
                or os.path.getsize(self.file_path) == 0:
            log.w(f'Failed to read {self.file_name}.')
            log.w('')
            return None

        df = pandas.read_excel(self.file_path,
                               usecols=['Local Code', 'Name (English)'],
                               dtype=str)
        df.rename(columns={'Local Code': 'code', 'Name (English)': 'name'},
                  inplace=True)
        df.set_index('code', inplace=True)
        self.register_stock_codes(list(df.index))
        self.conversion_table = df.loc[self.stock_codes, 'name']

        return None

    def download_conversion_table(self) -> None:
        """
        """
        hp = UrlsDefinition.jpx.get('hp', str())
        url = UrlsDefinition.jpx.get('url', str())
        if str() in [hp, url]:
            log.w('Cannot find a URL to download list of TSE-listed Issues.')
            log.w('')
            return None

        html = request.urlopen(url)
        soup = BeautifulSoup(html, 'html.parser')
        url = hp + \
            soup.find('div', attrs={'class': 'component-file'}).a.get('href')
        request.urlretrieve(url, self.file_path)

        return None


if __name__ == '__main__':
    pass
