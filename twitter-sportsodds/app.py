import requests
import os
from dotenv import load_dotenv
import psycopg2
import json

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
url = f"https://api.the-odds-api.com/v4/sports/baseball_mlb/odds/?apiKey={api_key}&regions=us&markets=h2h,spreads&oddsFormat=american&bookmakers=draftkings,>"

# Fetch API data
api_data = get_api_data(url)



# Database connection parameters
conn_params = {
    'dbname': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'port': int(os.getenv('DB_PORT', 25060)),
    'sslmode': 'require'
}

try:
    # Connect to the PostgreSQL server
    conn = psycopg2.connect(**conn_params)
    cur = conn.cursor()

    # Insert data into the database
    if api_data:
        for item in api_data:
            # Convert the entire item to JSON and store it in the data column
            # Ensure your item is a dictionary that can be converted into JSON
            item_json = json.dumps(item)
            
            # Execute the INSERT statement
            cur.execute("""
                INSERT INTO odds_data (data) 
                VALUES (%s::jsonb)
            """, (item_json,))

        # Commit the transaction
        conn.commit()
        print("Data inserted successfully.")
    else:
        print("No data retrieved from the API.")
except (Exception, psycopg2.DatabaseError) as error:
    print(f"Failed to insert data: {error}")
finally:
    # Close the cursor and connection
    if cur:
        cur.close()
    if conn:
        conn.close()

