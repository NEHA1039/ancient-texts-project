Ancient Texts and Artifacts API
This project is a full-stack application designed to create a digital bridge between classical literature and ancient artifacts. It functions as a case study in Digital Humanities, demonstrating how to build a system that ingests data from disparate sources (museum APIs and text files) and organizes it into a cohesive, relational database. The backend is powered by a Flask-based REST API that serves this interconnected data, allowing for new ways to explore and discover the context of the ancient world.

## Features
Relational Database: An SQLite database architected to model the relationships between authors, texts, artifacts, and their cultural origins.

Automated Data Ingestion: Python scripts that automatically fetch artifact data from The Metropolitan Museum of Art's API and ingest literary works from local text files.

RESTful API: A backend built with Flask that exposes a series of endpoints to query the interconnected data.

Structured Data: All API responses are served in a clean, machine-readable JSON format.

## Technology Stack
Backend: Python, Flask

Database: SQLite

Primary Libraries: requests, sqlite3

Data Sources: The Metropolitan Museum of Art Collection API, Project Gutenberg

## Setup and Installation
To get this project running on your local machine, follow these steps.

1. Clone the Repository

Bash

git clone https://github.com/YOUR_USERNAME/ancient-texts-project.git
cd ancient_texts-project
2. Create and Populate the Database
First, create the database from the schema.

Bash

python setup_database.py
Next, run the ingestion scripts to fill the database with data.

Bash

# Ingest artifacts from The Met's API
python scripts/ingest_met_data.py

# Ingest texts from local files
python scripts/ingest_texts.py
3. Run the Backend Server
Navigate into the backend folder and start the Flask application.

Bash

cd backend
python app.py
The server will be running at http://127.0.0.1:5000.

## API Endpoints
The following endpoints are currently available:

Method	Endpoint	Description
GET	/api/artifacts	Retrieves a list of all artifacts.
GET	/api/artifacts/<int:artifact_id>	Retrieves details for a single artifact by its ID.
GET	/api/texts	Retrieves a list of all literary works.
GET	/api/texts/<int:text_id>	Retrieves the full content of a single work.

Export to Sheets
## Future Work
Develop a frontend application (e.g., using React or Vue.js) to consume the API and provide a user-friendly interface for exploring the data.

Implement more advanced API features, such as search and filtering.

Integrate Natural Language Processing (NLP) to automatically suggest links between texts and artifacts.









