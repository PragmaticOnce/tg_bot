import sqlite3

def create_db(db_file):
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_messages (
    id      TEXT,
    is_peeked   INTEGER
    );
    """)

    connection.commit()


if __name__ == '__main__':
    create_db('db.db')