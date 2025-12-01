import sqlite3

conn = sqlite3.connect("movies.db", check_same_thread=False)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS watchlist (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    movie_id INTEGER,
    movie_title TEXT,
    poster_url TEXT
)
""")

conn.commit()


def register_user(username, password):
    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        return True
    except:
        return False

def login_user(username, password):
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    row = c.fetchone()
    if row:
        return {"id": row[0], "username": row[1], "password": row[2]}
    return None

def change_username(user_id, new_username):
    try:
        c.execute("UPDATE users SET username=? WHERE id=?", (new_username, user_id))
        conn.commit()
        return True
    except:
        return False

def change_password(user_id, new_password):
    try:
        c.execute("UPDATE users SET password=? WHERE id=?", (new_password, user_id))
        conn.commit()
        return True
    except:
        return False

def add_watchlist(user_id, movie_id, title, poster_url):
    c.execute("""
        INSERT INTO watchlist (user_id, movie_id, movie_title, poster_url)
        VALUES (?, ?, ?, ?)
    """, (user_id, movie_id, title, poster_url))
    conn.commit()


def get_watchlist(user_id):
    c.execute("SELECT id, movie_title, poster_url FROM watchlist WHERE user_id=?", (user_id,))
    return c.fetchall()


def delete_watchlist(item_id):
    c.execute("DELETE FROM watchlist WHERE id=?", (item_id,))
    conn.commit()
