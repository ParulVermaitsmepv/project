# Configuration file for School Management System
# Copy this to config.py and modify as needed

import os
from datetime import timedelta

# Flask Configuration
SECRET_KEY = 'dev-secret-key-change-in-production-xyz123'
DEBUG = True
TESTING = False

# Database Configuration
SQLALCHEMY_DATABASE_URI = 'sqlite:///school.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = False

# Session Configuration
PERMANENT_SESSION_LIFETIME = timedelta(days=7)
SESSION_COOKIE_SECURE = False  # Set to True in production with HTTPS
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'

# Upload Configuration
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'txt', 'doc', 'docx', 'xlsx', 'csv'}

# Application Configuration
SCHOOL_NAME = 'School Management System'
SCHOOL_EMAIL = 'admin@school.edu'
SCHOOL_PHONE = '+91-XXXXXXXXXX'
SCHOOL_ADDRESS = 'School Address Here'

# Email Configuration (Optional)
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USERNAME = 'your-email@gmail.com'
MAIL_PASSWORD = 'your-app-password'

# Pagination
ITEMS_PER_PAGE = 20

# Fees Configuration
DEFAULT_FEES_AMOUNT = 5000.00
FEES_DUE_DAYS = 30
LATE_FEE_PERCENTAGE = 5.0

# Logging Configuration
LOG_FILE = 'app.log'
LOG_LEVEL = 'INFO'

# Environment-specific configuration
if os.getenv('FLASK_ENV') == 'production':
    DEBUG = False
    SESSION_COOKIE_SECURE = True
    SQLALCHEMY_ECHO = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'change-this-in-production')
elif os.getenv('FLASK_ENV') == 'testing':
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False
