import sqlite3
from datetime import datetime

def initialize_database():
    conn = sqlite3.connect("van_damage_detection.db")
    cursor = conn.cursor()

    # Create tables
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS vans (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        van_id TEXT UNIQUE
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS images (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        van_id TEXT,
        image_path TEXT,
        timestamp TEXT,
        FOREIGN KEY (van_id) REFERENCES vans(van_id)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS comparisons (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        van_id TEXT,
        old_image_path TEXT,
        new_image_path TEXT,
        similarity_score REAL,
        damage_detected_path TEXT,
        timestamp TEXT,
        FOREIGN KEY (van_id) REFERENCES vans(van_id)
    )
    ''')

    conn.commit()
    conn.close()

# Function to add a van ID if it doesn't exist
def add_van(van_id):
    conn = sqlite3.connect("van_damage_detection.db")
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO vans (van_id) VALUES (?)", (van_id,))
    conn.commit()
    conn.close()

# Function to add an image record
def add_image(van_id, image_path):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn = sqlite3.connect("van_damage_detection.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO images (van_id, image_path, timestamp) VALUES (?, ?, ?)",
                   (van_id, image_path, timestamp))
    conn.commit()
    conn.close()

# Function to add a comparison record
def add_comparison(van_id, old_image_path, new_image_path, similarity_score, damage_detected_path):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn = sqlite3.connect("van_damage_detection.db")
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO comparisons (van_id, old_image_path, new_image_path, similarity_score, 
                      damage_detected_path, timestamp) VALUES (?, ?, ?, ?, ?, ?)''',
                   (van_id, old_image_path, new_image_path, similarity_score, damage_detected_path, timestamp))
    conn.commit()
    conn.close()

# Function to get the latest image for a van ID
def get_latest_image(van_id):
    conn = sqlite3.connect("van_damage_detection.db")
    cursor = conn.cursor()
    cursor.execute("SELECT image_path FROM images WHERE van_id = ? ORDER BY timestamp DESC LIMIT 1", (van_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

# Initialize the database if this file is run as a script
if __name__ == "__main__":
    initialize_database()
