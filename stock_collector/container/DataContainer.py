import pandas

from container.UrlContainer import UrlContainer
from logger.ExecutionLogger import AccumulativeDataLogger
from logger.Log import log


class DataContainer(object):

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

        self.url_container = UrlContainer()

        self.average_data_list = list()
        self.data_table = dict()

    def register_accumulative_data(self, url_table) -> None:
        """
        """
        target_data = list()

        if url_table == dict():
            log.e('        Failed to accumulate data (URL doesn\'t exist).')
            log.e('')
            return None

        for stock_code, urls in url_table.items():
            target_data = [pandas.read_html(url)[5] for url in urls]
            if len(target_data) != len(urls) or target_data == list():
                log.e(
                    f'        Failed to accumulate data with URLs related to {stock_code}.')
                log.e('')
                continue
            else:
                self.data_table[stock_code] = pandas.concat(target_data, axis=0).sort_values(
                    '日付', ascending=False)
                log.i(
                    f'        Accumulated data with URLs related to {stock_code}.')
                log.i('')

        return None

    def register_average_data(self, average_value_table) -> None:
        """
        """
        self.average_data_list.append(average_value_table)
        return None

    def get_accumulative_data(self, stock_code: str) -> pandas.DataFrame:
        """
        """
        return self.data_table.get(stock_code, pandas.DataFrame())

    def get_average_data(self) -> list:
        """
        """
        return self.average_data_list

    def dump_accumulative_data(self, stock_name, stock_code: str) -> None:
        """
        """
        stock_name = self.url_container.get_conversion_table(stock_code)
        if stock_name == str():
            log.e('        Failed to match stock name with stock code.')
            log.e('')
            return None

        accumulative_data_logger = AccumulativeDataLogger(
            stock_name, stock_code)
        accumulative_data_logger.dump_execution_log(
            self.data_table[stock_code])

        return None


if __name__ == '__main__':
    pass
