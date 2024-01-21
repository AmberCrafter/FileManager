'''
Module manager subsystem

Author: Weiru Chen <flamingm321@gmail.com>
Date: 2024-01-21
'''

import importlib
import sys


class ModuleManager:
    '''
    Module Manager use to manage python plugin
    '''
    def __init__(self):
        self.modules = {}

    def is_exist(self, module: str) -> bool:
        '''Check module loaded or not'''
        if module in sys.modules:
            return True
        return False

    def active(self, module: str):
        '''Active the module in ~/plugins'''
        if self.is_exist(module):
            print("Module `{module}` is already loaded.")
            return
        self.modules[module] = importlib.import_module(f".{module}", "plugins")

    def call(self, module: str, func: str, *args, **argv):
        '''Execute module function with arguments'''
        try:
            return self.modules[module].__getattribute__(func)(*args, **argv)
        except Exception as err:
            raise err
