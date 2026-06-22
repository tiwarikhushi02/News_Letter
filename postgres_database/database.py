import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()


def get_connection():
    return psycopg2.connect(
        os.getenv("DATABASE_URL")
    )


def init_db():
    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS subscribers(
            id SERIAL PRIMARY KEY,
            email VARCHAR(255) UNIQUE NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def add_subscriber(email):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO subscribers(email) VALUES(%s)",
            (email,)
        )

        conn.commit()
        return True

    except Exception:
        return False

    finally:
        conn.close()


def get_subscribers():
    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM subscribers"
    )

    users = cursor.fetchall()

    conn.close()

    return users


def remove_subscriber(email):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM subscribers WHERE email = %s",
        (email,)
    )

    success = cursor.rowcount

    conn.commit()
    conn.close()

    return success > 0












