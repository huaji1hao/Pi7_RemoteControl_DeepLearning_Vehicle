from flask import Flask, request
import sqlite3
import os

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_string():
    if 'filename' not in request.form or 'result' not in request.form:
        return 'Missing filename or result', 400
    
    filename = request.form['filename']
    result = request.form['result']
    
    if filename == '' or result == '':
        return 'Filename or result is empty', 400
    
    # Connect to the SQLite database
    conn = sqlite3.connect('./database/cats.db')
    c = conn.cursor()
    
    # Insert data into the records table
    c.execute('INSERT INTO records (filename, result) VALUES (?, ?)', (filename, result))
    
    # Commit the transaction
    conn.commit()
    
    # Close the connection
    conn.close()
    
    return 'Text successfully received and inserted into database', 200

if __name__ == '__main__':
    if not os.path.exists('./database'):
        os.makedirs('./database')
    app.run(host='0.0.0.0', port=6000)
