Anti-Corruption Reporting Platform - Complete Setup Guide
A comprehensive web-based platform for anonymous corruption reporting with a secure admin dashboard for case management.
**Table of Contents:
**
Overview
Features
System Requirements
Installation Guide
Configuration
Running Locally
Deployment to Render
Usage Guide
Troubleshooting
Project Structure
Technology Stack


Overview
The Anti-Corruption Reporting Platform enables citizens to report corruption cases anonymously and securely. It includes:

Public Portal: Anonymous report submission with evidence upload
Report Tracking: Citizens can track their reports by unique ID
Admin Dashboard: Comprehensive tools for reviewing and managing reports
Dark Mode: Full light/dark theme support with localStorage persistence
Responsive Design: Works seamlessly on desktop, tablet, and mobile devices


Features
Citizen Features ✅

Anonymous corruption reporting (no login required)
Multiple corruption type categories
File upload for evidence (images and PDFs, up to 16MB)
Unique Report ID generation for tracking
Track reports by Report ID
Edit/update reports (only if status is "Pending")
Add/remove evidence files
View report timeline
Light/Dark mode toggle

Admin Features ✅

Secure admin login with password hashing
Dashboard with real-time statistics
Advanced filtering (by status, type, date range)
Pagination for large datasets
Report status management workflow
Evidence viewing and downloading
CSV export functionality
Report deletion with confirmation
Hidden from public navigation (security)

Security Features ✅

Complete anonymity (no personal data collection)
Werkzeug password hashing (PBKDF2-SHA256)
SQL injection prevention (SQLAlchemy ORM)
XSS protection (Jinja2 auto-escaping)
File upload validation and sanitization
Secure session management
CSRF protection


System Requirements
Minimum Requirements
ComponentVersionPurposePython3.10+Backend runtimePostgreSQL12+DatabasepipLatestPython package managerGitLatestVersion control
Operating Systems

✅ Linux (Ubuntu 20.04+, Debian 11+)
✅ macOS (10.14+)
✅ Windows (WSL2 recommended)

Browser Support

✅ Chrome 120+
✅ Firefox 121+
✅ Safari 17+
✅ Edge 120+
✅ Mobile browsers (iOS Safari, Chrome Mobile)


Installation Guide
Step 1: Install System Dependencies
On Ubuntu/Debian:
bash# Update package manager
sudo apt update
sudo apt upgrade -y

# Install Python and pip
sudo apt install python3 python3-pip python3-venv -y

# Install PostgreSQL
sudo apt install postgresql postgresql-contrib -y

# Install Git (if not already installed)
sudo apt install git -y
On macOS:
bash# Install Homebrew (if not already installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python
brew install python3

# Install PostgreSQL
brew install postgresql

# Install Git (if not already installed)
brew install git
On Windows (WSL2):
bash# Install WSL2 first, then follow Ubuntu/Debian steps above
Step 2: Start PostgreSQL Service
On Linux:
bash# Start PostgreSQL
sudo systemctl start postgresql

# Enable auto-start on boot (optional)
sudo systemctl enable postgresql

# Verify it's running
sudo systemctl status postgresql
```

You should see:
```
● postgresql.service - PostgreSQL RDBMS
     Loaded: loaded (...; enabled; preset: enabled)
     Active: active (running)
On macOS:
bash# Start PostgreSQL
brew services start postgresql

# Verify it's running
brew services list
Step 3: Create PostgreSQL Database
bash# Access PostgreSQL
sudo -u postgres psql

# In the PostgreSQL prompt (postgres=#), run:
CREATE DATABASE anticorruption_db;

# Create a dedicated user (recommended)
CREATE USER anticorruption_user WITH PASSWORD 'Tedi1667';

# Grant privileges
GRANT ALL PRIVILEGES ON DATABASE anticorruption_db TO anticorruption_user;

