import os, re, json
from pathlib import Path

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

    def clear(self):
        self.re_match = None
        self.rule = None

    def find_match(self, filename: str) -> bool:
        self.clear()
        for key in self.config["rules"].keys():
            rule = self.config["rules"][key]
            if "format" not in rule:
                continue
            self.re_match = re.match(rule["format"], filename)
            if self.re_match is not None:
                self.rule = rule
                self.file = Path(filename)
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


def main():
    pass


if __name__ == "__main__":
    finder = ConfigFinder("./config.json")
    manager = FileManager("./config.json")
    test = "./hello_1234_56_78_sadkld.nc"
    with open(test, 'w') as fd:
        fd.write("1234,123,12,1\n")
        fd.write("1234,123,12,1\n")

    finder.find_match(test)
    finder.dump_result()
    manager.move(finder.get_destination(), finder.file)
