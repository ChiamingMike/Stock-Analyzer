import datetime
import time

import Processor
import Collector
import DataContainer


class StockParser(object):

    def __init__(self):
        """
        """
        pass
        return None

    def collect_stock_data(self):
        """
        """
        l_creater = Collector.LinkCreater()
        stock_code_list, url_list = l_creater.make_link()
        value_ave_data_list = list()
        for num, url in enumerate(url_list):
            print(num, url)
            l_finder = Collector.DataParser(stock_code_list[num], url)
            stock_name, url_list = l_finder.find_target_url_list()
            all_data = l_finder.parse_data(url_list)
            d_handler = Processor.DataHandler(
                all_data, stock_name, stock_code_list[num])
            value_ave_data_df = d_handler.calculate_data()
            value_ave_data_list.append(value_ave_data_df)
            d_saver = DataContainer.DataSaver(
                stock_name, stock_code_list[num], all_data, value_ave_data_list)
            d_saver.output_all_data()
            d_saver.output_ave_data()
            value_ave_data_list.clear()

        return None


if __name__ == '__main__':
    print(datetime.datetime.now())
    stock_parser = StockParser()
    stock_parser.collect_stock_data()
    print(datetime.datetime.now())
