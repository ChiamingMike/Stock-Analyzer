import pandas

from logger.Log import log


class DataProcessor(object):

    def __init__(self) -> None:
        """
        """
        self.open = str()
        self.high = str()
        self.low = str()
        self.close = str()

    def pre_calculate_data(self, accumulative_data: pandas.DataFrame) -> None:
        """
        """
        self.open = accumulative_data[['始値']].values
        self.high = accumulative_data[['高値']].values
        self.low = accumulative_data[['安値']].values
        self.close = accumulative_data[['終値']].values

        return None

    def calculate_data(self,
                       stock_name: str,
                       stock_code: str,
                       accumulative_data: pandas.DataFrame) -> pandas.DataFrame:
        """
        """
        self.pre_calculate_data(accumulative_data)

        average_value_table = pandas.DataFrame({
            'Name': [stock_name],
            'Code': [stock_code],
            'Open (ave)': [int(sum(self.open) / len(self.open))],
            'High (ave)':	[int(sum(self.high) / len(self.high))],
            'Low (ave)': [int(sum(self.low) / len(self.low))],
            'Close (ave)': [int(sum(self.close) / len(self.close))]
        })

        return average_value_table


if __name__ == '__main__':
    pass
