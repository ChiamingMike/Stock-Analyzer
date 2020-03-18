import time

from container.DataContainer import DataContainer
from container.UrlContainer import JPUrlContainer
from logger.ExecutionLogger import AverageDataLogger
from logger.Log import log
from processor.Processor import AverageDataProcessor


class StockParser(object):

    def __init__(self) -> None:
        """
        """
        self.url_container = JPUrlContainer()
        self.data_container = DataContainer()
        self.average_data_logger = AverageDataLogger()

        self.stock_codes = self.url_container.get_stock_codes()
        self.accumulate_urls()
        self.accumulate_data()

        return None

    def accumulate_urls(self) -> None:
        """
        """
        self.url_container.register_accumulative_url()
        self.url_table = self.url_container.get_url_table()

        return None

    def accumulate_data(self) -> None:
        """
        """
        self.data_container.register_accumulative_data(self.url_table)

        return None

    def calcualte_data(self):
        """
        """
        for stock_code in self.stock_codes:
            stock_name = self.url_container.get_conversion_table(stock_code)
            average_data_processor = AverageDataProcessor(stock_code)
            average_data_processor.calculate_data()
            self.export_data(stock_name, stock_code)

        return None

    def export_data(self, stock_name, stock_code):
        """
        """
        self.data_container.dump_accumulative_data(stock_name, stock_code)
        self.data_container.dump_average_data()

        return None


if __name__ == '__main__':
    start_time = time.time()
    stock_parser = StockParser()
    stock_parser.calcualte_data()
    end_time = time.time() - start_time
    log.i(f'TIME : {end_time} (s)')
