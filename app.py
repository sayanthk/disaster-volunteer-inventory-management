from flask import Flask
from config import Config
from models import db, User
from flask_login import LoginManager

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Import and register blueprints
    from routes.auth import auth_bp
    from routes.main import main_bp
    from routes.disaster import disaster_bp
    from routes.resource import resource_bp
    from routes.assignment import assignment_bp
    from routes.volunteer import volunteer_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(disaster_bp)
    app.register_blueprint(resource_bp)
    app.register_blueprint(assignment_bp)
    app.register_blueprint(volunteer_bp)

    with app.app_context():
        db.create_all()
        # Ensure migration for existing databases (e.g. Render deployments)
        try:
            from sqlalchemy import text
            db.session.execute(text("ALTER TABLE users ADD COLUMN status VARCHAR(50) DEFAULT 'Active' NOT NULL"))
            db.session.commit()
        except Exception:
            db.session.rollback() # Ignore if column already exists

        # Ensure migration for assignments table (e.g. Render deployments)
        try:
            db.session.execute(text("ALTER TABLE assignments ADD COLUMN task_description TEXT"))
            db.session.commit()
        except Exception:
            db.session.rollback() # Ignore if column already exists

        try:
            db.session.execute(text("ALTER TABLE assignments ADD COLUMN completion_date TIMESTAMP"))
            db.session.commit()
        except Exception:
            db.session.rollback() # Ignore if column already exists

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
