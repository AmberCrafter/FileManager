'''
Config manager subsystem

Author: Weiru Chen <flamingm321@gmail.com>
Date: 2024-01-21
'''

import re
import os
import json
from pathlib import Path
from enum import Enum
import toml


class ConfigType(Enum):
    '''Config file type'''
    UNKNOWN = 0
    TEXT = 1
    INI = 2
    JSON = 3
    TOML = 4

    @staticmethod
    def get(suffix: str):
        """Retrieve config file enum type"""
        suffix = suffix.lower()
        if suffix == 'txt':
            return ConfigType.TEXT
        if suffix == 'ini':
            return ConfigType.INI
        if suffix == 'json':
            return ConfigType.JSON
        if suffix == 'toml':
            return ConfigType.TOML
        return ConfigType.UNKNOWN


class ConfigManager:
    '''
    Config Manager use to manager config file

    Note. current only support Json
    '''
    def __init__(self, config):
        self.path = Path(config)
        self.file = self.path.name
        self.type = ConfigType.get(self.path.suffix[1:])

        if self.type == ConfigType.JSON:
            with open(config, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
        elif self.type == ConfigType.TOML:
            with open(config, 'r', encoding='utf-8') as f:
                self.config = toml.load(f)
        else:
            raise f"[ConfigManager] not support config format: {self.type}\
                  (file: {self.file})"

    def save(self):
        '''Save config to file'''
        if self.type == ConfigType.JSON:
            with open(self.path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f)
        elif self.type == ConfigType.TOML:
            with open(self.path, 'w', encoding='utf-8') as f:
                toml.dump(self.config, f)
        else:
            raise f"[ConfigManager] not support config format: {self.type}\
                  (file: {self.file})"

    def delete(self):
        '''Remove config file'''
        os.remove(self.path)

    def reload(self):
        '''Reload config'''
        if self.type == ConfigType.JSON:
            with open(self.path, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
        elif self.type == ConfigType.TOML:
            with open(self.path, 'r', encoding='utf-8') as f:
                self.config = toml.load(f)
        else:
            raise f"[ConfigManager] not support config format: {self.type}\
                  (file: {self.file})"

    def get(self) -> dict:
        '''Get config from RAM'''
        return self.config

    def set(self, keys: str | list, value):
        '''Set config'''
        if isinstance(keys, str):
            self.config[keys] = value
        elif isinstance(keys, list):
            cfg = self.config
            for key in keys[:-1]:
                cfg = cfg[key]
            cfg[keys[-1]] = value


class ConfigFinder:
    '''
    Config Finder use to find specifed rule in config
    '''
    def __init__(self, config):
        self.config = ConfigManager(config)
        self.re_match = None
        self.rule = None
        self.file = None
        self.rulename = None

    def clear(self):
        '''Clear all config in RAM and reload from file'''
        self.re_match = None
        self.rule = None
        self.file = None
        self.rulename = None
        self.config.reload()

    def set_rule(self, rule):
        '''Helper function: setup rule with init root information'''
        self.rule = rule
        self.rule['root'] = self.config.config['root']

    def find_rule(self, rulename: str) -> bool:
        '''Find specified rule in config'''
        if rulename not in self.config.get()["rules"].keys():
            return False
        self.rulename = rulename
        self.set_rule(self.config.get()["rules"][rulename])
        return True

    def find_match(self, filepath: str) -> bool:
        '''Find rule which the filter rule match filepath'''
        self.clear()
        for rulename in self.config.get()["rules"].keys():
            rule = self.config.get()["rules"][rulename]
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
        root = self.config.get()["root"]
        folders = [self.rule["folder"][0]]
        folders.extend(
            [self.re_match.group(key) for key in self.rule["folder"][1:]]
        )
        return Path(root, *folders, self.file.name)


if __name__ == "__main__":
    cfg = ConfigManager("./config.json")
    cfg.set(['rules', 'unknown', 'type'], '123')
    print(cfg.get())
