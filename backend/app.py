# Import necessary libraries
from flask import Flask, jsonify
import sqlite3

# Create an instance of the Flask class
app = Flask(__name__)

# Function to get a database connection
def get_db_connection():
    conn = sqlite3.connect('../database/artifacts.db')
    conn.row_factory = sqlite3.Row
    return conn

# Homepage route
@app.route('/')
def hello_world():
    return 'This is the backend server for the Ancient Texts Project!'

# Endpoint to get all artifacts (from Day 7)
@app.route('/api/artifacts')
def get_all_artifacts():
    conn = get_db_connection()
    artifacts_cursor = conn.execute('SELECT * FROM Artifacts LIMIT 20')
    artifacts = artifacts_cursor.fetchall()
    conn.close()
    return jsonify([dict(row) for row in artifacts])


# New: Create the endpoint for a single artifact
# The <int:artifact_id> part is a dynamic route. Flask captures the integer
# from the URL and passes it as an argument to our function.
@app.route('/api/artifacts/<int:artifact_id>')
def get_artifact_by_id(artifact_id):
    # 1. Get a database connection
    conn = get_db_connection()
    
    # 2. Execute a SQL query to get the artifact with the matching ID
    # The '?' is a placeholder to prevent SQL injection attacks.
    artifact_cursor = conn.execute('SELECT * FROM Artifacts WHERE ArtifactID = ?', (artifact_id,))
    artifact = artifact_cursor.fetchone() # fetchone() gets the first result
    
    # 3. Close the database connection
    conn.close()
    
    # 4. If the artifact was not found, return an error (optional but good practice)
    if artifact is None:
        return jsonify({"error": "Artifact not found"}), 404
        
    # 5. Convert the row to a dictionary and return as JSON
    return jsonify(dict(artifact))


# Run the application
if __name__ == '__main__':
    app.run(debug=True)