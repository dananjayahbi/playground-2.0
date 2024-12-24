# flask_app/app/models.py
import os
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Quote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    char_count = db.Column(db.Integer, nullable=False)

def init_db(app):
    db.init_app(app)
    db_path = app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', '')

    # Check if the database file exists
    if not os.path.exists(db_path):
        with app.app_context():
            db.create_all()
