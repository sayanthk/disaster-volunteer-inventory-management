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
        # 1. Add 'status' column to 'users' table if it doesn't exist
        c.execute("PRAGMA table_info(users)")
        columns = [row[1] for row in c.fetchall()]
        if 'status' not in columns:
            print("Adding 'status' column to 'users' table...")
            c.execute("ALTER TABLE users ADD COLUMN status VARCHAR(50) DEFAULT 'Active' NOT NULL")
        else:
            print("'status' column already exists in 'users' table.")

        # 2. Create 'training_status' table if it doesn't exist
        print("Creating 'training_status' table if it doesn't exist...")
        c.execute("""
            CREATE TABLE IF NOT EXISTS training_status (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                status VARCHAR(50) NOT NULL DEFAULT 'Pending',
                completion_date DATETIME,
                FOREIGN KEY (user_id) REFERENCES users (id)
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
