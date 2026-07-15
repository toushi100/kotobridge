import os
import sqlite3
class DB:
    def __init__(self, db_name: str = "kotobridge.db") :
        self.db_name = db_name
        self.db_path = os.path.abspath(f"./src/db/{db_name}")
        self.migration_files_dir = os.path.abspath("./src/db/migrations")
        self.conn = None
        self.cursor = None
        self.__check_and_create_db()
        self.connect()

    def connect(self):
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        return self

    def query(self, query: str):
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def insert(self, query: str):
        self.cursor.execute(query)
        self.conn.commit()
        return self.cursor.lastrowid
    
    def clear_db(self):
        self.cursor.execute("DELETE FROM videos")
        self.conn.commit()
        return True
    
    def update(self, query: str):
        self.cursor.execute(query)
        self.conn.commit()
        return True

    def __check_and_create_db(self):
        if not os.path.exists(self.db_path):
            self.__create_db(self.db_path)

    def __create_db(self, db_path):
        conn = sqlite3.connect(db_path)
        self.__setup_tables(conn, self.migration_files_dir)
        conn.commit()
        conn.close()

    def __setup_tables(self, conn, migrations_dir=None):
        cursor = conn.cursor()
        if migrations_dir and os.path.exists(migrations_dir):
            migration_files = sorted([f for f in os.listdir(migrations_dir) if f.endswith('.sql')])
            for filename in migration_files:
                file_path = os.path.join(migrations_dir, filename)
                with open(file_path, 'r', encoding='utf-8') as f:
                    cursor.executescript(f.read())
        conn.commit()

