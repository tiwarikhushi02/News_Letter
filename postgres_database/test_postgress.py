import psycopg2
import os
from dotenv import load_dotenv
import database
from postgres_database.database import get_subscribers

print(get_subscribers())

load_dotenv()

conn = psycopg2.connect(os.getenv("DATABASE_URL"))

cursor = conn.cursor()

cursor.execute("""
SELECT table_name
FROM information_schema.tables
WHERE table_schema='public';
""")

print(cursor.fetchall())

import database

result = database.add_subscriber(
    "test@gmail.com"
)

print(result)
print(
    database.get_subscribers()
)

conn.close()