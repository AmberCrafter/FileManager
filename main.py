import os, re, json
from pathlib import Path
import importlib
import sys


class ModuleManager:
    def __init__(self):
        self.modules = {}
    
    def is_exist(self, module: str) -> bool:
        if module in sys.modules:
            return True
        return False

    def active(self, module: str):
        if self.is_exist(module):
            print("Module `{module}` is already loaded.")
            return
        self.modules[module] = importlib.import_module(f".{module}", "plugins")

    def call(self, module: str, func: str, *args, **argv):
        try:
            return self.modules[module].__getattribute__(func)(*args, **argv)
        except Exception as err:
            raise err


class FileManager:
    def __init__(self, config):
        self.config = json.load(open(config, 'r'))
        if self.config["root"] is None:
            self.root = Path.absolute("./output/")
            self.config["root"] = str(self.root)
            json.dump(self.config, open(config, 'w'))

    def check_or_create_folder(self, path: str | Path):
        Path(path).mkdir(parents=True, exist_ok=True)

    def move(self, dst: str | Path, src: str | Path):
        src_path = Path(src)
        dst_path = Path(dst)
        self.check_or_create_folder(dst_path.parent)
        src_path.rename(dst_path)


class ConfigFinder:
    def __init__(self, config):
        self.config = json.load(open(config, 'r'))
        self.re_match = None
        self.rule = None
        self.file = None
        self.key = None

    def clear(self):
        self.re_match = None
        self.rule = None

    def find_match(self, filepath: str) -> bool:
        self.clear()
        for key in self.config["rules"].keys():
            rule = self.config["rules"][key]
            rule["root"] = self.config["root"]
            if "format" not in rule:
                continue
            self.re_match = re.match(rule["format"], filepath)
            if self.re_match is not None:
                self.key = key
                self.rule = rule
                self.file = Path(filepath)
                return True
        return False

    def dump_result(self):
        print(self.re_match)
        print(self.rule)

        print("folder layer:")
        for folder in self.rule["folder"][1:]:
            print(f"\t{folder}: {self.re_match.group(folder)}")

    def get_destination(self) -> None | str | Path:
        if self.re_match is None or self.rule["folder"] is None:
            return None
        root = self.config["root"]
        folders = [self.rule["folder"][0]]
        folders.extend(
            [self.re_match.group(key) for key in self.rule["folder"][1:]]
        )
        return Path(root, *folders, self.file.name)


class FileSystem:
    def __init__(self, config: str) -> None:
        self.finder = ConfigFinder(config)
        self.manager = FileManager(config)
        self.mods = ModuleManager()
        self.groups = {}

    def add(self, filepath: str):
        if self.finder.find_match(filepath) and \
          "plugin" in self.finder.rule.keys():
            src = self.finder.file
            dst = self.finder.get_destination()

            self.mods.active(self.finder.rule["plugin"])
            key = self.finder.key
            if key not in self.groups.keys():
                self.groups[key] = {
                    "db": self.mods.call(key, "Cache",
                                         cfg=self.finder.rule)
                }

            self.groups[key]["db"].add_cache(dst, self.finder.rule)
            self.manager.move(dst, src)
        else:
            # TODO
            pass

    def search(self, classname: str, meta: dict) -> list:
        return self.groups[classname]["db"].search(meta)


def main():
    pass


if __name__ == "__main__":
    fs = FileSystem("./config.json")

    files = [
        "./hello_2022_01_30_sadkld.txt",
        "./hello_2022_02_10_sadkld.txt",
        "./hello_2022_03_30_sadkld.txt",
        "./hello_2022_04_30_sadkld.txt",
    ]

    for f in files:
        with open(f, 'w') as fd:
            fd.write("1234,123,12,1\n")
            fd.write("1234,123,12,1\n")

        fs.add(f)
        fs.finder.dump_result()

    print(fs.search("general", dict(starttime="2022-01-01", endtime="2022-03-03")))
    print(fs.search("general", dict(parameter=["datetime", "path"], starttime="2022-01-01", endtime="2022-03-03")))

