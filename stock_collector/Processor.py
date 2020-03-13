import pandas as pd


class DataHandler:
    def __init__(self, all_data, stock_name, stock_code):
        self.stock_name = stock_name
        self.stock_code = stock_code
        self.open = all_data[['始値']].values
        self.high = all_data[['高値']].values
        self.low = all_data[['安値']].values
        self.close = all_data[['終値']].values

    def calculate_data(self):
        value_ave_data = pd.DataFrame({
            'Name': [self.stock_name],
            'Code': [self.stock_code],
            'Open(ave)': [int(sum(self.open) / len(self.open))],
            'High(ave)':	[int(sum(self.high) / len(self.high))],
            'Low(ave)': [int(sum(self.low) / len(self.low))],
            'Close(ave)': [int(sum(self.close) / len(self.close))]
        })

        return value_ave_data
