"""
Module for fetching and processing user data from an external API.
"""
import json
import logging
from typing import List, Dict, Any
import requests

API_URL = "https://jsonplaceholder.typicode.com/users"
OUTPUT_FILE = "users.json"
TIMEOUT_SEC = 10

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

def fetch_users() -> List[Dict[str, Any]]:
    """Fetches user data from the JSONPlaceholder API securely with error handling."""
    try:
        response = requests.get(API_URL, headers=HEADERS, timeout=TIMEOUT_SEC)
        
        # Explicitly check for successful HTTP response code
        if response.status_code == 200:
            return response.json()
        else:
            logging.error(f"API returned non-200 status code: {response.status_code}")
            response.raise_for_status()
            return []
            
    except requests.exceptions.HTTPError as e:
        logging.error(f"HTTP Error fetching data from API: {e}")
        return []
    except requests.exceptions.ConnectionError as e:
        logging.error(f"Connection Error fetching data from API: {e}")
        return []
    except requests.exceptions.Timeout as e:
        logging.error(f"Timeout Error fetching data from API: {e}")
        return []
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to fetch data from API: {e}")
        return []
    except ValueError as e:
        logging.error(f"Failed to parse JSON response: {e}")
        return []
    except Exception as e:
        logging.error(f"Unexpected error occurred: {e}")
        return []

def process_and_display_users(users: List[Dict[str, Any]]) -> List[Dict[str, str]]:
    """Processes user data, displays specified fields, and returns a sanitized list."""
    processed_users = []
    print("\n[Task A1] User Records:")
    for user in users:
        if not isinstance(user, dict):
            continue
            
        name = user.get('name', 'Unknown')
        username = user.get('username', 'Unknown')
        email = user.get('email', 'Unknown')
        
        # Safe traversal for nested dictionaries
        company_info = user.get('company')
        if isinstance(company_info, dict):
            company_name = company_info.get('name', 'Unknown')
        else:
            company_name = 'Unknown'
        
        print(f"Name: {name}, Username: {username}, Email: {email}, Company: {company_name}")
        
        processed_users.append({
            "name": name,
            "email": email,
            "company": company_name
        })
        
    return processed_users

def fetch_api_data() -> None:
    """Main execution block to manage data pipeline for the API segment."""
    print("--- Part A: API Data Collection ---")
    users = fetch_users()
    
    if not users:
        print("No user data retrieved.")
        return

    processed_users = process_and_display_users(users)
    
    # Task A2: Count total number of users
    print(f"\n[Task A2] Total Users: {len(users)}")
    
    # Task A3: Extract all company names
    company_names = [u['company'] for u in processed_users if u['company'] != 'Unknown']
    print(f"\n[Task A3] Company Names: {company_names}")
    
    # Task A4: The python dictionary was created dynamically inside process_and_display_users
    print("\n[Task A4] Created Python dictionary for each user containing name, email, and company.")
        
    # Task A5: Save into users.json securely
    try:
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            json.dump(processed_users, f, indent=4)
        print(f"[Task A5] Successfully saved processed API data to {OUTPUT_FILE}.\n")
    except IOError as e:
        logging.error(f"Failed to save {OUTPUT_FILE}: {e}")

if __name__ == "__main__":
    fetch_api_data()
