import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect('agrolinga.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS sensor_data
                 (id INTEGER PRIMARY KEY, timestamp TEXT, soil_moisture REAL, temperature REAL, ph_level REAL, npk_n REAL, npk_p REAL, npk_k REAL, ec REAL, co2 REAL)''')
    
    # Add missing columns if they don't exist (for migration from old schema)
    try:
        c.execute("ALTER TABLE sensor_data ADD COLUMN npk_n REAL")
    except sqlite3.OperationalError:
        pass  # Column already exists
    
    try:
        c.execute("ALTER TABLE sensor_data ADD COLUMN npk_p REAL")
    except sqlite3.OperationalError:
        pass
    
    try:
        c.execute("ALTER TABLE sensor_data ADD COLUMN npk_k REAL")
    except sqlite3.OperationalError:
        pass
    
    try:
        c.execute("ALTER TABLE sensor_data ADD COLUMN ec REAL")
    except sqlite3.OperationalError:
        pass
    
    try:
        c.execute("ALTER TABLE sensor_data ADD COLUMN co2 REAL")
    except sqlite3.OperationalError:
        pass
    
    conn.commit()
    conn.close()

def save_sensor_data(soil_moisture, temperature, ph_level, npk_n=None, npk_p=None, npk_k=None, ec=None, co2=None):
    conn = sqlite3.connect('agrolinga.db')
    c = conn.cursor()
    timestamp = datetime.now().isoformat()
    c.execute("INSERT INTO sensor_data (timestamp, soil_moisture, temperature, ph_level, npk_n, npk_p, npk_k, ec, co2) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
              (timestamp, soil_moisture, temperature, ph_level, npk_n, npk_p, npk_k, ec, co2))
    conn.commit()
    conn.close()

def get_latest_sensor_data(): 
    conn = sqlite3.connect('agrolinga.db')
    c = conn.cursor()
    c.execute("SELECT * FROM sensor_data ORDER BY id DESC LIMIT 1")
    data = c.fetchone()
    conn.close()
    return data

def get_sensor_history(limit=10):
    conn = sqlite3.connect('agrolinga.db')
    c = conn.cursor()
    c.execute("SELECT * FROM sensor_data ORDER BY id DESC LIMIT ?", (limit,))
    data = c.fetchall()
    conn.close()
    return data
