# Import necessary libraries
from flask import Flask, jsonify # New: import jsonify
import sqlite3                 # New: import sqlite3

# Create an instance of the Flask class
app = Flask(__name__)

# New: Function to get a database connection.
# This avoids having to reconnect every time a request is made.
def get_db_connection():
    # Connect to the database file
    conn = sqlite3.connect('../database/artifacts.db')
    # This line allows you to access columns by name (like a dictionary)
    conn.row_factory = sqlite3.Row
    return conn

# Keep the old homepage route (optional)
@app.route('/')
def hello_world():
    return 'This is the backend server for the Ancient Texts Project!'

# New: Create the first API endpoint
# This decorator tells Flask that the /api/artifacts URL should trigger this function.
@app.route('/api/artifacts')
def get_all_artifacts():
    # 1. Get a database connection
    conn = get_db_connection()
    
    # 2. Execute a SQL query to get all artifacts
    # We add "LIMIT 20" for now to keep the response from being too large.
    artifacts_cursor = conn.execute('SELECT * FROM Artifacts LIMIT 20')
    artifacts = artifacts_cursor.fetchall()
    
    # 3. Close the database connection
    conn.close()
    
    # 4. Convert the database rows to a list of dictionaries and return as JSON
    # jsonify is a Flask function that correctly formats the data for web APIs.
    return jsonify([dict(row) for row in artifacts])

# Run the application
if __name__ == '__main__':
    app.run(debug=True)