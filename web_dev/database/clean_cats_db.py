import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('cats.db')
c = conn.cursor()

# Delete all records from the records table
c.execute('DELETE FROM records')

# Commit the transaction
conn.commit()

# Close the connection
conn.close()

print("All records deleted successfully")
