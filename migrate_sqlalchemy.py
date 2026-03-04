from app import create_app
from models import db
from sqlalchemy import text

def migrate():
    app = create_app()
    with app.app_context():
        # Add status column
        try:
            db.session.execute(text("ALTER TABLE users ADD COLUMN status VARCHAR(50) DEFAULT 'Active' NOT NULL"))
            db.session.commit()
            print("Successfully added 'status' column to 'users' table.")
        except Exception as e:
            db.session.rollback()
            print(f"Notice (status column): {e}")

        # Create training_status table
        try:
            db.session.execute(text("""
                CREATE TABLE IF NOT EXISTS training_status (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    status VARCHAR(50) NOT NULL DEFAULT 'Pending',
                    completion_date DATETIME,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            """))
            db.session.commit()
            print("Successfully created 'training_status' table.")
        except Exception as e:
            db.session.rollback()
            print(f"Error creating 'training_status': {e}")
            
        # Verify
        try:
            res = db.session.execute(text("SELECT status FROM users LIMIT 1")).fetchone()
            print("Verification successful: 'status' column is queryable.")
        except Exception as e:
            print("Verification failed:", e)

if __name__ == "__main__":
    migrate()
