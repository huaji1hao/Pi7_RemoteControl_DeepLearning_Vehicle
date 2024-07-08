import sqlite3

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('cats.db')
c = conn.cursor()

# Create a new table with id, filename, and result fields
c.execute('''
CREATE TABLE IF NOT EXISTS records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    filename TEXT NOT NULL,
    result TEXT NOT NULL
)
''')

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Database and table created successfully.")
