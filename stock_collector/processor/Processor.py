import pandas

from constant.Definition import ColumnsDefinition
from container.DataContainer import DataContainer
from container.UrlContainer import UrlContainer
from logger.Log import log


class DataProcessor(object):

    def __init__(self, stock_code) -> None:
        """
        """
        self.data_container = DataContainer()
        self.url_container = UrlContainer()

        self.stock_code = stock_code
        self.stock_name = self.url_container.get_conversion_table(
            self.stock_code)

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
        self.length = len(accumulative_data)
        self.open = sum(
            accumulative_data.loc[:, ColumnsDefinition.OPENING_PRICE])
        self.high = sum(accumulative_data.loc[:, ColumnsDefinition.HIGH_PRICE])
        self.low = sum(accumulative_data.loc[:, ColumnsDefinition.LOW_PRICE])
        self.close = sum(
            accumulative_data.loc[:, ColumnsDefinition.CLOSING_PRICE])

        return None

    def calculate_data(self) -> None:
        """
        """
        average_data_table = dict()
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
