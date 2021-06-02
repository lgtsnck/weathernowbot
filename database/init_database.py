import sqlite3
from pathlib import Path


def sqlite_connect():
    connect = sqlite3.connect(database, check_same_thread=False)
    return connect


def init_sqlite():
    connect = sqlite_connect()
    cnt = connect.cursor()
    cnt.execute("""CREATE TABLE IF NOT EXISTS users(
        user_id INTEGER PRIMARY KEY,
        language TEXT DEFAULT NULL,
        city TEXT DEFAULT NULL,
        temp_scale TEXT DEFAULT NULL);
    """)
    connect.commit()
    connect.close()


database = Path("./database/users.db")

try:
    database.resolve(strict=True)
except FileExistsError:
    try:
        init_sqlite()
    except Exception as e:
        print("Create database error", e.__repr__(), e.args)
        pass
    else:
        print("Success")
