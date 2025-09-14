import requests
import sqlite3
import time # New: Import the time library to pause between requests

# --- CONFIGURATION ---
DB_FILE = "database/artifacts.db"
# New: Define the Search API URL and our search term
SEARCH_TERM = "Greek Art"
SEARCH_API_URL = f"https://collectionapi.metmuseum.org/public/collection/v1/search?q={SEARCH_TERM}"
OBJECT_API_BASE_URL = "https://collectionapi.metmuseum.org/public/collection/v1/objects/"

# --- SCRIPT EXECUTION ---
try:
    # 1. New: Search for objects to get a list of IDs
    print(f"Searching for objects with term: '{SEARCH_TERM}'...")
    search_response = requests.get(SEARCH_API_URL)
    search_response.raise_for_status()
    search_data = search_response.json()
    
    object_ids = search_data.get('objectIDs')
    if not object_ids:
        print("No objects found for this search term.")
    else:
        # Let's limit to the first 50 objects to not overload the API or our DB
        object_ids_to_fetch = object_ids[:50] 
        print(f"Found {len(object_ids)} objects. Fetching details for the first {len(object_ids_to_fetch)}.")

        # 2. Connect to the database (once, before the loop)
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        # 3. New: Loop through each object ID
        for object_id in object_ids_to_fetch:
            print(f"\n--- Fetching Object ID: {object_id} ---")
            object_api_url = f"{OBJECT_API_BASE_URL}{object_id}"
            
            # This inner try/except handles errors for a single object
            try:
                obj_response = requests.get(object_api_url)
                obj_response.raise_for_status()
                data = obj_response.json()

                # Extract data (same as Day 3)
                title = data.get('title')
                culture = data.get('culture')
                creation_date = data.get('objectDate')
                image_path = data.get('primaryImageSmall')
                description = data.get('objectName')

                if not all([title, culture, image_path]):
                    print(f"   - Skipping {object_id}: Missing essential data.")
                    continue # Skips to the next iteration of the loop

                # Insert Provenance (same as Day 3)
                cursor.execute("SELECT ProvenanceID FROM Provenances WHERE Name = ?", (culture,))
                result = cursor.fetchone()
                if result:
                    provenance_id = result[0]
                else:
                    cursor.execute("INSERT INTO Provenances (Name) VALUES (?)", (culture,))
                    provenance_id = cursor.lastrowid
                
                # Insert Artifact (same as Day 3)
                cursor.execute("""
                    INSERT OR IGNORE INTO Artifacts (Title, ObjectType, ProvenanceID, CreationDate, ImageFilePath, Description)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (title, description, provenance_id, creation_date, image_path, "Fetched from The Met API"))
                
                print(f"   - Success! Saved '{title}' to the database.")

            except requests.exceptions.RequestException as e:
                print(f"   - Error fetching object {object_id}: {e}")
            
            # New: Be polite to the API and wait a moment before the next request
            time.sleep(0.1) # Wait for 0.1 seconds
            
        # 4. Commit all changes and close the connection (once, after the loop)
        conn.commit()
        conn.close()
        print("\n✅ Bulk ingestion complete.")

except requests.exceptions.RequestException as e:
    print(f"\n❌ An error occurred during the initial search: {e}")
except sqlite3.Error as e:
    print(f"\n❌ A database error occurred: {e}")