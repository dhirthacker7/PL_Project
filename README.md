# ⚽ Automated FPL Data Pipeline

This project establishes a complete, end-to-end data pipeline to automatically **collect**, **clean**, and **consolidate** Fantasy Premier League (FPL) data and Premier League standings.  
The final output is stored in **Google Sheets**, ready to be consumed by a **live Tableau Public dashboard**.

This pipeline replicates the functionality of a similar R project, utilizing modern **Python data engineering techniques**.

---

## 🚀 Live Dashboard (Example Placeholder)

[👉 View Tableau Public Dashboard](#)  

---

## ✨ Project Architecture & Automation

The entire pipeline is orchestrated by **GitHub Actions** and runs **daily** to ensure data is fresh for the connected visualization layer.

| **Component**     | **Technology**                          | **Role**                                                                                      |
|--------------------|------------------------------------------|-----------------------------------------------------------------------------------------------|
| **Data Acquisition** | Python (`requests`, `beautifulsoup4`)   | Fetches dynamic FPL API data and scrapes static league standings from the BBC.                |
| **Data Processing**  | Python (`pandas`)                       | Cleans, validates, and prepares five distinct tables, including the crucial *Teams_Lookup* table. |
| **Data Storage**     | Google Sheets (`gspread`)               | Stores the final, clean, automated data extracts for reliable consumption by Tableau Public.   |
| **Automation**       | GitHub Actions                          | Schedules the Python script to run daily using secure credentials (Secrets).                   |
| **Visualization**    | Tableau Public                          | Connects to the live Google Sheet extract and displays data in a dynamic dashboard.            |

---

## ⚙️ Data Flow

The data is standardized into **five distinct sheets**, providing a robust relational structure for Tableau:

- **Player_Static** — Current player prices, total points, and transfer data.  
- **Teams_Lookup** — Dynamic mapping of FPL Team ID (number) to Team Name (string). *(Crucial for Tableau joins)*  
- **Historic_Seasons** — Detailed season-by-season points history for players.  
- **Fixtures** — All past and future match data.  
- **Standings** — Current Premier League table scraped from the BBC.

---

## 💻 Setup and Installation

### **Prerequisites**

- Python **3.10+**  
- Git and a GitHub account  
- A Google Cloud Project with the **Google Sheets API** enabled  
- A **Google Service Account key** (`service_account_key.json`)

---

### **Local Setup**

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/dhirthacker7/PL_Project.git
   cd PL_Project/PL_Pipeline
   ```
   
2. **Setup Environment & Install Libraries**
   ``` bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Authentication**
   Place your service_account_key.json file inside the PL_Pipeline folder

4. **Run Locally**
   ```bash
   python main_pipeline.py
   ```
