from database import init_db, add_subscriber

init_db()  # creates table if missing

add_subscriber("khushitiwari0206@gmail.com")

print("User added")