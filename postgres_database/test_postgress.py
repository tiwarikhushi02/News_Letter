import database

conn = database.get_connection()
cursor = conn.cursor()

# Show all tables
cursor.execute("""
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public';
""")

print("Tables:")
print(cursor.fetchall())

# Show all columns of subscribers table
cursor.execute("""
SELECT column_name
FROM information_schema.columns
WHERE table_name = 'subscribers';
""")

print("\nSubscribers Table Columns:")
print(cursor.fetchall())

# Show subscribers
print("\nSubscribers:")
print(database.get_subscribers())

conn.close()