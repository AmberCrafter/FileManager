from typing import Optional
from plugins import general


class Cache(general.Cache):
    # Overwrite _check_columns for init
    def _check_columns(self):
        pass

    # Overwrite search
    def search(self, meta: object) -> list:
        pass

    # Overwrite add cache
    def add_cache(self, filename: str, tags: None | list = None):
        pass


