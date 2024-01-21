'''
File Database source code

Author: Weiru Chen <flamingm321@gmail.com>
Date: 2024-01-21
'''

import os
import re
import json
from pathlib import Path
import importlib
import sys
from lib.error import FileExistInDataBase, UnknownFileType
from lib.log import SystemLog


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


class FileManager:
    '''
    File Manager use to manager file-base database
    '''
    def __init__(self, config):
        with open(config, 'r', encoding='utf-8') as f:
            self.config = json.load(f)
            if self.config["root"] is not None:
                return
        self.root = Path.absolute("./output/")
        self.config["root"] = str(self.root)
        with open(config, 'w', encoding='utf-8') as f:
            json.dump(self.config, f)

    def check_or_create_folder(self, path: str | Path):
        '''Create all directories in specified path which may not exist'''
        Path(path).mkdir(parents=True, exist_ok=True)

    def move(self, dst: str | Path, src: str | Path):
        '''
        Move @src file into @dst which @dst included filename and suffix type
        '''
        src_path = Path(src)
        dst_path = Path(dst)
        self.check_or_create_folder(dst_path.parent)
        src_path.rename(dst_path)


class ConfigFinder:
    '''
    Config Finder use to find specifed rule in config
    '''
    def __init__(self, config):
        with open(config, 'r', encoding='utf-8') as f:
            self.config = json.load(f)
        self.re_match = None
        self.rule = None
        self.file = None
        self.rulename = None

    def clear(self):
        '''Clear all config in RAM'''
        self.re_match = None
        self.rule = None
        self.file = None
        self.rulename = None

    def set_rule(self, rule):
        '''Helper function: setup rule with init root information'''
        self.rule = rule
        self.rule['root'] = self.config['root']

    def find_rule(self, rulename: str) -> bool:
        '''Find specified rule in config'''
        if rulename not in self.config["rules"].keys():
            return False
        self.rulename = rulename
        self.set_rule(self.config["rules"][rulename])
        return True

    def find_match(self, filepath: str) -> bool:
        '''Find rule which the filter rule match filepath'''
        self.clear()
        for rulename in self.config["rules"].keys():
            rule = self.config["rules"][rulename]
            if "format" not in rule:
                continue
            self.re_match = re.match(rule["format"], filepath)
            if self.re_match is not None:
                self.rulename = rulename
                self.set_rule(rule)
                self.file = Path(filepath)
                return True
        return False

    def dump_result(self):
        '''Dump debug info'''
        if self.file is None or self.re_match is None:
            return

        print(f"file: {self.file}")
        print(f"match result: {self.re_match}")
        # print(self.rule)
        print("folder layer:")
        for folder in self.rule["folder"][1:]:
            print(f"\t{folder}: {self.re_match.group(folder)}")
        print()

    def get_destination(self) -> None | str | Path:
        '''Helper function: Generate destination path which is matched'''
        if self.re_match is None or self.rule["folder"] is None:
            return None
        root = self.config["root"]
        folders = [self.rule["folder"][0]]
        folders.extend(
            [self.re_match.group(key) for key in self.rule["folder"][1:]]
        )
        return Path(root, *folders, self.file.name)


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

        for key in self.groups.keys():
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
