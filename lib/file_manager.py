'''
File manager subsystem

Author: Weiru Chen <flamingm321@gmail.com>
Date: 2024-01-21
'''

import json
from pathlib import Path


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
