'''
The general version of File Database plugin

Author: Weiru Chen <flamingm321@gmail.com>
Date: 2024-01-21
'''

import os
import uuid
import re
import datetime
from pathlib import Path
from lib import libindex


class Cache:
    '''Plugin basic class'''
    def __init__(self, cfg: dict):
        self.config = cfg
        path = cfg["cache_path"]
        if path is None or len(path) == 0:
            path = f"./caches/{uuid.uuid4()}.db"
        path = Path(self.config['root'], path)
        path.parent.mkdir(parents=True, exist_ok=True)

        if not os.path.exists(path):
            self.index = libindex.Index(path)
            self.index.init()
        else:
            self.index = libindex.Index(path)
        self._check_columns()

    def _check_columns(self):
        tbname = self.index.get_default_tablename()
        db_columns = self.index.get_columns(tbname)
        columns = []
        labels = self.config["labels"]
        for key in labels.keys():
            for ele in labels[key]:
                columns.append(ele)

        for ele in columns:
            if ele not in db_columns:
                if ele in ["year", "month", "day"]:
                    # self.index.add_column(tbname, ele, "integer")
                    print(f"Skip: {ele}")

    def search(self, meta: object) -> list:
        '''search specified file by @meta data'''
        tbname = self.index.get_default_tablename()
        if "parameter" not in meta or meta["parameter"] is None or\
           meta["parameter"] == []:
            parameter = "*"
        else:
            parameter = meta["parameter"]
            if isinstance(parameter, list):
                parameter = ','.join(parameter)

        and_conditions = []
        or_conditions = []
        conditions = ""
        if "starttime" in meta and "endtime" in meta:
            st = meta["starttime"]
            et = meta["endtime"]
            and_conditions.append(f'datetime between "{st}" and "{et}"')
        elif "starttime" in meta:
            st = meta["starttime"]
            and_conditions.append(f'datetime >= "{st}"')
        elif "endtime" in meta:
            et = meta["endtime"]
            and_conditions.append(f'datetime <= "{et}"')

        if "tags" in meta:
            tags = None
            if isinstance(meta["tags"], str):
                tags = meta["tags"].split(',')
            if isinstance(meta["tags"], list):
                tags = meta["tags"]
            if tags is not None:
                for tag in tags:
                    or_conditions.append(f'tags LIKE "%{tag}%"')

        # combine all conditions
        tmp = ""
        if len(or_conditions) > 0:
            tmp = ' or '.join(or_conditions)
            and_conditions.append(tmp)
        if len(and_conditions) > 0:
            tmp = ' and '.join(and_conditions)
            conditions = f"where {tmp}"
        query = f"SELECT {parameter} from {tbname} {conditions};"

        self.index.query(query)
        return self.index.fa()

    def add_cache(self, file: str | Path, cfg: dict, tags: None | list = None):
        '''Add file meta data'''
        file = file if isinstance(file, Path) else Path(file)
        finder = re.match(cfg["format"], file.name)

        # We known that year, month, and day in the file
        groups = finder.groupdict().keys()
        current_time = datetime.datetime.now()
        year = int(finder.group("year")) if "year" in groups\
            else current_time.year
        month = int(finder.group("month")) if "month" in groups\
            else current_time.month
        day = int(finder.group("day")) if "day" in groups else current_time.day
        hour = int(finder.group("hour")) if "hour" in groups else 0
        minute = int(finder.group("minute")) if "minute" in groups else 0
        second = int(finder.group("second")) if "second" in groups else 0

        tbname = self.index.get_default_tablename()
        dt = datetime.datetime(year, month, day, hour, minute, second)\
            .strftime('"%Y-%m-%d %H:%M:%S"')
        if tags is not None and len(tags) > 0:
            tag = ','.join(tags)
            self.index.query(f"""INSERT INTO {tbname} (datetime, path, tags)
                         VALUES ({dt}, \"{file.absolute()}\", \"{tag}\");""")
        else:
            self.index.query(f"""INSERT INTO {tbname} (datetime, path) VALUES
                         ({dt}, \"{file.absolute()}\");""")
