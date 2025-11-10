from extensions import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


# ==============================
# Admin Model
# ==============================
class Admin(UserMixin, db.Model):
    __tablename__ = 'admins'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(120), unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        """Hashes and stores the password."""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verifies the provided password against the stored hash."""
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<Admin {self.username}>'


@login_manager.user_loader
def load_user(user_id):
    """Flask-Login user loader."""
    return Admin.query.get(int(user_id))


# ==============================
# Report Model
# ==============================
class Report(db.Model):
    __tablename__ = 'reports'
    
    id = db.Column(db.Integer, primary_key=True)
    report_id = db.Column(db.String(50), unique=True, nullable=False)  # Increased from 20 → 50
    corruption_type = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(255))
    status = db.Column(db.String(30), default='Pending')  # Increased from 20 → 30 (future-proof)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship to Evidence
    evidence = db.relationship('Evidence', backref='report', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Report {self.report_id}>'


# ==============================
# Evidence Model
# ==============================
class Evidence(db.Model):
    __tablename__ = 'evidence'
    
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    original_filename = db.Column(db.String(255), nullable=False)
    file_type = db.Column(db.String(50))
    file_size = db.Column(db.Integer)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    report_id = db.Column(db.Integer, db.ForeignKey('reports.id'), nullable=False)
    
    def __repr__(self):
        return f'<Evidence {self.original_filename}>'
