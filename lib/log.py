'''
Log system for File Database

Author: Weiru Chen <flamingm321@gmail.com>
Date: 2024-01-21
'''


import datetime
from enum import Enum

TIMEFORMAT = "%Y-%m-%d %H:%M:%S"


# Base on system time zone
def _get_current_time():
    return datetime.datetime.now()


class LogLevel(Enum):
    '''
    Log level
        INFO = 1
        WARN = 2
        DEBUG = 3
        ERROR = 4
    '''
    INFO = 1
    WARN = 2
    DEBUG = 3
    ERROR = 4

    def to_str(self):
        '''convert log level into string'''
        return self.name


class SystemLog:
    '''SystemLog class'''
    def __init__(self, title: str, show: bool = False) -> None:
        self.title = title
        self.show = show

    def _print(self, level: LogLevel, msg):
        if not self.show:
            return
        time = _get_current_time().strftime(TIMEFORMAT)
        print(f"{time} - [{level.name}] [{self.title}] {str(msg)}")

    def info(self, msg: str):
        '''log info message'''
        self._print(LogLevel.INFO, msg)

    def warn(self, msg: str):
        '''log warning message'''
        self._print(LogLevel.WARN, msg)

    def debug(self, msg: str):
        '''log debug message'''
        self._print(LogLevel.DEBUG, msg)

    def error(self, msg: str):
        '''log error message'''
        self._print(LogLevel.ERROR, msg)
