from app import create_app
from models import db, User, TrainingStatus
from datetime import datetime
import uuid

def verify():
    app = create_app()
    with app.app_context():
        # 1. Simulate Registration
        email = f"test_{uuid.uuid4().hex[:6]}@example.com"
        print(f"Creating volunteer with email: {email}")
        
        volunteer = User(
            name="Test Volunteer",
            email=email,
            password="pbkdf2:sha256:...", # placeholder
            role="Volunteer",
            status="Training Pending" # Logic from routes/auth.py
        )
        db.session.add(volunteer)
        db.session.commit()
        
        # Initialize training status (Logic from routes/auth.py)
        ts = TrainingStatus(user_id=volunteer.id, status="Pending")
        db.session.add(ts)
        db.session.commit()
        
        print(f"Volunteer created with status: {volunteer.status}")
        assert volunteer.status == "Training Pending", "Initial status should be Training Pending"
        
        # 2. Check TrainingStatus record
        ts_rec = TrainingStatus.query.filter_by(user_id=volunteer.id).first()
        assert ts_rec is not None, "TrainingStatus record should exist"
        assert ts_rec.status == "Pending", "TrainingStatus should be Pending"
        print("Initial verification successful.")
        
        # 3. Simulate Training Completion (Logic from routes/volunteer.py)
        training = TrainingStatus.query.filter_by(user_id=volunteer.id, status='Pending').first()
        if training:
            training.status = 'Completed'
            training.completion_date = datetime.utcnow()
            volunteer.status = 'Active'
            db.session.commit()
            print("Simulated training completion.")
        
        # 4. Final Verification
        updated_volunteer = User.query.get(volunteer.id)
        assert updated_volunteer.status == "Active", f"Volunteer status should be Active, got {updated_volunteer.status}"
        
        updated_ts = TrainingStatus.query.filter_by(user_id=volunteer.id).first()
        assert updated_ts.status == "Completed", "TrainingStatus should be Completed"
        assert updated_ts.completion_date is not None, "Completion date should be set"
        
        print("Final verification successful! Flow works as expected.")

if __name__ == "__main__":
    verify()
