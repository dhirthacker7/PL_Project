import gspread
from gspread_dataframe import set_with_dataframe
import pandas as pd
import os
from dotenv import load_dotenv

# Load environment variables from .env file (for local development)
load_dotenv()

# --- CONFIGURATION ---
SERVICE_ACCOUNT_FILE = 'service_account_key.json'

# Get spreadsheet key from environment variable
SPREADSHEET_KEY = os.getenv('SPREADSHEET_KEY')

if not SPREADSHEET_KEY:
    raise ValueError(
        "SPREADSHEET_KEY not found in environment variables. "
        "Please set it in your .env file or as an environment variable."
    )
# ---------------------

def authenticate_gsheets():
    """Authenticates with Google Sheets using the service account file."""
    try:
        gc = gspread.service_account(filename=SERVICE_ACCOUNT_FILE)
        print("Google Sheets authenticated.")
        return gc
    except Exception as e:
        print(f"ERROR: Could not authenticate with Google Sheets. {e}")
        return None

def upload_dataframe_to_gsheet(df, sheet_name, gc):
    """Uploads a pandas DataFrame to a specified worksheet in the target spreadsheet."""
    if df.empty or gc is None:
        print(f"Skipping upload for {sheet_name}. DataFrame is empty or authentication failed.")
        return

    try:
        sh = gc.open_by_key(SPREADSHEET_KEY)
        
        # Try to open the sheet, if not found, create it
        try:
            worksheet = sh.worksheet(sheet_name)
        except gspread.WorksheetNotFound:
            # Create a new sheet with default size
            worksheet = sh.add_worksheet(title=sheet_name, rows=100, cols=20) 
            
        # Clear the sheet and write the DataFrame (faster than update_cells)
        worksheet.clear()
        set_with_dataframe(worksheet, df, include_index=False)
        
        # Make the header row bold
        worksheet.format('1:1', {
            'textFormat': {
                'bold': True
            }
        })
        
        print(f"Successfully uploaded data to Google Sheet: Tab '{sheet_name}'")
        
    except Exception as e:
        print(f"ERROR: Failed to upload to Google Sheet: {e}")