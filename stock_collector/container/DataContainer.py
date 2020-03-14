import pandas


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

        self.average_data_list = list()
        self.data_table = dict()

    def accumulate_data(self, url_table) -> None:
        """
        """
        target_data = list()

        if url_table == dict():
            print('')  # error_msg

        for stock_code, urls in url_table.items():
            target_data = [pandas.read_html(url)[5] for url in urls]
            self.data_table[stock_code] = pandas.concat(target_data)

        return None

    def get_accumulative_data(self, stock_code: str) -> pandas.DataFrame:
        """
        """
        return self.data_table.get(stock_code, str())

    def register_average_data(self, average_value_table) -> None:
        """
        """
        self.average_data_list.append(average_value_table)
        return None

    def get_average_data(self) -> list:
        """
        """
        return self.average_data_list


if __name__ == '__main__':
    pass
