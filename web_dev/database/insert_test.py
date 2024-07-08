import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('cats.db')
c = conn.cursor()

# Sample data to insert
data = [
    ('cat_image_1.jpg', 'result_1'),
    ('cat_image_2.jpg', 'result_2'),
    ('cat_image_3.jpg', 'result_3'),
    ('cat_image_4.jpg', 'result_4'),
    ('cat_image_5.jpg', 'result_5')
]

# Insert data into the records table
c.executemany('INSERT INTO records (filename, result) VALUES (?, ?)', data)

# Commit the transaction
conn.commit()

# Close the connection
conn.close()

print("Data inserted successfully")
