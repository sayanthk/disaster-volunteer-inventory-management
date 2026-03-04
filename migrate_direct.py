import sqlite3
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(BASE_DIR, 'app.db')
print(f"Targeting active database file at: {db_path}")

conn = sqlite3.connect(db_path, timeout=10) # 10s timeout to bypass minor locks
c = conn.cursor()

try:
    c.execute("ALTER TABLE users ADD COLUMN status VARCHAR(50) DEFAULT 'Active' NOT NULL")
    conn.commit()
    print("Successfully added 'status' column to users table.")
except Exception as e:
    print(f"Notice (status column): {e}")

try:
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
    print("Successfully created 'training_status' table.")
except Exception as e:
    print(f"Error creating training_status: {e}")

# verify users schema
c.execute("PRAGMA table_info(users)")
cols = [col[1] for col in c.fetchall()]
print(f"Current columns in users table: {cols}")

conn.close()
