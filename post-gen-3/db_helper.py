import sqlite3
import os

DB_FILE = "templates.db"

def initialize_db():
    """Initialize the SQLite database without overwriting existing data."""
    if not os.path.exists(DB_FILE):
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS templates (
                id TEXT PRIMARY KEY,
                name TEXT,
                settings TEXT,
                image_path TEXT
            )
        ''')
        conn.commit()
        conn.close()

def save_template(template_id, name, settings, image_path):
    """Save or update a template in the database."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO templates (id, name, settings, image_path)
        VALUES (?, ?, ?, ?)
    ''', (template_id, name, settings, image_path))
    conn.commit()
    conn.close()

def delete_template(template_id):
    """Delete a template by its ID."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM templates WHERE id = ?', (template_id,))
    conn.commit()
    conn.close()

def load_templates():
    """Load all templates."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT id, name FROM templates')
    templates = cursor.fetchall()
    conn.close()
    return templates

def load_template(template_id):
    """Load a specific template."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM templates WHERE id = ?', (template_id,))
    template = cursor.fetchone()
    conn.close()
    return template