# Exit PostgreSQL
\q
Verify it worked:
bashpsql -U postgres -h localhost -d anticorruption_db
# Enter password when prompted
# If you can connect, type \q to exit
Step 4: Clone the Project
bash# Create a projects directory (optional)
mkdir ~/projects
cd ~/projects

# Clone the repository (or extract if you have a ZIP file)
git clone https://github.com/YOUR_USERNAME/anti-corruption-platform.git
cd anti-corruption-platform

# Or if you downloaded as ZIP:
# unzip anti-corruption-platform.zip
# cd anti-corruption-platform
Step 5: Create Virtual Environment
bash# Navigate to project directory (if not already there)
cd ~/projects/anti-corruption-platform

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On Linux/macOS:
source venv/bin/activate

# On Windows:
# venv\Scripts\activate

# Verify activation (you should see (venv) at the start of your terminal line)
Step 6: Install Python Dependencies
bash# Make sure you're in the virtual environment
# (you should see (venv) in your terminal)

# Install all required packages
pip install --upgrade pip
pip install -r requirements.txt

# Verify installation
pip list
You should see all these packages:

Flask
Flask-SQLAlchemy
Flask-Migrate
Flask-Login
psycopg2-binary
Werkzeug
python-dotenv
gunicorn

Step 7: Create Project Directories
bash# Create uploads directory for evidence files
mkdir -p static/uploads
mkdir -p static/css
mkdir -p static/js

# Verify they were created
ls -la static/

Configuration
Step 1: Update Database Connection
bash# Edit the configuration file
nano config.py
Find this line (around line 11):
pythonSQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    'postgresql://postgres:Tedi1667@localhost/anticorruption_db'
Update it with:

Username: postgres (or your custom user)
Password: Tedi1667 (your actual password)
Host: localhost
Port: 5432 (default)
Database: anticorruption_db

Example with custom user:
pythonSQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    'postgresql://anticorruption_user:Tedi1667@localhost/anticorruption_db'
Save with Ctrl+X, then Y, then Enter.
Step 2: Create CSS and JS Files
Make sure these files exist:
bash# Check if files exist
ls -la static/css/style.css
ls -la static/js/theme.js

# If they don't exist, you can create them manually
# But they should be included in the project
If files are missing, check the earlier sections where we created them.

Running Locally
Step 1: Initialize the Database
bash# Make sure virtual environment is activated
source venv/bin/activate

# Set Flask app
export FLASK_APP=app.py

# Create database tables and admin user
python3 create_admin.py
```

You should see:
```
✅ Database tables created
✅ Admin user created!
```

Or if admin already exists:
```
✅ Admin user already exists
Step 2: Start the Application
bash# Make sure virtual environment is activated
source venv/bin/activate

# Navigate to project directory
cd ~/projects/anti-corruption-platform

# Run the Flask app
python3 app.py
```

You should see:
```
🚀 Starting Anti-Corruption Platform on http://localhost:5000
👤 Admin login: http://localhost:5000/admin/login
📝 Default credentials - Username: admin | Password: ChangeThisPassword123!
Step 3: Access the Application
Open your web browser and visit:
Public Portal:

Homepage: http://localhost:5000
Submit Report: http://localhost:5000/report
Track Report: http://localhost:5000/track
About: http://localhost:5000/about

Admin Panel:

Login: http://localhost:5000/admin/login
Dashboard: http://localhost:5000/admin/dashboard (after login)

Step 4: Test the Application
Test as a Citizen:

Visit http://localhost:5000
Click "Submit a Report"
Fill in the form:

Type: Choose any (e.g., "Bribery")
Description: Type anything (e.g., "Test report")


Click "Submit Report"
Note the Report ID (e.g., ACR-20250119-ABCD1234)
Click "Track Report"
Enter the Report ID and verify you can see your report

Test as Admin:

Visit http://localhost:5000/admin/login
Login with:

Username: admin
Password: ChangeThisPassword123!


Verify the dashboard shows your test report
Click the 👁️ icon to view report details
Change status to "Reviewed" and save
Try the dark mode toggle (🌙 icon)

