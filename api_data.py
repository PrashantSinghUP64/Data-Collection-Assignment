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

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

def fetch_users() -> List[Dict[str, Any]]:
    """Fetches user data from the JSONPlaceholder API."""
    try:
        response = requests.get(API_URL, timeout=TIMEOUT_SEC)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to fetch data from API: {e}")
        return []
    except ValueError as e:
        logging.error(f"Failed to parse JSON response: {e}")
        return []

def process_and_display_users(users: List[Dict[str, Any]]) -> List[Dict[str, str]]:
    """Processes user data and extracts relevant fields."""
    processed_users = []
    print("\n[Task A1] User Records:")
    for user in users:
        name = user.get('name', 'Unknown')
        username = user.get('username', 'Unknown')
        email = user.get('email', 'Unknown')
        company_name = user.get('company', {}).get('name', 'Unknown')
        
        print(f"Name: {name}, Username: {username}, Email: {email}, Company: {company_name}")
        
        processed_users.append({
            "name": name,
            "email": email,
            "company": company_name
        })
    return processed_users

def fetch_api_data() -> None:
    """Main execution function for Part A."""
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
    
    # Task A4: Processed dicts created above
    print("\n[Task A4] Created processed user list of dictionaries.")
        
    # Task A5: Save into JSON
    try:
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            json.dump(processed_users, f, indent=4)
        print(f"[Task A5] Saved processed API data to {OUTPUT_FILE}.\n")
    except IOError as e:
        logging.error(f"Failed to save {OUTPUT_FILE}: {e}")

if __name__ == "__main__":
    fetch_api_data()
