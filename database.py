import sqlite3

def init_db():
    conn = sqlite3.connect("subscribers.db")

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS subscribers(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def add_subscriber(email):
    conn = sqlite3.connect("subscribers.db")
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO subscribers(email) VALUES(?)",
            (email,)
        )

        conn.commit()
        return True

    except sqlite3.IntegrityError:
        return False

    finally:
        conn.close()


def get_subscribers():
    conn = sqlite3.connect("subscribers.db")

    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM subscribers"
    )

    users = cursor.fetchall()

    conn.close()

    return users