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

# Endpoint to get a list of all texts
@app.route('/api/texts')
def get_all_texts():
    conn = get_db_connection()
    texts_cursor = conn.execute("""
        SELECT W.WorkID, W.EnglishTitle, A.FullName as AuthorName
        FROM Works W
        JOIN Authors A ON W.AuthorID = A.AuthorID
    """)
    texts = texts_cursor.fetchall()
    conn.close()
    return jsonify([dict(row) for row in texts])

# Endpoint for a single text
@app.route('/api/texts/<int:text_id>')
def get_text_by_id(text_id):
    conn = get_db_connection()
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

# --- Day 10 Code Starts Here ---

# New: Create the endpoint to get all artifacts linked to a text
@app.route('/api/texts/<int:text_id>/artifacts')
def get_artifacts_for_text(text_id):
    conn = get_db_connection()
    # This query uses two JOINs to link Works -> Cross_References -> Artifacts
    artifacts_cursor = conn.execute("""
        SELECT A.* FROM Artifacts A
        JOIN Cross_References CR ON A.ArtifactID = CR.ArtifactID
        WHERE CR.WorkID = ?
    """, (text_id,))
    artifacts = artifacts_cursor.fetchall()
    conn.close()
    
    return jsonify([dict(row) for row in artifacts])

# --- Day 10 Code Ends Here ---


# Run the application
if __name__ == '__main__':
    app.run(debug=True)