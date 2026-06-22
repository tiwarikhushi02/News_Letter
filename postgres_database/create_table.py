import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(
    os.getenv("DATABASE_URL")
)

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS subscribers(
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL
)
""")

conn.commit()
conn.close()

print("✅ Table Created Successfully")