Step 5: Stop the Application
bash# In the terminal running the app, press:
Ctrl+C

# Deactivate virtual environment (optional)
deactivate

Deployment to Render
Prerequisite: Push to GitHub
bash# Initialize Git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - Anti-Corruption Platform"

# Create a repository on GitHub (via website)
# Then push your code:
git remote add origin https://github.com/YOUR_USERNAME/anti-corruption-platform.git
git branch -M main
git push -u origin main
```

### Step 1: Create Render Account

1. Go to https://render.com
2. Sign up with your GitHub account
3. Authorize Render to access your repositories

### Step 2: Create PostgreSQL Database on Render

1. From Render Dashboard, click **"New +"**
2. Select **"PostgreSQL"**
3. Fill in:
   - **Name:** `anticorruption-db`
   - **Database:** `anticorruption_db`
   - **User:** `anticorruption_user` (auto-generated)
   - **Region:** Choose closest to your users
   - **Plan:** Free tier or Starter
4. Click **"Create Database"**
5. Copy and save the **Internal Database URL**

Example:
```
postgresql://anticorruption_user:random_password@dpg-xxxxx-a.oregon-postgres.render.com/anticorruption_db
Step 3: Create Web Service on Render

From Render Dashboard, click "New +"
Select "Web Service"
Connect your GitHub repository
Fill in:

Name: anticorruption-platform
Region: Same as database
Branch: main
Runtime: Python 3
Build Command: ./build.sh
Start Command: gunicorn app:app



Step 4: Configure Environment Variables
In the Web Service settings, scroll to "Environment Variables" and add:
KeyValuePYTHON_VERSION3.12.0SECRET_KEY(Generate below)DATABASE_URL(From PostgreSQL service)FLASK_ENVproduction
Generate SECRET_KEY:
On your local computer:
bashpython3 -c "import secrets; print(secrets.token_hex(32))"
```

Copy the output and use it as the SECRET_KEY value.

### Step 5: Deploy

1. Click **"Create Web Service"**
2. Monitor the build in the Logs tab
3. Wait 5-10 minutes for deployment to complete

You should see:
```
✅ Build successful!
✅ Admin user created!
==> Your service is live 🎉
Step 6: Get Your Live URL
After successful deployment:

Go to your Render Dashboard
Click on your Web Service
Look for the URL at the top: https://anticorruption-platform-xxxx.onrender.com
Click on it to visit your live site

Step 7: Access Admin Panel in Production

Visit: https://your-app-url.onrender.com/admin/login
Login with:

Username: admin
Password: ChangeThisPassword123!



Step 8: Change Default Admin Password
Via Render Shell:

Go to Render Dashboard → Your Web Service
Click "Shell" tab
Run:

bashpython3
Then paste:
pythonfrom app import create_app
from extensions import db
from models import Admin

app = create_app()

with app.app_context():
    admin = Admin.query.filter_by(username='admin').first()
    admin.set_password('YOUR_NEW_SECURE_PASSWORD')
    db.session.commit()
    print("✅ Password changed!")
Press Ctrl+D to exit.

Usage Guide
For Citizens
How to Submit a Report:

Go to the homepage
Click "Submit a Report" button
Select corruption type from dropdown
Enter detailed description
(Optional) Add location
(Optional) Upload evidence files (images/PDFs)
Click "Submit Report"
Save your Report ID - you'll need it to track your report

How to Track Your Report:

Click "Track Report" in navigation
Enter your Report ID
View current status and details
If status is "Pending", you can edit the report
You can add more evidence or remove existing files

Supported Corruption Types:

Bribery
Embezzlement
Fraud
Extortion
Nepotism
Abuse of Power
Conflict of Interest
Money Laundering
Other

Evidence Requirements:

Formats: JPG, PNG, GIF, PDF
Max file size: 16MB per file
Multiple files supported

For Administrators
How to Login:

