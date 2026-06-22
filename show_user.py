from postgres_database.database import (
    init_db,
    add_subscriber,
    get_subscribers
)

init_db()
print(get_subscribers())