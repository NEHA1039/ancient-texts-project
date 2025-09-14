import sqlite3
import os # Import the 'os' library to work with files and folders

# --- CONFIGURATION ---
DB_FILE = "database/artifacts.db"
SOURCE_TEXTS_DIR = "source_texts" # The folder where you saved your .txt files

# --- A list of dictionaries containing info about our texts ---
# We are hard-coding this metadata for simplicity. It tells our script
# what to look for and what information to associate with each file.
TEXT_METADATA = [
    {
        "file_name": "the_odyssey.txt",
        "original_title": "Odysseia",
        "english_title": "The Odyssey",
        "author_name": "Homer",
        "provenance_name": "Archaic Greek"
    },
    {
        "file_name": "the_aeneid.txt",
        "original_title": "Aeneis",
        "english_title": "The Aeneid",
        "author_name": "Virgil",
        "provenance_name": "Roman"
    },
]

# --- SCRIPT EXECUTION ---
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

print("Starting text ingestion...")

# Loop through each text's metadata dictionary
for text_info in TEXT_METADATA:
    file_path = os.path.join(SOURCE_TEXTS_DIR, text_info["file_name"])
    
    print(f"\n--- Processing: {text_info['english_title']} ---")

    # 1. Check if the text file actually exists before trying to open it
    if not os.path.exists(file_path):
        print(f"   - Error: File not found at {file_path}. Skipping.")
        continue # Go to the next text in the list

    # 2. Get or create the ProvenanceID for the text's culture
    cursor.execute("SELECT ProvenanceID FROM Provenances WHERE Name = ?", (text_info["provenance_name"],))
    result = cursor.fetchone()
    if result:
        provenance_id = result[0]
    else:
        cursor.execute("INSERT INTO Provenances (Name) VALUES (?)", (text_info["provenance_name"],))
        provenance_id = cursor.lastrowid
        print(f"   - Added new provenance: '{text_info['provenance_name']}'")

    # 3. Get or create the AuthorID for the text's author
    cursor.execute("SELECT AuthorID FROM Authors WHERE FullName = ?", (text_info["author_name"],))
    result = cursor.fetchone()
    if result:
        author_id = result[0]
    else:
        cursor.execute("INSERT INTO Authors (FullName, ProvenanceID) VALUES (?, ?)", (text_info["author_name"], provenance_id))
        author_id = cursor.lastrowid
        print(f"   - Added new author: '{text_info['author_name']}'")

    # 4. Read the entire content of the text file
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 5. Insert the Work into the database, linking it to the author and provenance
    cursor.execute("""
        INSERT OR IGNORE INTO Works (OriginalTitle, EnglishTitle, AuthorID, ProvenanceID, Language, Content_Translation)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        text_info["original_title"],
        text_info["english_title"],
        author_id,
        provenance_id,
        "English Translation", # We assume all are translations for this project
        content
    ))
    print(f"   - Success! Saved '{text_info['english_title']}' to the database.")

# Commit all the changes made during the loop
conn.commit()
conn.close()

print("\n✅ Text ingestion complete.")