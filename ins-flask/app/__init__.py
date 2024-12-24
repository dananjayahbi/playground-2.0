# flask_app/app/__init__.py
import os
import sys
from flask import Flask
from app.models import init_db

def create_app():
    app = Flask(__name__)

    # Determine the persistent path for the SQLite database
    if getattr(sys, 'frozen', False):  # If running as an executable
        # Use the directory where the executable is located
        base_dir = os.path.dirname(sys.executable)
    else:  # If running as a script
        # Use the directory of the script for non-executable environments
        base_dir = os.path.dirname(os.path.abspath(__file__))

    # Ensure the database is created in a persistent directory
    db_dir = os.path.join(base_dir, '../instance')  # Store the database in the 'data' folder
    os.makedirs(db_dir, exist_ok=True)  # Create the 'data' directory if it doesn't exist
    db_path = os.path.join(db_dir, 'database.db')  # Database file location

    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize the database (only if it doesn't exist)
    init_db(app)

    return app
