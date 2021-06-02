from .init_database import sqlite_connect


def change_user_language(language, user_id):
    connect = sqlite_connect()
    cursor = connect.cursor()
    cursor.execute("UPDATE users SET language=? WHERE user_id=?;", (language, user_id))
    connect.commit()
    connect.close()


"""
    In the next version :)
"""
# def change_user_city(city, user_id):
#     connect = sqlite_connect()
#     cursor = connect.cursor()
#     cursor.execute("UPDATE users SET city=? WHERE user_id=?;", (city, user_id))
#     connect.commit()
#     connect.close()