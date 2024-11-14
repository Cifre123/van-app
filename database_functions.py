import sqlite3
from datetime import datetime

def add_van(van_id):
    conn = sqlite3.connect("van_damage_detection.db")
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO vans (van_id) VALUES (?)", (van_id,))
    conn.commit()
    conn.close()

def add_image(van_id, image_path):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn = sqlite3.connect("van_damage_detection.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO images (van_id, image_path, timestamp) VALUES (?, ?, ?)",
                   (van_id, image_path, timestamp))
    conn.commit()
    conn.close()

def add_comparison(van_id, old_image_path, new_image_path, similarity_score, damage_detected_path):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn = sqlite3.connect("van_damage_detection.db")
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO comparisons (van_id, old_image_path, new_image_path, similarity_score, 
                      damage_detected_path, timestamp) VALUES (?, ?, ?, ?, ?, ?)''',
                   (van_id, old_image_path, new_image_path, similarity_score, damage_detected_path, timestamp))
    conn.commit()
    conn.close()

def get_latest_image(van_id):
    conn = sqlite3.connect("van_damage_detection.db")
    cursor = conn.cursor()
    cursor.execute("SELECT image_path FROM images WHERE van_id = ? ORDER BY timestamp DESC LIMIT 1", (van_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None
