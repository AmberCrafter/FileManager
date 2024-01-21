'''
Error types in File Database

Author: Weiru Chen <flamingm321@gmail.com>
Date: 2024-01-21
'''


class GeneralException(Exception):
    '''General exception class'''
    def __init__(self, message: str):
        super().__init__(message)


class FileExistInDataBase(Exception):
    '''File exist exception'''
    def __init__(self, message: str):
        super().__init__(message)


class UnknownFileType(Exception):
    '''Unknown file type exception'''
    def __init__(self, message: str):
        super().__init__(message)
