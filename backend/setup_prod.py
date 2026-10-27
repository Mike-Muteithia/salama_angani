from app import app
from extensions import db
from models import User
from werkzeug.security import generate_password_hash
from flask_migrate import upgrade

with app.app_context():
    # 1. Wipe the legacy database schema completely
    db.reflect()
    db.drop_all()
    
    # 2. Run the Alembic migrations to build the new tables (including users)
    upgrade()
    
    # 3. Seed the production admin account so you can access the Provider Dashboard
    if not User.query.filter_by(email='admin@salama.com').first():
        provider = User(
            email='admin@salama.com', 
            password_hash=generate_password_hash('admin123'), 
            role='provider'
        )
        db.session.add(provider)
        db.session.commit()
        print("Production database reset, migrated, and seeded successfully!")