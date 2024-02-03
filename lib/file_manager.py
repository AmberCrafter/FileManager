'''
File manager subsystem

Author: Weiru Chen <flamingm321@gmail.com>
Date: 2024-01-21
'''

from pathlib import Path
from lib.config_manager import ConfigManager


class FileManager:
    '''
    File Manager use to manager file-base database
    '''
    def __init__(self, config):
        self.config = ConfigManager(config)
        if self.config.get()["root"] is not None:
            return
        self.root = Path.absolute("./output/")
        self.config.set("root", str(self.root))
        self.config.save()

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