Go to /admin/login (not visible in public navigation)
Enter credentials:

Username: admin
Password: (the one you set)



How to Access Reports:

Dashboard shows all reports with statistics
Use filters to find specific reports:

Filter by Status (Pending/Reviewed/Resolved)
Filter by Type (corruption category)
Filter by Date Range


Click the 👁️ icon to view full report details

How to Manage Reports:

From report details page:

View full description
Download evidence files
Update report status
See timeline of changes



How to Export Data:

Click "Export to CSV" button
Optionally apply filters first
CSV file downloads with all report data
Open in Excel or Google Sheets

Default Admin Credentials:

Username: admin
Password: ChangeThisPassword123!
⚠️ CHANGE immediately after first login!


Troubleshooting
Database Connection Issues
Problem: psycopg2.OperationalError: connection to server failed
Solutions:

Check PostgreSQL is running:

bash   sudo systemctl status postgresql
   # If not running, start it:
   sudo systemctl start postgresql

Verify credentials in config.py:

python   SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:YOUR_PASSWORD@localhost/anticorruption_db'

Test connection:

bash   psql -U postgres -h localhost -d anticorruption_db
Virtual Environment Issues
Problem: command not found: python3
Solution: Make sure virtual environment is activated:
bashsource venv/bin/activate
# You should see (venv) in your terminal
Port Already in Use
Problem: OSError: [Errno 48] Address already in use
Solution:
bash# Find what's using port 5000
lsof -ti:5000

# Kill it (replace PID with the number from above)
kill -9 PID

# Or use a different port:
python3 app.py --port 5001
Static Files Not Loading
Problem: CSS and JavaScript not styling the page
Solution:

Hard refresh browser: Ctrl+Shift+R (or Cmd+Shift+R on Mac)
Check if files exist:

bash   ls -la static/css/style.css
   ls -la static/js/theme.js

Verify in browser: Go to http://localhost:5000/static/css/style.css

If you see CSS code → file is loading
If 404 error → file doesn't exist



Admin Login Not Working
Problem: "Invalid username or password"
Solution:

Create admin user:

bash   python3 create_admin.py

Default credentials:

Username: admin
Password: ChangeThisPassword123!


Reset password:

bash   python3
   >>> from app import create_app
   >>> from extensions import db
   >>> from models import Admin
   >>> app = create_app()
   >>> with app.app_context():
   ...     admin = Admin.query.filter_by(username='admin').first()
   ...     admin.set_password('newpassword')
   ...     db.session.commit()
   >>> exit()
File Upload Not Working
Problem: Can't upload evidence files
Solutions:

Check directory exists:

bash   mkdir -p static/uploads
   chmod 755 static/uploads

Check file size: Max 16MB per file
Check file type: Only JPG, PNG, GIF, PDF supported

Dark Mode Not Working
Problem: Dark mode toggle not responding
Solution:

Hard refresh: Ctrl+Shift+R
Check CSS file:

