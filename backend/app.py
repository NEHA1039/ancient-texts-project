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

# Endpoint to get all artifacts
@app.route('/api/artifacts')
def get_all_artifacts():
    conn = get_db_connection()
    artifacts_cursor = conn.execute('SELECT * FROM Artifacts LIMIT 20')
    artifacts = artifacts_cursor.fetchall()
    conn.close()
    return jsonify([dict(row) for row in artifacts])

# Endpoint for a single artifact
@app.route('/api/artifacts/<int:artifact_id>')
def get_artifact_by_id(artifact_id):
    conn = get_db_connection()
    artifact_cursor = conn.execute('SELECT * FROM Artifacts WHERE ArtifactID = ?', (artifact_id,))
    artifact = artifact_cursor.fetchone()
    conn.close()
    
    if artifact is None:
        return jsonify({"error": "Artifact not found"}), 404
        
    return jsonify(dict(artifact))

# --- Day 9 Code Starts Here ---

# New: Create the endpoint to get a list of all texts
@app.route('/api/texts')
def get_all_texts():
    conn = get_db_connection()
    # We use a JOIN to include the author's name along with the work's details
    texts_cursor = conn.execute("""
        SELECT W.WorkID, W.EnglishTitle, A.FullName as AuthorName
        FROM Works W
        JOIN Authors A ON W.AuthorID = A.AuthorID
    """)
    texts = texts_cursor.fetchall()
    conn.close()
    return jsonify([dict(row) for row in texts])

# New: Create the endpoint for a single text
@app.route('/api/texts/<int:text_id>')
def get_text_by_id(text_id):
    conn = get_db_connection()
    # We join with Authors again to get the author's name for the single text view
    text_cursor = conn.execute("""
        SELECT W.*, A.FullName as AuthorName
        FROM Works W
        JOIN Authors A ON W.AuthorID = A.AuthorID
        WHERE W.WorkID = ?
    """, (text_id,))
    text = text_cursor.fetchone()
    conn.close()
    
    if text is None:
        return jsonify({"error": "Text not found"}), 404
        
    return jsonify(dict(text))

# --- Day 9 Code Ends Here ---


# Run the application
if __name__ == '__main__':
    app.run(debug=True)