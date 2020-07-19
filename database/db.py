import sqlite3

__connection = None


def get_db():
    global __connection
    if __connection is None:
        __connection = sqlite3.connect('E:/reposPython/tg_bot/database/tg_base.db')
    return __connection


def init_db(flag: bool = False):
    connector = get_db()

    cursor = connector.cursor()
    if flag:
        cursor.execute('DROP TABLE IF EXISTS users')
    cursor.execute("""CREATE TABLE IF NOT EXISTS users (id TEXT, is_peacked BOOLEAN)""")

    connector.commit()


def insert_to_db(user_id: str, ispeacked: bool):
    connector = get_db()
    cursor = connector.cursor()
    # TODO Перевірка id

    cursor.execute("INSERT INTO users (id, is_peacked) VALUES (?,?)", (user_id, ispeacked))
    connector.commit()


def add_to_favorite(id, fav):
    connector = get_db()
    cursor = connector.cursor()
    # print(get_favorites(id))
    if get_favorites(id)[0][0] is not None:
        cursor.execute("UPDATE users SET fav_city=? WHERE id=?", (get_favorites(id)[0][0] + ',' + fav, id))
    else:
        cursor.execute("UPDATE users SET fav_city=? WHERE id=?", (fav, id))
    connector.commit()


def get_favorites(id):
    connector = get_db()
    cursor = connector.cursor()

    favorite_citys = cursor.execute("SELECT fav_city FROM users WHERE id=?", (id,)).fetchall()
    connector.commit()
    return favorite_citys


def get_status(id: str):
    connector = get_db()
    cursor = connector.cursor()
    status = cursor.execute("SELECT is_peacked FROM users WHERE id=?", (str(id),)).fetchall()
    connector.commit()
    return status

def del_favorites(id):
    connector = get_db()
    cursor = connector.cursor()
    cursor.execute("UPDATE users SET fav_city=? WHERE id=?", ('<null>', id))
    connector.commit()

def get_id(id):
    connector = get_db()
    cursor = connector.cursor()
    is_id = cursor.execute("SELECT * FROM users WHERE id=?", (str(id),)).fetchall()
    if is_id == []:
        return False
    else:
        return True


if __name__ == '__main__':
    init_db(True)
    insert_to_db('5656456464', True)
