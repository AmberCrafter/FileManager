'''
The File Database plugin template

Author: Weiru Chen <flamingm321@gmail.com>
Date: 2024-01-21
'''

from pathlib import Path
from plugins import general


class Cache(general.Cache):
    '''
    Basic class for File database plugin

    Requirements:
     - Overwrite search method
     - Overwrite add_cache method
    '''
    # Overwrite search
    def search(self, meta: object) -> list:
        pass

    # Overwrite add cache
    def add_cache(self, file: str | Path, cfg: dict, tags: None | list = None):
        pass
