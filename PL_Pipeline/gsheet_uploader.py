import gspread
from gspread_dataframe import set_with_dataframe
import pandas as pd

# --- CONFIGURATION ---
SERVICE_ACCOUNT_FILE = 'service_account_key.json' # Must be in the root directory
# !!! REPLACE THIS WITH YOUR SHEET KEY (from the URL) !!!
SPREADSHEET_KEY = '15pL_p-LVDftcb9rBPMJcyjuDaxg851N5k6ZiMcsHLQI' 
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
        
        print(f"Successfully uploaded data to Google Sheet: Tab '{sheet_name}'")
        
    except Exception as e:
        print(f"ERROR: Failed to upload to Google Sheet: {e}")