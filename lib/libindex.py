'''
File Database basic data structure

Author: Weiru Chen <flamingm321@gmail.com>
Date: 2024-01-21
'''
import sqlite3
from pathlib import Path
import re


class Index:
    '''File Database index which wrap sqlite3 function'''
    def __init__(self, path: str | Path) -> None:
        self.db = sqlite3.connect(path)
        self.cur = self.db.cursor()
        self.exe = self.cur.execute
        self.fa = self.cur.fetchall

    def init(self, tablename: str = "contents"):
        '''create database table'''
        raw_query = f"""
            CREATE TABLE IF NOT EXISTS {tablename} (
                id integer primary key autoincrement,
                datetime text,
                path text NOT NULL,
                tags text
            );"""
        query = re.sub(r"\n?\s+", " ", raw_query)
        self.exe(query)
    
    def query(self, cmd: str):
        '''SQL query'''
        query = re.sub(r"\n?\s+", " ", cmd)
        self.exe(query)
        self.db.commit()

    def add_column(self, tablename: str, column: str, type: str, 
                   opts: str = ""):
        '''Add new column into sql'''
        query = f"""
            ALTER TABLE {tablename} ADD {column} {type} {opts};
            """
        self.exe(query)

    def get_default_tablename(self) -> str:
        '''Get default tablename'''
        return "contents"

    def get_columns(self, tablename: str) -> list:
        '''Get all column in specified @tablename'''
        query = f"PRAGMA table_info({tablename});"
        self.exe(query)
        return [row[1] for row in self.fa()]
