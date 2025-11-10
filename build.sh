#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Only initialize Alembic if migrations folder doesn’t exist
if [ ! -d "migrations" ]; then
    echo "Initializing Alembic..."
    flask db init
fi

# Upgrade database to latest version
echo "Upgrading database..."
flask db upgrade || echo "⚠️ Database already up to date or revision mismatch."

# Create uploads directory
mkdir -p static/uploads

# Create default admin user
python3 << END
from app import create_app
from extensions import db
from models import Admin

app = create_app()

with app.app_context():
    db.create_all()
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
