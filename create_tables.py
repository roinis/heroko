import sqlite3


def create_base_tables():
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()

    user_table_query = "CREATE TABLE IF NOT EXISTS user (id INTEGER PRIMARY KEY, username text, password text)"
    cursor.execute(user_table_query)

    message_table_query = 'CREATE TABLE IF NOT EXISTS message (id INTEGER PRIMARY KEY, sender_id INTEGER, receiver_id INTEGER,' \
                          ' message text, subject text, creation_date text, read INTEGER,' \
                          ' FOREIGN KEY (sender_id) REFERENCES user (id), FOREIGN KEY (receiver_id) REFERENCES user (id))'
    cursor.execute(message_table_query)

    connection.commit()
    connection.close()



