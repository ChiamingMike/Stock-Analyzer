import time

from container.DataContainer import DataContainer
from container.UrlContainer import UrlContainer
from logger.ExecutionLogger import AverageDataLogger
from logger.Log import log
from processor.Processor import AverageDataProcessor


class StockParser(object):

    def __init__(self):
        """
        """
        self.url_container = UrlContainer()
        self.data_container = DataContainer()
        self.average_data_logger = AverageDataLogger()
        return None

    def collect_stock_data(self):
        """
        """
        self.url_container.register_accumulative_url()
        stock_codes = self.url_container.get_stock_codes()
        url_table = self.url_container.get_url_table()
        self.data_container.register_accumulative_data(url_table)
        for stock_code in stock_codes:
            stock_name = self.url_container.get_conversion_table(stock_code)
            self.data_container.dump_accumulative_data(stock_name, stock_code)
            average_data_processor = AverageDataProcessor(stock_code)
            average_data_processor.calculate_data()
            self.data_container.dump_average_data()

        return None


if __name__ == '__main__':
    start_time = time.time()
    stock_parser = StockParser()
    stock_parser.collect_stock_data()
    end_time = time.time() - start_time
    log.i(f'        TIME : {end_time} (s)')
