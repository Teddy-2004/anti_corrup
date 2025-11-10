from app import create_app, db
from models import Admin

app = create_app()

with app.app_context():
    # Create all tables
    db.create_all()
    print("✓ Database tables created")
    
    # Create default admin if not exists
    admin = Admin.query.filter_by(username='admin').first()
    if not admin:
        admin = Admin(username='admin')
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        print("✓ Default admin created (username: admin, password: admin123)")
    else:
        print("✓ Admin already exists")
    
    print("\n✅ Database initialized successfully!")