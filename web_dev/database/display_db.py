import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('cats.db')
c = conn.cursor()

# Query to select all records from the records table
c.execute('SELECT * FROM records')

# Fetch all results from the executed query
rows = c.fetchall()

# Print each row
for row in rows:
    print(row)

# Close the connection
conn.close()
