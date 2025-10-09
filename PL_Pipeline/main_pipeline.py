import sys
import pandas as pd
from fpl_data_fetcher import fetch_static_data, fetch_fixtures, fetch_player_historic_data
from scraper import scrape_standings
from gsheet_uploader import authenticate_gsheets, upload_dataframe_to_gsheet

def main():
    print("\n--- Starting FPL Data Pipeline ---")
    
    # 1. API Data Acquisition
    try:
        # teams_lookup_df is now returned here
        player_data, teams_lookup_df, gameweeks_df = fetch_static_data()
        fixtures_df = fetch_fixtures()
        historic_df = fetch_player_historic_data(player_data)
        
    except Exception as e:
        print(f"A critical error occurred during primary data fetching: {e}")
        sys.exit(1)
        
    # 2. Web Scraping (Now fixed to return clean Points)
    standings_df = scrape_standings()

    # 3. Google Sheets Persistence
    gc = authenticate_gsheets()
    
    # List of DataFrames to upload and their target sheet names
    data_to_upload = [
        (historic_df, 'Historic_Seasons'),
        (player_data, 'Player_Static'),
        (fixtures_df, 'Fixtures'),
        (standings_df, 'Standings'), # This is the sheet that is now clean
        (teams_lookup_df, 'Teams_Lookup') # This is the dynamic lookup table
    ]
    
    for df, name in data_to_upload:
        upload_dataframe_to_gsheet(df, name, gc)

    print("--- FPL Data Pipeline Completed Successfully ---")

if __name__ == "__main__":
    main()