'''
File Database source code

Author: Weiru Chen <flamingm321@gmail.com>
Date: 2024-01-21
'''

import os
from lib.error import FileExistInDataBase, UnknownFileType
from lib.log import SystemLog
from lib.module_manager import ModuleManager
from lib.config_manager import ConfigFinder
from lib.file_manager import FileManager


class FileDB:
    '''File Database: Manager your files. This is user interface'''
    def __init__(self, config: str) -> None:
        self.finder = ConfigFinder(config)
        self.manager = FileManager(config)
        self.mods = ModuleManager()
        self.groups = {}
        self.log = SystemLog("FileDB", True)

    def _load_module_raw(self, rulename: str):
        '''Helper function: loading specified module/plugin with rulename'''
        if rulename is None:
            return

        for key in list(self.groups.keys()):
            if rulename == key:
                return

        self.mods.active(self.finder.rule["plugin"])
        self.groups[rulename] = {
            "db": self.mods.call(rulename, "Cache",
                                 cfg=self.finder.rule)
        }

    def load_module(self, rulename: str) -> bool:
        '''Loading specified module/plugin with rulename'''
        if not self.finder.find_rule(rulename):
            return False
        self._load_module_raw(rulename)
        return True

    def add(self, filepath: str, tags: None | list = None):
        '''
        Adding file into database
         @filepath: source file path
         @tags: tags list for this file
        '''
        if self.finder.find_match(filepath) and \
           "plugin" in self.finder.rule.keys():
            src = self.finder.file
            dst = self.finder.get_destination()

            if os.path.exists(dst):
                msg = FileExistInDataBase(f"{src} is exist in {dst}")
                self.log.error(msg)
                self.finder.clear()
                # raise msg
                return

            rulename = self.finder.rulename
            self._load_module_raw(rulename)
            self.groups[rulename]["db"].add_cache(dst, self.finder.rule, tags)
            self.manager.move(dst, src)
        else:
            # raise UnknownFileType(f"File name: {src}")
            self.log.warn(UnknownFileType(f"File: {filepath}"))
            return

    def search(self, rulename: str, meta: dict) -> list:
        '''Search files with @rulename and @meta data'''
        if self.load_module(rulename):
            return self.groups[rulename]["db"].search(meta)
        return []


def main():
    '''nothing'''
    # pass


if __name__ == "__main__":
    fs = FileDB("./config.json")

    files = [
        "./hello_2022_01_30_sadkld.txt",
        "./hello_2022_02_10_sadkld.txt",
        "./hello_2022_03_30_sadkld.txt",
        "./hello_2022_04_30_sadkld.txt",
    ]

    count = 0
    for file in files:
        with open(file, 'w', encoding='utf-8') as fd:
            fd.write("1234,123,12,1\n")
            fd.write("1234,123,12,1\n")

        fs.add(file, [f"count={count}"])
        fs.finder.dump_result()
        count += 1

    print(fs.search("general", {
        "starttime": "2022-01-01",
        "endtime": "2022-03-03"
        }))
    print(fs.search("general", {
        "parameter": ["datetime", "path"],
        "starttime": "2022-01-01",
        "endtime": "2022-03-03"
        }))
    print(fs.search("general", {
        "parameter": ["datetime", "tags"],
        "tags": "count"
        }))
    print(fs.search("general", {
        "parameter": ["datetime", "tags"],
        "tags": [1, 2]
        }))
