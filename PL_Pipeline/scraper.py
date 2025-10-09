import requests
from bs4 import BeautifulSoup
import pandas as pd
from io import StringIO
import re

def scrape_standings():
    """Scrapes the Premier League table from the BBC website."""
    url = "https://www.bbc.co.uk/sport/football/premier-league/table"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    try:
        tables = pd.read_html(StringIO(response.text))
        
        if not tables:
            print("Error: No tables found on the page")
            return pd.DataFrame()
        
        # Get the first table (main standings table)
        standings_df = tables[0]
        
        print(f"Initial table shape: {standings_df.shape}")
        
        # Handle MultiIndex columns if present
        if isinstance(standings_df.columns, pd.MultiIndex):
            standings_df.columns = [' '.join(col).strip() if isinstance(col, tuple) else col 
                                   for col in standings_df.columns.values]
        
        # Remove empty rows and columns
        standings_df = standings_df.dropna(how='all')
        standings_df = standings_df.dropna(axis=1, how='all')
        
        # The first column contains Position + Team name combined (e.g., "1Arsenal")
        # We need to split this into two separate columns
        if 'Team' in standings_df.columns:
            # Extract position (leading digits) and team name
            standings_df['Position'] = standings_df['Team'].astype(str).str.extract(r'^(\d+)')[0]
            standings_df['Team'] = standings_df['Team'].astype(str).str.replace(r'^\d+', '', regex=True)
            
            # Convert Position to numeric
            standings_df['Position'] = pd.to_numeric(standings_df['Position'], errors='coerce')
        
        # Rename columns to match expected format
        column_mapping = {
            'Goals For': 'GF',
            'Goals Against': 'GA',
            'Goal Difference': 'GD',
            'Form, Last 6 games, Oldest first': 'Form'
        }
        standings_df = standings_df.rename(columns=column_mapping)
        
        # Reorder columns to put Position first
        column_order = ['Position', 'Team', 'Played', 'Won', 'Drawn', 'Lost', 'GF', 'GA', 'GD', 'Points']
        
        # Add Form if it exists
        if 'Form' in standings_df.columns:
            column_order.append('Form')
        
        # Select only the columns we want, in the correct order
        standings_df = standings_df[column_order]
        
        # Convert numeric columns to proper data types
        numeric_cols = ['Position', 'Played', 'Won', 'Drawn', 'Lost', 'GF', 'GA', 'GD', 'Points']
        for col in numeric_cols:
            if col in standings_df.columns:
                standings_df[col] = pd.to_numeric(standings_df[col], errors='coerce')
        
        # Clean up Team names (remove extra whitespace)
        if 'Team' in standings_df.columns:
            standings_df['Team'] = standings_df['Team'].str.strip()
        
        # Clean up Form column - extract only W, L, D characters and take last 5
        if 'Form' in standings_df.columns:
            standings_df['Form'] = standings_df['Form'].astype(str).str.findall(r'[WLD]').str.join('').str[-5:]
        
        # Sort by Position to ensure correct order
        standings_df = standings_df.sort_values('Position').reset_index(drop=True)
        
        print(f"Successfully scraped {len(standings_df)} teams")
        print(f"Final columns: {standings_df.columns.tolist()}")
        print(f"\nSample data:")
        print(standings_df.head(3))
        
        return standings_df
        
    except Exception as e:
        print(f"Error during scraping: {e}")
        import traceback
        traceback.print_exc()
        return pd.DataFrame()