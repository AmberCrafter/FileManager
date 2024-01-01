import sqlite3
from pathlib import Path
import re


class Index:
    def __init__(self, path: str | Path) -> None:
        self.db = sqlite3.connect(path)
        self.cur = self.db.cursor()
        self.exe = self.cur.execute
        self.fa = self.cur.fetchall

    def init(self, tablename: str = "contents"):
        raw_query = f"""
            CREATE TABLE IF NOT EXISTS {tablename} (
                id integer primary key autoincrement,
                datetime text,
                path text NOT NULL
            );"""
        query = re.sub(r"\n?\s+", " ", raw_query)
        self.exe(query)
    
    def query(self, cmd: str):
        query = re.sub(r"\n?\s+", " ", cmd)
        self.exe(query)
        self.db.commit()

    def add_column(self, tablename: str, column: str, type: str, 
                   opts: str = ""):
        query = f"""
            ALTER TABLE {tablename} ADD {column} {type} {opts};
            """
        self.exe(query)

    def get_default_tablename(self) -> str:
        return "contents"

    def get_columns(self, tablename: str) -> list:
        query = f"PRAGMA table_info({tablename});"
        self.exe(query)
        return [row[1] for row in self.fa()]

