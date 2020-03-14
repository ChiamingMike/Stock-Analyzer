import configparser
import datetime
import openpyxl
import os
import pandas


class DataSaver:
    def __init__(self, file_name: str) -> None:
        """
        """
        execution_date = datetime.datetime.now().strftime('%Y%m%d')

        self.log_file_name = f'{execution_date}_{file_name}'
        self.is_header_writtern = bool()
        self.log_path = str()
        self.file_path = str()

        try:
            root = os.path.join(os.path.dirname(
                os.path.dirname(__file__)), 'conf', 'Logging.ini')
            config = configparser.ConfigParser()
            config.read(root)
            logging_information = config['LOGGING']
            self.log_path = logging_information['LOG_PATH']
        except Exception as e:
            print('')  # error_msg

        try:
            root = os.path.dirname(os.path.dirname(__file__))
            os.makedirs(os.path.join(root, execution_date), exist_ok=True)
            self.file_path = os.path.join(
                root, execution_date, self.log_file_name)
            if os.path.isfile(self.file_path):
                self.is_header_writtern = True
            self.log_file = open(self.file_path, mode='a')
        except Exception as e:
            print('')  # error_msg

        return None

    def dump_execution_log(self) -> None:
        """
        """
        return None


class AccumulativeDataLogger(DataSaver):
    def __init__(self) -> None:
        """
        """
        self.file_name = 'stock_detail.xlsx'
        super().__init__(self.file_name)
        return None

    def dump_execution_log(self,
                           stock_name: str,
                           stock_code: str,
                           accumulative_data: pandas.DataFrame) -> None:
        """
        """
        sheet_nm = f'{stock_name}_{stock_code}'

        if os.path.getsize(self.file_path) != 0:
            # 既存ファイルに追記
            with pandas.ExcelWriter(path=self.file_path, mode='a') as writer:
                writer.book = openpyxl.load_workbook(filename=self.file_path)
                accumulative_data.to_excel(writer, sheet_name=sheet_nm,
                                           header=True, index=False, encoding='cp932')
        elif os.path.getsize(self.file_path) == 0:
            # 新規ファイルを作成
            accumulative_data.to_excel(excel_writer=self.file_path, sheet_name=sheet_nm,
                                       header=True, index=False, encoding='cp932')
        return None


class AverageDataLogger(DataSaver):
    def __init__(self) -> None:
        """
        """
        self.file_name = 'stock_info.xlsx'
        super().__init__(self.file_name)
        return None

    def output_ave_data(self, average_data: pandas.DataFrame) -> None:
        """
        """
        average_data_list = list()
        average_data_list.append(average_data)
        value_ave_data = pandas.concat(average_data_list)
        if os.path.getsize(self.file_path) != 0:
            # 既存ファイルに追記
            wb = openpyxl.load_workbook(filename=self.file_path)
            sheet = wb.worksheets[0]
            val = value_ave_data.values.tolist()

            row_length = len(val)
            for i in range(0, row_length):
                sheet.append(val[i])

            wb.save(filename=self.file_path)

        elif os.path.getsize(self.file_path) == 0:
            # 新規ファイルを作成
            value_ave_data.to_excel(excel_writer=self.file_path, sheet_name='stock_info',
                                    header=True, index=False, encoding='cp932')
            # self.value_ave_data_list.clear()


if __name__ == '__main__':
    pass
