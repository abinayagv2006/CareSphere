import sqlite3

conn = sqlite3.connect('users.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    age INTEGER,
    gender TEXT,
    phone TEXT,
    email TEXT,
    password TEXT
)
''')
cursor.execute('''
CREATE TABLE IF NOT EXISTS medicines(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    medicine_name TEXT,
    medicine_time TEXT,
    user_email TEXT
)
''')
cursor.execute('''
CREATE TABLE IF NOT EXISTS health_records(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_name TEXT,
    weight REAL,
    height REAL,
    blood_pressure TEXT,
    sugar_level TEXT,
    user_email TEXT
)
''')
cursor.execute('''
CREATE TABLE IF NOT EXISTS feedbacks(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    feedback TEXT,
    rating TEXT,
    user_email TEXT
)
''')
cursor.execute('''
CREATE TABLE IF NOT EXISTS emergency_contacts(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    relation TEXT,
    phone TEXT,
    user_email TEXT
)
''')
cursor.execute('''
CREATE TABLE IF NOT EXISTS health_passport(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    age INTEGER,
    blood_group TEXT,
    blood_pressure TEXT,
    sugar_level TEXT,
    emergency_contact TEXT,
    user_email TEXT
)
''')

conn.commit()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
print(cursor.fetchall())

conn.close()

print("Database Created Successfully!")