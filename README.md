**Anti-Corruption Reporting Platform - Complete Setup Guide**

A comprehensive web-based platform for anonymous corruption reporting with a secure admin dashboard for case management.

**Overview**

The Anti-Corruption Reporting Platform enables citizens to report corruption cases anonymously and securely. It includes:

**Public Portal:** Anonymous report submission with evidence upload

**Report Tracking:** Citizens can track their reports by unique ID

**Admin Dashboard:** Comprehensive tools for reviewing and managing reports

**Dark Mode:** Full light/dark theme support with localStorage persistence

**Responsive Design:** Works seamlessly on desktop, tablet, and mobile devices


**Features**

**Citizen Features**

- Anonymous corruption reporting (no login required)

- Multiple corruption type categories

- File upload for evidence (images and PDFs, up to 16MB)

- Unique Report ID generation for tracking

- Track reports by Report ID

- Edit/update reports (only if status is "Pending")

- Add/remove evidence files

- View report timeline

- Light/Dark mode toggle

**Admin Features**

- Secure admin login with password hashing

- Dashboard with real-time statistics

- Advanced filtering (by status, type, date range)

- Pagination for large datasets

- Report status management workflow

- Evidence viewing and downloading

- CSV export functionality

- Report deletion with confirmation

- Hidden from public navigation (security)

**Security Features**

- Complete anonymity (no personal data collection)

- Werkzeug password hashing (PBKDF2-SHA256)

- SQL injection prevention (SQLAlchemy ORM)

- XSS protection (Jinja2 auto-escaping)

- File upload validation and sanitization

- Secure session management

- CSRF protection


**System Requirements**

**Minimum Requirements:**

- Linux (Ubuntu 20.04+, Debian 11+)

- macOS (10.14+)

- Windows (WSL2 recommended)

**Browser Support**

- Chrome 120+

- Firefox 121+

- Safari 17+

- Edge 120+

-Mobile browsers (iOS Safari, Chrome Mobile)


**Installation Guide**

**Step 1:** **Install System Dependencies**

**On Ubuntu/Debian:**

**Update package manager**

sudo apt update

sudo apt upgrade -y

# Install Python and pip
sudo apt install python3 

python3-pip 

python3-venv -y

# Install PostgreSQL
sudo apt install postgresql 

postgresql-contrib -y

# Install Git (if not already installed)
sudo apt install git -y

On macOS:

Install Homebrew (if not already installed)

/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python
brew install python3

# Install PostgreSQL
brew install postgresql

# Install Git (if not already installed)
brew install git

**On Windows (WSL2):**

Install WSL2 first, then follow Ubuntu/Debian steps above

Step 2: Start PostgreSQL Service

**On Linux:**
Start PostgreSQL

sudo systemctl start postgresql

# Enable auto-start on boot (optional)
sudo systemctl enable postgresql

# Verify it's running
sudo systemctl status postgresql
```

You should see:
● postgresql.service - PostgreSQL RDBMS
     Loaded: loaded (...; enabled; preset: enabled)
     Active: active (running)
```
**On macOS:**

Start PostgreSQL

brew services 

start postgresql

# Verify it's running

brew services list

Step 3: Create PostgreSQL Database

Access PostgreSQL

sudo -u postgres psql

**Step 4:** **Clone the Project**

bash# Create a projects directory (optional)

mkdir ~/projects

cd ~/projects

# Clone the repository (or extract if you have a ZIP file)

git clone https://github.com/Teddy-2004/anti_corrup.git

cd anti-corrup

**Step 5: Create Virtual Environment**

bash# Navigate to project directory (if not already there)

cd ~/projects/anti-corruption-platform

# Create virtual environment
python3 -m venv venv

**Activate virtual environment**

**On Linux/macOS:**

source venv/bin/activate

**On Windows:**

venv\Scripts\activate

Verify activation (you should see (venv) at the start of your terminal line)

**Step 6: Install Python Dependencies**

bash# Make sure you're in the virtual environment

**Install all required packages**

pip install --upgrade pip

pip install -r requirements.txt

**Verify installation**

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

**Step 7: Create Project Directories**

bash# Create uploads directory for evidence files

mkdir -p static/uploads

mkdir -p static/css

mkdir -p static/js

**Verify they were created**
ls -la static/

Running Locally

**Step 1: Initialize the Database**

bash# Make sure virtual environment is activated

source venv/bin/activate

**Set Flask app**

export FLASK_APP=app.py

**Create database tables and admin user**

python3 create_admin.py
```

You should see:
✅ Database tables created
✅ Admin user created!
```

**Step 2: Start the Application**

bash# Make sure virtual environment is activated

source venv/bin/activate

**Navigate to project directory**

cd ~/projects/anti-corrup

# Run the Flask app
python3 app.py
```

You should see:
🚀 Starting Anti-Corruption Platform on http://localhost:5000
👤 Admin login: http://localhost:5000/admin/login
📝 Default credentials - Username: admin | Password: ChangeThisPassword123!
```

**Step 3: Access the Application**

Open your web browser and visit:

Public Portal:

Homepage: http://localhost:5000

Submit Report: http://localhost:5000/report

Track Report: http://localhost:5000/track

About: http://localhost:5000/about

Admin Panel:

Login: http://localhost:5000/admin/login

Dashboard: http://localhost:5000/admin/dashboard (after login)

**Step 4: Test the Application**

Test as a Citizen:

Visit http://localhost:5000

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

**Deactivate virtual environment (optional)**

deactivate

License & Attribution

This project is provided as-is for educational and development purposes.

**Tedla Tesfaye Godebo**
