import sqlite3
import os

db_path = 'app.db'

def migrate():
    if not os.path.exists(db_path):
        print(f"Database {db_path} not found.")
        return

    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    try:
        print("Creating 'resource_requests' table if it doesn't exist...")
        c.execute("""
            CREATE TABLE IF NOT EXISTS resource_requests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                volunteer_id INTEGER NOT NULL,
                disaster_id INTEGER NOT NULL,
                resource_id INTEGER NOT NULL,
                quantity INTEGER NOT NULL,
                status VARCHAR(50) NOT NULL DEFAULT 'Pending',
                request_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (volunteer_id) REFERENCES users (id),
                FOREIGN KEY (disaster_id) REFERENCES disasters (id),
                FOREIGN KEY (resource_id) REFERENCES resources (id)
            )
        """)

        conn.commit()
        print("Migration completed successfully.")
    except Exception as e:
        conn.rollback()
        print(f"Error during migration: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    migrate()
