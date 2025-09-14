# Import the necessary libraries
import requests  # For making HTTP requests
import json      # For pretty-printing the full response (optional)

# --- CONFIGURATION ---
# The ID of the specific object we want to fetch from The Met's collection
OBJECT_ID = 466112
# The base URL for The Met's Collection API for a single object
API_URL = f"https://collectionapi.metmuseum.org/public/collection/v1/objects/{OBJECT_ID}"

# --- SCRIPT EXECUTION ---
print(f"Attempting to fetch data for object ID: {OBJECT_ID}...")
print(f"URL: {API_URL}")

try:
    # 1. Make the API request
    # This sends a GET request to the specified URL and waits for a response.
    response = requests.get(API_URL)

    # This line will automatically raise an error if the request failed (e.g., 404 Not Found)
    response.raise_for_status()

    print("\n✅ Success! API request was successful.")

    # 2. Parse the JSON response
    # The API's response is in JSON format. We convert it into a Python dictionary.
    data = response.json()

    # 3. Extract and display the key details
    # We use the .get() method, which is a safe way to access dictionary keys.
    # It returns None instead of an error if a key doesn't exist.
    print("\n--- Artifact Details ---")
    print(f"  Title: {data.get('title')}")
    print(f"  Date: {data.get('objectDate')}")
    print(f"  Culture: {data.get('culture')}")
    print(f"  Medium: {data.get('medium')}")
    print(f"  Image URL: {data.get('primaryImageSmall')}")
    print("------------------------\n")

# This block catches potential errors (like no internet connection or a bad URL)
except requests.exceptions.RequestException as e:
    print(f"\n❌ An error occurred during the request: {e}")