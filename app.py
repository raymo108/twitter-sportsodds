import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Retrieve API key from environment
api_key = os.getenv('ODDS_API_KEY')

def get_api_data(url):
    try:
        # Sending a GET request to the API
        response = requests.get(url)
        
        # Check if the request was successful
        response.raise_for_status()
        
        # Return the JSON data from the response
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        # Handle HTTP errors (e.g., response 4xx, 5xx)
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        # Handle other possible errors
        print(f"An error occurred: {err}")

# Construct the API URL with appropriate parameters
url = f"https://api.the-odds-api.com/v4/sports/baseball_mlb/odds/?apiKey={api_key}&regions=us&markets=h2h,spreads&oddsFormat=american&bookmakers=draftkings,fanduel,barstool,betmgm,williamhill_us,espnbet"

# Fetch API data
api_data = get_api_data(url)
if api_data:
    print(api_data)
else:
    print("Failed to retrieve data.")
