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
            log.w(e)
            log.w('Failed to get the information from Logging.ini .')
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
            self.e(e)
            self.e('Failed to create a log file.')
            self.e('')
            return None

        return None

    def dump_execution_log(self, accumulative_data: pandas.DataFrame) -> None:
        """
        """
        accumulative_data.to_csv(
            self.file_path, header=True, index=False, mode='w', encoding='cp932')
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
        self.file_name = 'stock_info'
        super().__init__(self.file_name)
        return None

    def dump_execution_log(self, accumulative_data: pandas.DataFrame) -> None:
        """
        """
        if os.path.isfile(self.file_path) and os.path.getsize(self.file_path) != 0:
            accumulative_data.to_csv(
                self.file_path, header=False, index=False, mode='a', encoding='cp932')
            return None
        super().dump_execution_log(accumulative_data)
        return None


if __name__ == '__main__':
    pass