bash   ls -la static/css/style.css
```

3. **Check browser console:** Press `F12` and look for errors

---

## Project Structure
```
anti-corruption-platform/
│
├── app.py                      # Main Flask application
├── extensions.py               # Flask extensions (db, migrate, login_manager)
├── config.py                   # Configuration settings
├── models.py                   # Database models
├── create_admin.py             # Admin user creation script
├── build.sh                    # Render build script
├── requirements.txt            # Python dependencies
├── README.md                   # This file
│
├── routes/
│   ├── __init__.py
│   ├── citizen.py             # Public routes (report submission, tracking)
│   └── admin.py               # Admin routes (dashboard, management)
│
├── templates/
│   ├── base.html              # Base template with navigation
│   ├── citizen/
│   │   ├── index.html         # Homepage
│   │   ├── report_form.html   # Report submission form
│   │   ├── success.html       # Success confirmation page
│   │   ├── track_report.html  # Report tracking page
│   │   ├── manage_report.html # Report management page
│   │   └── about.html         # About/FAQ page
│   └── admin/
│       ├── login.html         # Admin login page
│       ├── dashboard.html     # Admin dashboard
│       └── view_report.html   # Report detail view
│
├── static/
│   ├── css/
│   │   └── style.css          # Custom styles (includes dark mode)
│   ├── js/
│   │   └── theme.js           # Theme toggle functionality
│   └── uploads/               # Evidence file storage
│
└── venv/                      # Python virtual environment (auto-created)
```

---

## Technology Stack

### Backend
- **Framework:** Flask 3.0.0
- **Language:** Python 3.12
- **ORM:** SQLAlchemy with Flask-SQLAlchemy
- **Authentication:** Flask-Login
- **Database:** PostgreSQL 12+
- **Migration Tool:** Flask-Migrate
- **Server:** Gunicorn (production)

### Frontend
- **Template Engine:** Jinja2
- **CSS Framework:** Bootstrap 5.3.2
- **Icons:** Font Awesome 6.4.0
- **Styling:** Custom CSS with dark mode
- **JavaScript:** Vanilla (no jQuery)

### Database
- **PostgreSQL 12+**
- **3 Tables:** admins, reports, evidence
- **Relationships:** One-to-many (reports to evidence)

### Deployment
- **Platform:** Render Cloud
- **Database Hosting:** Render PostgreSQL
- **SSL/TLS:** Automatic HTTPS

### Development Tools
- **Version Control:** Git
- **Package Manager:** pip
- **Environment:** Virtual environment (venv)

---

## Security Information

### Passwords

**Default Admin Password:**
```
ChangeThisPassword123!
⚠️ MUST be changed immediately after first deployment!
Secure Password Requirements:

Minimum 12 characters
Mix of uppercase and lowercase
Numbers and special characters
No dictionary words

Environment Variables (Production)
Never commit these to Git:

DATABASE_URL
SECRET_KEY
Admin passwords

Use .env file (add to .gitignore):
bashFLASK_ENV=production
SECRET_KEY=your_secure_key_here
DATABASE_URL=postgresql://...
File Upload Security

Only whitelisted file types allowed (JPG, PNG, GIF, PDF)
Max file size: 16MB
Files stored outside web root
Admin-only download access

Authentication

Passwords hashed with PBKDF2-SHA256
Session timeout: 2 hours
Secure cookies
Login required for admin routes


Support & Resources
Documentation

Flask: https://flask.palletsprojects.com/
PostgreSQL: https://www.postgresql.org/docs/
Bootstrap: https://getbootstrap.com/docs/
SQLAlchemy: https://docs.sqlalchemy.org/

Troubleshooting Steps

Check all previous steps are completed
Verify credentials in config.py
Ensure PostgreSQL is running
Check virtual environment is activated
Look at Flask logs for error messages
Try hard refreshing browser (Ctrl+Shift+R)
Check browser console (F12) for JavaScript errors

Getting Help
If you encounter issues:

Check the Troubleshooting section above
Review the Installation Guide step-by-step
Check Flask logs (terminal output when running the app)
Verify all files exist in correct locations


Quick Reference
Start the App (Local)
bashcd ~/projects/anti-corruption-platform
source venv/bin/activate
python3 app.py
# Visit http://localhost:5000
Stop the App
bash# Press Ctrl+C in the terminal running the app
Ctrl+C
```

### Access Admin Panel
```
http://localhost:5000/admin/login
Username: admin
Password: ChangeThisPassword123!
Deactivate Virtual Environment
bashdeactivate
Update Code & Redeploy (Render)
bashgit add .
git commit -m "Update message"
git push origin main
# Render automatically redeploys

License & Attribution
This project is provided as-is for educational and development purposes.

Last Updated: January 19, 2025
Version: 1.0.0
Status: ✅ Production Ready
For questions or issues, refer to the troubleshooting section or check the code comments.RetryClaude can make mistakes. Please double-check responses.
