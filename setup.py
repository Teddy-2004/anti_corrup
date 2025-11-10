#!/usr/bin/env python
"""
Setup script for Anti-Corruption Reporting Platform
Run this script to initialize the database and create necessary directories
"""

import os
import sys
from app import create_app, db
from models import Admin

def setup_directories():
    """Create necessary directories"""
    print("📁 Creating directories...")
    
    directories = [
        'static/uploads',
        'static/css',
        'static/js'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"   ✓ Created {directory}")

def init_database():
    """Initialize database and create tables"""
    print("\n🗄️  Initializing database...")
    
    app = create_app()
    
    with app.app_context():
        try:
            # Create all tables
            db.create_all()
            print("   ✓ Database tables created")
            
            # Check if admin exists
            admin_exists = Admin.query.filter_by(username='admin').first()
            
            if not admin_exists:
                # Create default admin
                admin = Admin(username='admin', email='admin@example.com')
                admin.set_password('admin123')
                db.session.add(admin)
                db.session.commit()
                print("   ✓ Default admin user created")
                print("      Username: admin")
                print("      Password: admin123")
                print("      ⚠️  IMPORTANT: Change this password after first login!")
            else:
                print("   ℹ️  Admin user already exists")
            
            return True
            
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
            return False

def verify_setup():
    """Verify that setup was successful"""
    print("\n✅ Verifying setup...")
    
    checks = {
        'uploads directory': os.path.exists('static/uploads'),
        'config file': os.path.exists('config.py'),
        'models file': os.path.exists('models.py'),
        'app file': os.path.exists('app.py'),
        'templates directory': os.path.exists('templates'),
        'routes directory': os.path.exists('routes')
    }
    
    all_passed = True
    for check, passed in checks.items():
        status = "✓" if passed else "❌"
        print(f"   {status} {check}")
        if not passed:
            all_passed = False
    
    return all_passed

def print_instructions():
    """Print post-setup instructions"""
    print("\n" + "="*60)
    print("🎉 Setup Complete!")
    print("="*60)
    print("\nNext Steps:")
    print("1. Start the application:")
    print("   python app.py")
    print("\n2. Open your browser and visit:")
    print("   http://localhost:5000")
    print("\n3. Login to admin panel:")
    print("   http://localhost:5000/admin/login")
    print("   Username: admin")
    print("   Password: admin123")
    print("\n4. ⚠️  IMPORTANT: Change the default password immediately!")
    print("\n5. Submit a test report to verify everything works")
    print("="*60)

def main():
    """Main setup function"""
    print("="*60)
    print("Anti-Corruption Reporting Platform - Setup")
    print("="*60)
    
    # Check Python version
    if sys.version_info < (3, 10):
        print("❌ Error: Python 3.10 or higher is required")
        print(f"   Current version: {sys.version}")
        sys.exit(1)
    
    print(f"✓ Python version: {sys.version.split()[0]}")
    
    # Setup directories
    setup_directories()
    
    # Initialize database
    db_success = init_database()
    
    if not db_success:
        print("\n❌ Database setup failed!")
        print("Please check:")
        print("1. PostgreSQL is installed and running")
        print("2. Database 'anticorruption_db' exists")
        print("3. Connection string in config.py is correct")
        sys.exit(1)
    
    # Verify setup
    if not verify_setup():
        print("\n⚠️  Some files are missing. Please check your installation.")
        sys.exit(1)
    
    # Print instructions
    print_instructions()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Setup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
        print("Please check the README.md for manual setup instructions")
        sys.exit(1)