'''
Created on 2020/03/19

@author: ChiamingMike
'''

import datetime
import os
import pandas

from bs4 import BeautifulSoup
from urllib import request

from constant.Definition import UrlsDefinition
from logger.Log import log


class CodeContainer(object):

    def __init__(self, file_name: str) -> None:
        """
        """
        execution_date = datetime.datetime.now().strftime('%Y%m')
        self.file_name = f'{execution_date}_{file_name}'
        self.file_path = os.path.join(os.path.dirname(
            os.path.dirname(__file__)), 'asset', file_name)

        if not os.path.isfile(self.file_path):
            self.download_conversion_table()

        self.register_conversion_table()

        return None

    def register_conversion_table(self) -> None:
        pass

    def download_conversion_table(self) -> None:
        pass

    def get_conversion_table(self) -> pandas.Series:
        """
        """
        if self.conversion_table.empty:
            log.e('Failed to get conversion table.')
            log.e('')
            return pandas.Series()

        return self.conversion_table


class JPCodeContainer(CodeContainer):

    def __init__(self, stock_codes) -> None:
        """
        """
        file_name = 'JP_stock_list.xls'
        self.conversion_table = pandas.Series()

        self.stock_codes = stock_codes

        super().__init__(file_name)

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
        self.conversion_table = df.loc[self.stock_codes, 'name']

        return None

    def download_conversion_table(self) -> None:
        """
        """
        hp = UrlsDefinition.jpx.get('hp', str())
        url = UrlsDefinition.jpx.get('url', str())
        if str() in [hp, url]:
            log.w('Cannot find a URL to download List of TSE-listed Issues.')
            log.w('')
            return None

        html = request.urlopen(url)
        soup = BeautifulSoup(html, 'html.parser')
        url = hp + \
            soup.find('div', attrs={'class': 'component-file'}).a.get('href')
        request.urlretrieve(url, self.file_path)

        return None

    def get_conversion_table(self) -> pandas.Series:
        """
        """
        return super().get_conversion_table()


if __name__ == '__main__':
    pass
