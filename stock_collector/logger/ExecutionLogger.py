import configparser
import datetime
import openpyxl
import os
import pandas

from logger.Log import log


class ExecutionLogger(object):

    def __init__(self, file_name: str) -> None:
        """
        """
        execution_date = datetime.datetime.now().strftime('%Y%m%d')

        self.log_file_name = f'{execution_date}_{file_name}.csv'
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
            log.w('        ' + str(e))
            log.w('        Failed to get the information from Logging.ini .')
            log.w('')
            return None

        try:
            if self.log_path == str():
                self.log_path = os.path.dirname(os.path.dirname(__file__))
            os.makedirs(os.path.join(self.log_path,
                                     execution_date), exist_ok=True)
            self.file_path = os.path.join(
                self.log_path, execution_date, self.log_file_name)
        except Exception as e:
            self.e('        ' + str(e))
            self.e('        Failed to create a log file.')
            self.e('')
            return None

        return None

    def dump_execution_log(self, accumulative_data: pandas.DataFrame) -> None:
        """
        """
        accumulative_data.to_csv(
            self.file_path, index=False, mode='w', encoding='cp932')
        return None


class AccumulativeDataLogger(ExecutionLogger):

    def __init__(self, sotck_name, stock_code) -> None:
        """
        """
        self.file_name = f'{stock_code}_{sotck_name}'
        super().__init__(self.file_name)
        return None

    def dump_execution_log(self, accumulative_data: pandas.DataFrame) -> None:
        """
        """
        super().dump_execution_log(accumulative_data)
        return None


class AverageDataLogger(ExecutionLogger):

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
            wb = openpyxl.load_workbook(filename=self.file_path)
            sheet = wb.worksheets[0]
            val = value_ave_data.values.tolist()

            row_length = len(val)
            for i in range(0, row_length):
                sheet.append(val[i])

            wb.save(filename=self.file_path)

        elif os.path.getsize(self.file_path) == 0:
            # create a new file
            value_ave_data.to_excel(excel_writer=self.file_path, sheet_name='stock_info',
                                    header=True, index=False, encoding='cp932')


if __name__ == '__main__':
    pass
