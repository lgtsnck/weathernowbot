from .init_database import sqlite_connect


def get_language(user_id):
    connect = sqlite_connect()
    cursor = connect.cursor()
    cursor.execute("SELECT language FROM users WHERE user_id=?;", user_id)
    language = cursor.fetchone()
    connect.close()
    lang = ''.join(language)
    return lang
