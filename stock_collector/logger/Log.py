import configparser
import datetime
import logging
import os


class Log(object):

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

        self.__is_initialized = True

        self.logger = logging.getLogger(__name__)
        self.file_path = str()

        log_format = '%(asctime)s: %(message)s'

        self.log_level = logging.WARNING

        try:
            root = os.path.join(os.path.dirname(
                os.path.dirname(__file__)), 'conf', 'Logging.ini')
            config = configparser.ConfigParser()
            config.read(root)
            logging_information = config['LOGGING']
            self.log_level = int(logging_information['LOG_LEVEL'])
            self.log_path = logging_information['LOG_PATH']
        except Exception as e:
            self.w(str(e))
            self.w('Failed to get the information from Loggind.ini .')
            self.w('')
            return None

        logging.basicConfig(level=self.log_level,
                            format=log_format,
                            datefmt='%Y-%m-%d %H:%M:%S')

        execution_date = datetime.datetime.now().strftime('%Y%m%d')
        self.file_name = datetime.datetime.now().strftime('%Y%m%d') + '.log'
        try:
            root = os.path.dirname(os.path.dirname(__file__))
            os.makedirs(os.path.join(root, execution_date), exist_ok=True)
            file_path = os.path.join(root, execution_date, self.file_name)

            self.file_handler = logging.FileHandler(
                filename=file_path, mode='w')
            self.file_handler.setLevel(self.log_level)
            self.file_handler.setFormatter(logging.Formatter(log_format))
            self.logger.addHandler(self.file_handler)
        except Exception as e:
            self.e(str(e))
            self.e('Failed to create a log file.')
            self.e('')
            return None

        return None

    def c(self, msg):
        self.logger.log(logging.CRITICAL, 'CRITICAL:        ' + str(msg))
        return None

    def e(self, msg):
        self.logger.log(logging.ERROR, 'ERROR:        ' + str(msg))
        return None

    def w(self, msg):
        self.logger.log(logging.WARNING, 'WARN:        ' + str(msg))
        return None

    def i(self, msg):
        self.logger.log(logging.INFO, 'INFO:        ' + str(msg))
        return None

    def d(self, msg):
        self.logger.log(logging.DEBUG, 'DEBUG:        ' + str(msg))
        return None

    def t(self, msg):
        self.logger.log(logging.DEBUG, 'TRACE:        ' + str(msg))
        return None


log = Log()
