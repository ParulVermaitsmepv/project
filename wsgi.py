import os
import sys

# -----------------------------------------------------------------------------
# PythonAnywhere WSGI Configuration for Flask
# -----------------------------------------------------------------------------
# This file serves as the entry point for running your Flask application on
# WSGI servers like PythonAnywhere.
# -----------------------------------------------------------------------------

# Automatically get the directory where wsgi.py is located
project_home = os.path.dirname(os.path.abspath(__file__))

# Ensure project directory is in Python path
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Optional: Set environment variables for production
# os.environ['FLASK_ENV'] = 'production'
# os.environ['SECRET_KEY'] = 'your-custom-secret-key-here'

# Import the Flask app object and alias it to 'application'
# WSGI servers (like PythonAnywhere) search for an executable object named 'application'
from app import app as application

if __name__ == "__main__":
    application.run()
