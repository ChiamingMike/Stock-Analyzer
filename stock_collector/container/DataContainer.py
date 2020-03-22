'''
Created on 2020/03/06

@author: ChiamingMike
'''

import pandas

from constant.Definition import ColumnsDefinition
from logger.ExecutionLogger import AccumulativeDataLogger
from logger.ExecutionLogger import AverageDataLogger
from logger.Log import log


class DataContainer(object):

    def __init__(self) -> None:
        pass

    def register_accumulative_data(self) -> None:
        pass

    def register_average_data(self) -> None:
        pass

    def get_accumulative_data(self) -> None:
        pass

    def get_average_data(self) -> None:
        pass

    def dump_accumulative_data(self) -> None:
        pass

    def dump_average_data(self) -> None:
        pass


class JPDataContainer(DataContainer):

    __instance = None
    __is_initialized = False

    def __new__(cls):
        """
        """
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)

        return cls.__instance

    def __init__(self) -> None:
        """
        """
        if self.__is_initialized is True:
            return None

        self.__is_initialized = True

        self.stock_code = str()
        self.average_data_table = dict()
        self.data_table = dict()
        self.average_data = pandas.DataFrame()

        return None

    def register_accumulative_data(self, url_table) -> None:
        """
        """
        target_data = list()

        if url_table == dict():
            log.e('Failed to accumulate data (URL doesn\'t exist).')
            log.e('')
            return None

        for stock_code, urls in url_table.items():
            target_data = [pandas.read_html(url)[5] for url in urls]
            if len(target_data) != len(urls) or target_data == list():
                log.e(
                    f'Failed to accumulate data with URLs ({stock_code}).')
                log.e('')
                continue
            else:
                self.data_table[stock_code] = pandas.concat(
                    target_data, axis=0).sort_values(ColumnsDefinition.DATE,
                                                     ascending=False)
                log.i(f'Accumulated data with URLs related to {stock_code}.')
                log.i('')

        return None

    def register_average_data(self, stock_code, average_data) -> None:
        """
        """
        self.average_data_table[stock_code] = average_data

        return None

    def get_accumulative_data(self, stock_code: str) -> pandas.DataFrame:
        """
        """
        return self.data_table.get(stock_code, pandas.DataFrame())

    def get_average_data(self) -> pandas.DataFrame:
        """
        """
        return self.average_data_table

    def dump_accumulative_data(self, stock_name: str, stock_code: str) -> None:
        """
        """
        accumulative_data_logger = AccumulativeDataLogger(stock_name,
                                                          stock_code)
        accumulative_data_logger.dump_execution_log(
            self.data_table[stock_code])

        return None

    def dump_average_data(self) -> None:
        """
        """
        df_list = list()
        average_data_logger = AverageDataLogger()
        existence_log = average_data_logger.get_existence_log()
        if not existence_log.empty:
            df_list.append(existence_log)

        for stock_code, average_data in self.average_data_table.items():
            df_list.append(average_data)
            log.i(f'Exporting average data...({stock_code})')
            log.i('')
        else:
            self.average_data = pandas.concat(df_list, axis=0)
            self.average_data.sort_values(['TERM', 'CODE'], inplace=True)
            average_data_logger.dump_execution_log(self.average_data)

        return None


if __name__ == '__main__':
    pass
