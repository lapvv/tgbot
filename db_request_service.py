import sqlite3

conn = sqlite3.connect("users.db")

CREATE_QUERY = """
    CREATE TABLE IF NOT EXISTS users (
        user_id int PRIMARY KEY,
        username text,
        chat_id int
    )
"""

conn.execute(CREATE_QUERY)

conn.execute("""INSERT INTO users (user_id, username, chat_id) VALUES (1, 'Basil', 123);""")

conn.commit()
