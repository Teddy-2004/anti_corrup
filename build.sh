#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Initialize Flask-Migrate if migrations folder doesn't exist
if [ ! -d "migrations" ]; then
    flask db init
fi

# Create initial migration if none exist
flask db migrate -m "Initial migration" || echo "Migration already exists or no changes detected"

# Run database migrations
flask db upgrade

# Create uploads directory
mkdir -p static/uploads

# Create default admin user
python3 << END
from app import create_app
from extensions import db
from models import Admin

app = create_app()

with app.app_context():
    # Create tables
    db.create_all()
    
    # Create admin if doesn't exist
    admin = Admin.query.filter_by(username='admin').first()
    if not admin:
        admin = Admin(username='admin', email='admin@example.com')
        admin.set_password('ChangeThisPassword123!')
        db.session.add(admin)
        db.session.commit()
        print("✅ Admin user created!")
    else:
        print("✅ Admin user already exists")
END