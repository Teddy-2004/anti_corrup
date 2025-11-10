from flask import Flask
from extensions import db, migrate, login_manager
from config import Config
import os

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Ensure upload folder exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'admin.login'
    
    # IMPORTANT: Import models BEFORE blueprints to register user_loader
    import models
    
    # Register blueprints
    from routes.citizen import citizen_bp
    from routes.admin import admin_bp
    
    app.register_blueprint(citizen_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    
    return app

if __name__ == '__main__':
    app = create_app()
    
    if os.environ.get('FLASK_ENV') == 'development':
        print("🚀 Starting Anti-Corruption Platform on http://localhost:5000")
        print("👤 Admin login: http://localhost:5000/admin/login")
        print("📝 Default credentials - Username: admin | Password: admin123")
    
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)