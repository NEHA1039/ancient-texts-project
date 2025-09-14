import sqlite3

# Define the path to the database file and the schema file
DB_FILE = "database/artifacts.db"
SCHEMA_FILE = "database/schema.sql"

# Connect to the database (this will create the file if it doesn't exist)
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

print("Database created. Now setting up the schema...")

# Read the schema file
with open(SCHEMA_FILE, 'r') as f:
    schema_sql = f.read()

# Execute the SQL commands from the schema file
cursor.executescript(schema_sql)

print("Schema has been applied successfully.")
print(f"Database is ready at: {DB_FILE}")

# Commit the changes and close the connection
conn.commit()
conn.close()

