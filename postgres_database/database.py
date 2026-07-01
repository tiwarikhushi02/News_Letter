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

def save_otp(email, otp):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO pending_verifications(email, otp)
        VALUES(%s, %s)
        ON CONFLICT(email)
        DO UPDATE SET
            otp = EXCLUDED.otp,
            created_at = CURRENT_TIMESTAMP
    """, (email, otp))

    conn.commit()
    conn.close()

def verify_otp(email, otp):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM pending_verifications
        WHERE email = %s
        AND otp = %s
        AND created_at >= NOW() - INTERVAL '5 minutes'
    """, (email, otp))

    user = cursor.fetchone()

    conn.close()

    return user
    
def delete_pending_verification(email):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM pending_verifications WHERE email = %s",
        (email,)
    )

    conn.commit()
    conn.close()

def subscriber_exists(email):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM subscribers WHERE email = %s",
        (email,)
    )

    user = cursor.fetchone()

    conn.close()

    return user is not None    


def get_total_subscribers():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM subscribers"
    )

    total = cursor.fetchone()[0]

    conn.close()

    return total

def get_total_pending():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM pending_verifications"
    )

    total = cursor.fetchone()[0]

    conn.close()

    return total

def get_latest_subscribers():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT email, subscribed_at
        FROM subscribers
        ORDER BY subscribed_at DESC
        LIMIT 5
    """)

    users = cursor.fetchall()

    conn.close()

    return users

def search_subscriber(email):
    
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT email, subscribed_at
        FROM subscribers
        WHERE email = %s
    """, (email,))

    user = cursor.fetchone()

    conn.close()

    return user

def admin_remove_subscriber(email):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM subscribers
        WHERE email = %s
    """, (email,))

    deleted = cursor.rowcount

    conn.commit()
    conn.close()

    return deleted > 0












