from .init_database import sqlite_connect


def add_user(user_id, users_id):
    connect = sqlite_connect()
    cursor = connect.cursor()
    cursor.execute("SELECT user_id FROM users WHERE user_id = {};".format(users_id))
    users_id_data = cursor.fetchone()
    if users_id_data is None:
        cursor.execute("INSERT INTO users (user_id) VALUES(?);", user_id)
        connect.commit()
    else:
        # print("Пользователь уже есть -_-")
        pass
    connect.close()
