import requests
from bs4 import BeautifulSoup
import pandas as pd
from io import StringIO # Needed to wrap the string for pandas

def scrape_standings():
    """Scrapes the Premier League table from the BBC website."""
    url = "https://www.bbc.co.uk/sport/football/premier-league/table"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    # --- SIMPLIFIED SCRAPING ---
    # We rely on pandas.read_html to find the table in the entire HTML content
    # This is more robust than relying on brittle CSS classes.
    try:
        # Wrap the response text in StringIO to suppress the Future Warning
        standings_list = pd.read_html(StringIO(response.text))
        
        # Assuming the first table found is the main league table
        standings_df = standings_list[0]
        
    except ValueError:
        print("Error: pandas.read_html failed to find any table structure.")
        return pd.DataFrame()
        
    # --- COLUMN CLEANING FIX ---
    # The scraped table seems to have 10 columns (excluding 'Form'). 
    # We MUST ensure the length of the new column list matches the DataFrame size.
    
    expected_columns = ['Position', 'Team', 'Played', 'Won', 'Drawn', 'Lost', 'GF', 'GA', 'GD', 'Points']
    
    if standings_df.shape[1] == len(expected_columns):
        standings_df.columns = expected_columns
    else:
        print(f"Error: Table has {standings_df.shape[1]} columns, but we expected {len(expected_columns)}. Cannot rename.")
        return pd.DataFrame()

    print("League Standings scraped and processed successfully.")
    return standings_df