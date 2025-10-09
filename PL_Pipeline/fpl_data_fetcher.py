import requests
import pandas as pd
from tqdm import tqdm

def fetch_static_data():
    """Fetches the main static data from the FPL API, including Teams Lookup."""
    url = "https://fantasy.premierleague.com/api/bootstrap-static/"
    response = requests.get(url)
    response.raise_for_status() 
    data = response.json()
    
    # Extract key components into DataFrames
    elements_df = pd.DataFrame(data['elements'])
    teams_df = pd.DataFrame(data['teams']) # This is the dynamic Teams_Lookup table
    gameweeks_df = pd.DataFrame(data['events'])
    
    # Select essential player columns for Player_Static table
    player_data = elements_df[['id', 'web_name', 'first_name', 'second_name', 
                               'element_type', 'team', 'total_points', 'now_cost', 
                               'form', 'selected_by_percent', 'transfers_in', 
                               'goals_scored', 'assists', 'bonus', 'yellow_cards', 'red_cards']]
    
    print("Static data fetched successfully.")
    return player_data, teams_df, gameweeks_df

def fetch_fixtures():
    """Fetches all past and future fixture data."""
    url = "https://fantasy.premierleague.com/api/fixtures/"
    response = requests.get(url)
    response.raise_for_status()
    fixtures_df = pd.DataFrame(response.json())
    
    print("Fixtures data fetched successfully.")
    return fixtures_df

def fetch_player_historic_data(player_data_df):
    """Fetches detailed historic data for every player using an ID loop."""
    historic_data_list = []
    
    player_ids = player_data_df['id'].tolist()
    
    for player_id in tqdm(player_ids, desc="Fetching Player History"):
        url = f"https://fantasy.premierleague.com/api/element-summary/{player_id}/"
        
        try:
            response = requests.get(url)
            
            if response.status_code == 200:
                data = response.json()
            else:
                raise requests.HTTPError(f"Status Code: {response.status_code}")

            # Check for 'history_past' (Historic Seasons data)
            if 'history_past' in data and len(data['history_past']) > 0:
                df = pd.DataFrame(data['history_past'])
                df['player_id'] = player_id
                historic_data_list.append(df)
            
        except requests.exceptions.RequestException as e:
            tqdm.write(f"Skipping Player ID {player_id} due to request error: {e}")
            continue

    if historic_data_list:
        final_historic_df = pd.concat(historic_data_list, ignore_index=True)
    else:
        final_historic_df = pd.DataFrame()
        
    print("\nHistoric player data loop completed.")
    return final_historic_df