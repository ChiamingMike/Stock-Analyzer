'''
Created on 2020/03/06

@author: ChiamingMike
'''

import configparser
import os

from bs4 import BeautifulSoup
from urllib import request

from constant.Definition import UrlsDefinition
from constant.Definition import PeriodDefinition
from container.CodeContainer import JPCodeContainer
from logger.Log import log


class UrlContainer(object):

    def __init__(self) -> None:
        """
        """
        try:
            root = os.path.join(os.path.dirname(
                os.path.dirname(__file__)), 'conf', 'Setting.ini')
            config = configparser.ConfigParser()
            config.read(root)
            section = 'DEFAULT'
            self.term = config.get(section, 'period')
            self.period = PeriodDefinition.period.get(self.term, None)
        except Exception as e:
            log.w(e)
            log.w('Failed to get the information from setting.ini .')
            log.w('')
            return None

        return None

    def create_initial_url(self) -> None:
        pass

    def register_accumulative_url(self) -> None:
        pass

    def get_url_table(self) -> dict:
        """
        """
        return self.url_table

    def get_term(self) -> str:
        """
        """
        return self.term

    def _is_url_valid(self, url, stock_code) -> bool:
        """
        """
        try:
            result = request.urlopen(url)
            result.close()
            return True
        except Exception as e:
            log.w(e)
            log.w(f'Invalid URL for stock code {stock_code}')
            log.w('')
            return False


class JPUrlContainer(UrlContainer):

    def __init__(self) -> None:
        """
        """
        self.url_table = dict()
        self.period = str()
        super().__init__()

        self.code_container = JPCodeContainer()
        self.create_initial_url()

        return None

    def create_initial_url(self) -> None:
        """
        """
        url_format = UrlsDefinition.kabutan_jp.get('url', str())
        if url_format == str():
            log.w('Cannot find a format to create initial url.')
            log.w('')
            return None

        stock_codes = self.code_container.get_stock_codes()
        OFFSET = 1
        for stock_code in stock_codes:
            url = url_format.format(stock_code=stock_code,
                                    period=self.period,
                                    offset=OFFSET)
            if self._is_url_valid(url, stock_code):
                self.url_table[stock_code] = [url]

        return None

    def register_accumulative_url(self) -> None:
        """
        """
        next_url_format = UrlsDefinition.kabutan_jp.get('next_page', str())
        if next_url_format == str():
            log.w('Cannot find a format to create url for next page.')
            log.w('')
            return None

        if self.url_table == dict():
            log.e('Failed to collect relevant URLs.')
            log.e('Initial URL doesn\'t exist.')
            log.e('')
            return None

        for stock_code in self.url_table.keys():

            while True:
                html = request.urlopen(self.url_table[stock_code][-1])
                soup = BeautifulSoup(html, 'html.parser')
                is_exist_pager = soup.find('li', string='次へ＞')
                if not is_exist_pager:
                    stock_name = self.code_container.convert_into_name(
                        stock_code)
                    log.i(
                        f'Found URLs related to {stock_code} ({stock_name}).')
                    log.i(
                        f'{len(self.url_table[stock_code])} URLs found.')
                    log.i('')
                    break
                elif is_exist_pager:
                    next_page = is_exist_pager.a.get('href')
                    if not next_page:
                        log.e('Failed to find next page.')
                        log.e('')
                        return None

                    next_url = next_url_format.format(next_page=next_page)
                    self.url_table[stock_code].append(next_url)
                    # time.sleep(3)

        return None


if __name__ == '__main__':
    pass
