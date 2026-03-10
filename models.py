from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(50), nullable=False, default='Volunteer') # Roles: Administrator, Inventory Manager, Volunteer
    skills = db.Column(db.Text, nullable=True)
    availability = db.Column(db.String(50), nullable=True)
    location = db.Column(db.String(100), nullable=True)
    average_rating = db.Column(db.Float, default=0.0)
    status = db.Column(db.String(50), nullable=False, default='Active') # Overall Volunteer Status: Active, Training Pending

    assignments = db.relationship('Assignment', backref='volunteer', lazy=True)
    ratings = db.relationship('Rating', backref='volunteer', lazy=True)
    training_status = db.relationship('TrainingStatus', backref='user', lazy=True)
    resource_requests = db.relationship('ResourceRequest', backref='volunteer', lazy=True)

class TrainingStatus(db.Model):

    __tablename__ = 'training_status'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.String(50), nullable=False, default='Pending') # Status: Pending, Completed
    completion_date = db.Column(db.DateTime, nullable=True)

class Disaster(db.Model):
    __tablename__ = 'disasters'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    location = db.Column(db.String(150), nullable=False)
    severity = db.Column(db.String(50), nullable=False) # e.g., Low, Medium, High, Critical
    required_skills = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(50), nullable=False, default='Active') # Status: Active, Resolved
    created_date = db.Column(db.DateTime, default=datetime.utcnow)

    assignments = db.relationship('Assignment', backref='disaster', lazy=True)
    resources = db.relationship('ResourceAllocation', backref='disaster', lazy=True)
    resource_requests = db.relationship('ResourceRequest', backref='disaster', lazy=True)

class Resource(db.Model):
    __tablename__ = 'resources'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False) # e.g., Food, Medical, Shelter, Tools
    quantity = db.Column(db.Integer, nullable=False, default=0)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    requests = db.relationship('ResourceRequest', backref='resource', lazy=True)

class ResourceAllocation(db.Model):
    __tablename__ = 'resource_allocations'
    id = db.Column(db.Integer, primary_key=True)
    resource_id = db.Column(db.Integer, db.ForeignKey('resources.id'), nullable=False)
    disaster_id = db.Column(db.Integer, db.ForeignKey('disasters.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    allocated_date = db.Column(db.DateTime, default=datetime.utcnow)

    resource = db.relationship('Resource', backref='allocations')

class Assignment(db.Model):
    __tablename__ = 'assignments'
    id = db.Column(db.Integer, primary_key=True)
    volunteer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    disaster_id = db.Column(db.Integer, db.ForeignKey('disasters.id'), nullable=False)
    status = db.Column(db.String(50), nullable=False, default='Assigned') # Assigned, Completed, Cancelled
    assigned_date = db.Column(db.DateTime, default=datetime.utcnow)
    completion_date = db.Column(db.DateTime, nullable=True)

class Rating(db.Model):
    __tablename__ = 'ratings'
    id = db.Column(db.Integer, primary_key=True)
    volunteer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    disaster_id = db.Column(db.Integer, db.ForeignKey('disasters.id'), nullable=False)
    rating_score = db.Column(db.Integer, nullable=False) # 1-5 scale
    remarks = db.Column(db.Text, nullable=True)
    rated_date = db.Column(db.DateTime, default=datetime.utcnow)

class ResourceRequest(db.Model):
    __tablename__ = 'resource_requests'
    id = db.Column(db.Integer, primary_key=True)
    volunteer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    disaster_id = db.Column(db.Integer, db.ForeignKey('disasters.id'), nullable=False)
    resource_id = db.Column(db.Integer, db.ForeignKey('resources.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(50), nullable=False, default='Pending') # Pending, Approved, Rejected
    request_date = db.Column(db.DateTime, default=datetime.utcnow)
