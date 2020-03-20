'''
Created on 2020/03/06

@author: ChiamingMike
'''

import pandas

from constant.Definition import ColumnsDefinition
from container.DataContainer import JPDataContainer
from container.UrlContainer import JPUrlContainer
from logger.Log import log


class DataProcessor(object):

    def __init__(self, stock_code) -> None:
        """
        """
        self.data_container = JPDataContainer()
        self.url_container = JPUrlContainer()

        self.stock_code = stock_code
        self.stock_name = self.url_container.convert_into_name(self.stock_code)

        return None

    def set_target_data(self) -> None:
        """
        """
        return None

    def calculate_data(self) -> None:
        """
        """
        return None


class AverageDataProcessor(DataProcessor):

    def __init__(self, stock_code) -> None:
        """
        """
        self.length = int()
        self.open = str()
        self.high = str()
        self.low = str()
        self.close = str()
        super().__init__(stock_code)

        self.set_target_data()

        return None

    def set_target_data(self) -> None:
        """
        """
        accumulative_data = self.data_container.get_accumulative_data(
            self.stock_code)
        if accumulative_data.empty:
            log.e(f'No accumulative data relevant to {self.stock_code}')
            log.e('')
            return None

        try:
            self.length = len(accumulative_data)
            self.open = sum(
                accumulative_data.loc[:, ColumnsDefinition.OPENING_PRICE])
            self.high = sum(
                accumulative_data.loc[:, ColumnsDefinition.HIGH_PRICE])
            self.low = sum(
                accumulative_data.loc[:, ColumnsDefinition.LOW_PRICE])
            self.close = sum(
                accumulative_data.loc[:, ColumnsDefinition.CLOSING_PRICE])
        except Exception as e:
            log.e(e)
            log.e('Failed to prepare calculation with accumulative data.')
            log.e('')
            return None

        return None

    def calculate_data(self) -> None:
        """
        """
        average_data_table = dict()
        if str() in [self.open, self.high, self.low, self.close]:
            log.e('Failed to do calculation with accumulative data.')
            log.e('')
            return None

        average_data = pandas.DataFrame([{
            'Name': str(self.stock_name),
            'Code': str(self.stock_code),
            'Open (ave)': float(self.open / self.length),
            'High (ave)': float(self.high / self.length),
            'Low (ave)': float(self.low / self.length),
            'Close (ave)': float(self.close / self.length)
        }])

        average_data_table[self.stock_code] = average_data
        self.data_container.register_average_data(average_data_table)

        return None


if __name__ == '__main__':
    pass
