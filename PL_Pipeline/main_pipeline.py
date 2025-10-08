# main_pipeline.py

import sys
import pandas as pd
from fpl_data_fetcher import fetch_static_data, fetch_fixtures, fetch_player_historic_data
from scraper import scrape_standings
from gsheet_uploader import authenticate_gsheets, upload_dataframe_to_gsheet

def main():
    print("\n--- Starting FPL Data Pipeline ---")
    
    # 1. API Data Acquisition
    try:
        player_data, teams_df, gameweeks_df = fetch_static_data()
        fixtures_df = fetch_fixtures()
        historic_df = fetch_player_historic_data(player_data)
        
    except Exception as e:
        print(f"A critical error occurred during primary data fetching: {e}")
        sys.exit(1)
        
    # 2. Web Scraping
    standings_df = scrape_standings()

    # 3. Data Cleaning/Joining: Merge Team Names onto Player Data
    # Create a mapping dictionary for team IDs to names
    team_name_map = teams_df.set_index('id')['name'].to_dict()
    
    # Map team names to the player data
    player_data['team_name'] = player_data['team'].map(team_name_map)
    
    # Example: Merge player name onto the historic data (using ID)
    player_name_map = player_data[['id', 'web_name', 'team_name']].set_index('id')
    
    if not historic_df.empty:
        historic_df = historic_df.merge(player_name_map, 
                                        left_on='player_id', 
                                        right_index=True)
    
    # 4. Google Sheets Persistence
    gc = authenticate_gsheets()
    
    # List of DataFrames to upload and their target sheet names
    data_to_upload = [
        (historic_df, 'Historic_Seasons'),
        (player_data, 'Player_Static'),
        (fixtures_df, 'Fixtures'),
        (standings_df, 'Standings')
    ]
    
    for df, name in data_to_upload:
        # We only upload if the DataFrame is not empty
        upload_dataframe_to_gsheet(df, name, gc)

    print("--- FPL Data Pipeline Completed Successfully ---")

if __name__ == "__main__":
    main()