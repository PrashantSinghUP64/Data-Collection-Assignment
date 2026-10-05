"""
Module for fetching and processing user data from an external API.
Implemented using Object-Oriented Programming (OOP) for enterprise scalability.
"""
import json
import logging
from typing import List, Dict, Any
import requests

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

class APIClient:
    """Client for fetching and processing user data securely."""
    
    def __init__(self) -> None:
        self.api_url = "https://jsonplaceholder.typicode.com/users"
        self.output_file = "users.json"
        self.timeout_sec = 10
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }

    def fetch_users(self) -> List[Dict[str, Any]]:
        """Fetches user data from the API securely with robust error handling."""
        try:
            response = requests.get(self.api_url, headers=self.headers, timeout=self.timeout_sec)
            
            if response.status_code == 200:
                return response.json()
            else:
                logging.error(f"API returned non-200 status code: {response.status_code}")
                response.raise_for_status()
                return []
                
        except requests.exceptions.HTTPError as e:
            logging.error(f"HTTP Error: {e}")
        except requests.exceptions.ConnectionError as e:
            logging.error(f"Connection Error: {e}")
        except requests.exceptions.Timeout as e:
            logging.error(f"Timeout Error: {e}")
        except requests.exceptions.RequestException as e:
            logging.error(f"Request Error: {e}")
        except ValueError as e:
            logging.error(f"JSON Parse Error: {e}")
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            
        return []

    def process_and_display_users(self, users: List[Dict[str, Any]]) -> List[Dict[str, str]]:
        """Processes user data and extracts relevant fields."""
        processed_users = []
        print("\n[Task A1] User Records:")
        
        for user in users:
            if not isinstance(user, dict):
                continue
                
            name = user.get('name', 'Unknown')
            username = user.get('username', 'Unknown')
            email = user.get('email', 'Unknown')
            
            company_info = user.get('company')
            company_name = company_info.get('name', 'Unknown') if isinstance(company_info, dict) else 'Unknown'
            
            print(f"Name: {name}, Username: {username}, Email: {email}, Company: {company_name}")
            
            processed_users.append({
                "name": name,
                "email": email,
                "company": company_name
            })
            
        return processed_users

    def save_data(self, data: List[Dict[str, str]]) -> None:
        """Saves processed data to a JSON file."""
        try:
            with open(self.output_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4)
            print(f"[Task A5] Successfully saved processed API data to {self.output_file}.\n")
        except IOError as e:
            logging.error(f"Failed to save {self.output_file}: {e}")

    def execute(self) -> None:
        """Main execution workflow for API Data Collection."""
        print("--- Part A: API Data Collection ---")
        users = self.fetch_users()
        
        if not users:
            print("No user data retrieved.")
            return

        processed_users = self.process_and_display_users(users)
        
        print(f"\n[Task A2] Total Users: {len(users)}")
        
        company_names = [u['company'] for u in processed_users if u['company'] != 'Unknown']
        print(f"\n[Task A3] Company Names: {company_names}")
        print("\n[Task A4] Created Python dictionary for each user containing name, email, and company.")
            
        self.save_data(processed_users)

def fetch_api_data() -> None:
    client = APIClient()
    client.execute()

if __name__ == "__main__":
    fetch_api_data()
