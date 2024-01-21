import datetime
from enum import Enum

TIMEFORMAT = "%Y-%m-%d %H:%M:%S"


# Base on system time zone
def _get_current_time():
    return datetime.datetime.now()


class GeneralException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class FileExistInDataBase(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class UnknownFileType(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class LogLevel(Enum):
    INFO = 1
    WARN = 2
    DEBUG = 3
    ERROR = 4

    def to_str(self):
        return self.name


class SystemLog:
    def __init__(self, title: str, show: bool = False) -> None:
        self.title = title
        self.show = show

    def _print(self, level: LogLevel, msg):
        if not self.show:
            return
        time = _get_current_time().strftime(TIMEFORMAT)
        print(f"{time} - [{level.name}] [{self.title}] {str(msg)}")

    def info(self, msg: str):
        self._print(LogLevel.INFO, msg)

    def warn(self, msg: str):
        self._print(LogLevel.WARN, msg)

    def debug(self, msg: str):
        self._print(LogLevel.DEBUG, msg)

    def error(self, msg: str):
        self._print(LogLevel.ERROR, msg)








