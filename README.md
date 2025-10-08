⚽ Automated FPL Data Pipeline
This project establishes a complete, end-to-end data pipeline to automatically collect, clean, and consolidate Fantasy Premier League (FPL) data and Premier League standings. The final output is stored in Google Sheets, ready to be consumed by a live Tableau Public dashboard.

This pipeline replicates the functionality of a similar R project, utilizing modern Python data engineering techniques.

🚀 Live Dashboard (Example Placeholder)
[Insert your Tableau Public Dashboard link here once published!]

✨ Project Architecture & Automation
The entire pipeline is orchestrated by GitHub Actions and runs daily to ensure data is fresh for the connected visualization layer.

Component

Technology

Role

Data Acquisition

Python (requests, beautifulsoup4)

Fetches dynamic FPL API data and scrapes static league standings from the BBC.

Data Processing

Python (pandas)

Cleans, validates, and prepares five distinct tables, including the crucial dynamic Teams_Lookup table.

Data Storage

Google Sheets (gspread)

Stores the final, clean, automated data extracts for reliable consumption by Tableau Public.

Automation

GitHub Actions

Schedules the Python script to run daily using secure credentials (Secrets).

Visualization

Tableau Public

Connects to the live Google Sheet extract and displays data in a dynamic dashboard.

⚙️ Data Flow
The data is standardized into five distinct sheets, providing a robust relational structure for Tableau:

Player_Static: Current player prices, total points, and transfer data.

Teams_Lookup: Dynamic mapping of FPL Team ID (number) to Team Name (string). (Crucial for Tableau joining)

Historic_Seasons: Detailed season-by-season points history for players.

Fixtures: All past and future match data.

Standings: Current Premier League table scraped from the BBC.

💻 Setup and Installation
Prerequisites
Python 3.10+

Git and a GitHub account

A Google Cloud Project with the Google Sheets API enabled.

A Google Service Account key (service_account_key.json).

Local Setup
Clone the Repository:

git clone [https://github.com/dhirthacker7/PL_Project.git](https://github.com/dhirthacker7/PL_Project.git)
cd PL_Project/PL_Pipeline

Setup Environment & Install Libraries:

python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

Authentication: Place your service_account_key.json file inside the PL_Pipeline folder.

Run Locally:

python main_pipeline.py

GitHub Actions Setup
Set Secret: Store the full content of your service_account_key.json file as a GitHub Repository Secret named GOOGLE_CREDENTIALS.

The workflow is configured to run daily via the pipeline.yml file.

🔗 Tableau Integration
The dashboard connects to the five sheets generated in the Google Spreadsheet. The Tableau data source is structured to facilitate advanced analysis by performing the following physical joins in the Physical Layer:

Player_Static is linked via Inner Join to Teams_Lookup (on Team ID).

Player_Static is linked via Left Join to Historic_Seasons (on Player ID).

Player_Static is linked via Left Join to Fixtures (on Team ID to both team_h OR team_a).
