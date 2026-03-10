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
        # Check if the column exists first
        c.execute("PRAGMA table_info(assignments)")
        columns = [row[1] for row in c.fetchall()]
        
        if 'task_description' not in columns:
            print("Adding 'task_description' column to 'assignments' table...")
            c.execute("ALTER TABLE assignments ADD COLUMN task_description TEXT")
            conn.commit()
            print("Migration completed successfully.")
        else:
            print("'task_description' column already exists in 'assignments' table.")
            
    except Exception as e:
        conn.rollback()
        print(f"Error during migration: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    migrate()
