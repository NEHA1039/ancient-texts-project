# Import the necessary libraries
import requests
import sqlite3 # New: Import the SQLite library

# --- CONFIGURATION ---
OBJECT_ID = 466112
API_URL = f"https://collectionapi.metmuseum.org/public/collection/v1/objects/{OBJECT_ID}"
DB_FILE = "database/artifacts.db" # New: Add path to your database file

# --- SCRIPT EXECUTION ---
print(f"Attempting to fetch data for object ID: {OBJECT_ID}...")
try:
    # 1. Make the API request (same as Day 2)
    response = requests.get(API_URL)
    response.raise_for_status()
    data = response.json()
    print("✅ Success! API data fetched.")

    # 2. Extract the relevant data
    title = data.get('title')
    culture = data.get('culture')
    creation_date = data.get('objectDate')
    image_path = data.get('primaryImageSmall')
    description = data.get('objectName') # Using objectName as a simple description
    
    # New: Don't proceed if essential data is missing
    if not all([title, culture, image_path]):
        print("❌ Missing essential data, skipping database insert.")
    else:
        # 3. Connect to the SQLite database
        print("Connecting to the database...")
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        # 4. Insert Provenance (Culture) if it doesn't exist
        # We check if the culture is already in the Provenances table to avoid duplicates.
        cursor.execute("SELECT ProvenanceID FROM Provenances WHERE Name = ?", (culture,))
        result = cursor.fetchone()
        
        if result:
            provenance_id = result[0]
        else:
            # If not found, insert it and get the new ID
            cursor.execute("INSERT INTO Provenances (Name) VALUES (?)", (culture,))
            provenance_id = cursor.lastrowid
            print(f"   - Added new provenance: '{culture}' with ID: {provenance_id}")

        # 5. Insert the Artifact data
        # We use the provenance_id we just found or created.
        cursor.execute("""
            INSERT INTO Artifacts (Title, ObjectType, ProvenanceID, CreationDate, ImageFilePath, Description)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (title, description, provenance_id, creation_date, image_path, "Fetched from The Met API"))
        
        # 6. Commit changes and close the connection
        conn.commit()
        conn.close()
        
        print(f"✅ Success! Artifact '{title}' has been saved to the database.")

except requests.exceptions.RequestException as e:
    print(f"\n❌ An error occurred during the request: {e}")
except sqlite3.Error as e:
    print(f"\n❌ A database error occurred: {e}")