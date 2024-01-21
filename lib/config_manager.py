'''
Config manager subsystem

Author: Weiru Chen <flamingm321@gmail.com>
Date: 2024-01-21
'''

import re
import json
from pathlib import Path


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
