import sqlite3
from werkzeug.security import safe_str_cmp, generate_password_hash

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

create_table = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)"
create_items_table = "CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY, name text, price real)"

cursor.execute(create_table)
cursor.execute(create_items_table)

insert_query = "INSERT INTO users VALUES(?, ?, ?)"

users = [
    (1, 'ade', generate_password_hash("ade", method='sha256')),
    (2, 'adeye', generate_password_hash("ade", method='sha256')),
    (3, 'adeyemo', generate_password_hash("ade", method='sha256'))
]


cursor.executemany(insert_query, users)
connection.commit()
connection.close()