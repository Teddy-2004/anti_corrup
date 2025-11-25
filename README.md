Anti-Corruption Reporting Platform

A secure, web-based platform for anonymous corruption reporting with a powerful admin dashboard for case management.

Live Demo: Homepage
 | Admin Dashboard

Contact: t.godebo@alustudent.com

Overview

The platform allows citizens to report corruption anonymously, track their reports, and provides administrators with tools to manage cases efficiently.

Key Features:

Citizen Portal

Anonymous report submission (no login required)

Multiple corruption categories

Upload evidence (images/PDFs, up to 16MB)

Unique report ID for tracking

Edit/update reports while pending

Light/Dark mode with persistence

Fully responsive design

Admin Dashboard

Secure login with hashed passwords

Real-time statistics and report management

Advanced filtering (status, type, date range)

Pagination for large datasets

Evidence viewing and CSV export

Hidden from public navigation for security

Security

Full anonymity (no personal data collected)

Passwords hashed with PBKDF2-SHA256

SQL injection protection via SQLAlchemy

XSS protection with Jinja2 auto-escaping

File validation and sanitization

CSRF protection and secure sessions

Technology Stack

Backend: Python 3.12, Flask, Flask-SQLAlchemy, PostgreSQL, Gunicorn
Frontend: Jinja2 templates, Bootstrap 5, Font Awesome, Custom CSS + Vanilla JS
Database: PostgreSQL (admins, reports, evidence)
Deployment: Render Cloud (PostgreSQL + Web Service)

Quick Start
Prerequisites

Python 3.10+

PostgreSQL 12+

pip

Git

Installation
# Clone the repository
git clone https://github.com/Anti-Corruption/anti-corruption-platform.git
cd anti-corruption-platform

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate    # Windows

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

Database Setup
# Start PostgreSQL
sudo systemctl start postgresql  # Linux
# Create database and user
psql -U postgres
CREATE DATABASE anticorruption_db;
CREATE USER anticorruption_user WITH PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE anticorruption_db TO anticorruption_user;
\q

Configuration

Update config.py:

SQLALCHEMY_DATABASE_URI = 'postgresql://anticorruption_user:your_secure_password@localhost/anticorruption_db'

Run Locally
# Initialize database tables and admin user
python3 create_admin.py

# Start the application
python3 app.py


Access the app: http://localhost:5000

Deployment to Render

Push project to GitHub

Create PostgreSQL service on Render

Create Web Service (Python runtime, gunicorn app:app)

Add environment variables: DATABASE_URL, SECRET_KEY, FLASK_ENV=production

Deploy and access live site

Usage Guide
For Citizens

Submit a report on the homepage

Track reports using the unique Report ID

Edit pending reports and manage evidence

For Admins

Login to the admin dashboard (password-protected)

View, filter, and manage reports

Download evidence and export report data to CSV

Change default password immediately after first login

Security Best Practices

Keep all passwords and SECRET_KEY in environment variables

Validate uploaded files and enforce size/type restrictions

Do not expose admin credentials publicly

Use HTTPS in production

Project Structure
anti-corruption-platform/
├── app.py
├── config.py
├── models.py
├── create_admin.py
├── requirements.txt
├── routes/
├── templates/
├── static/
└── venv/

License

MIT License © 2025 Tedla Tesfaye
