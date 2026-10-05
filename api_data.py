"""
api_data.py — Part A: API Data Collection

Fetches user records from the JSONPlaceholder API, extracts required fields
(Name, Username, Email, Company Name), and saves them to users.json.
"""
import json
import logging
from typing import List, Dict, Any

import requests

API_URL = "https://jsonplaceholder.typicode.com/users"
OUTPUT_FILE = "users.json"
TIMEOUT_SEC = 10
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


class APIClient:
    """Handles all communication with the JSONPlaceholder Users API."""

    def __init__(self) -> None:
        self.api_url = API_URL
        self.output_file = OUTPUT_FILE

    def fetch_users(self) -> List[Dict[str, Any]]:
        """Fetches raw user data from the API with layered exception handling."""
        try:
            response = requests.get(self.api_url, headers=HEADERS, timeout=TIMEOUT_SEC)

            if response.status_code != 200:
                logging.error(f"API returned HTTP {response.status_code}")
                response.raise_for_status()

            data = response.json()
            if not isinstance(data, list):
                logging.error("Unexpected API response format: expected a JSON array.")
                return []

            return data

        except requests.exceptions.HTTPError as e:
            logging.error(f"HTTP Error: {e}")
        except requests.exceptions.ConnectionError as e:
            logging.error(f"Connection Error: {e}")
        except requests.exceptions.Timeout as e:
            logging.error(f"Request timed out after {TIMEOUT_SEC}s: {e}")
        except requests.exceptions.RequestException as e:
            logging.error(f"Request failed: {e}")
        except ValueError as e:
            logging.error(f"JSON parse error: {e}")

        return []

    def process_users(self, users: List[Dict[str, Any]]) -> List[Dict[str, str]]:
        """
        Extracts Name, Username, Email, and Company Name from each raw user record.
        All four fields are retained in the saved output, matching the assignment spec.
        """
        processed: List[Dict[str, str]] = []
        print("\n[Task A1] User Records:")

        for user in users:
            if not isinstance(user, dict):
                continue

            name = str(user.get("name", "Unknown"))
            username = str(user.get("username", "Unknown"))
            email = str(user.get("email", "Unknown"))

            # Safe nested access for company
            company_info = user.get("company")
            company_name = (
                company_info.get("name", "Unknown")
                if isinstance(company_info, dict)
                else "Unknown"
            )

            print(
                f"  Name: {name} | Username: {username} | "
                f"Email: {email} | Company: {company_name}"
            )

            # All four required fields are stored
            processed.append({
                "name": name,
                "username": username,
                "email": email,
                "company": company_name,
            })

        return processed

    def save_data(self, data: List[Dict[str, str]]) -> None:
        """Persists processed user records to a UTF-8 JSON file."""
        try:
            with open(self.output_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            logging.info(f"[Task A5] Saved {len(data)} user records to '{self.output_file}'.")
        except IOError as e:
            logging.error(f"Failed to write '{self.output_file}': {e}")

    def execute(self) -> None:
        """Orchestrates the API data-collection workflow (Tasks A1–A5)."""
        print("--- Part A: API Data Collection ---")

        users = self.fetch_users()
        if not users:
            print("No user data retrieved. Check network connectivity.")
            return

        processed = self.process_users(users)

        # Task A2
        print(f"\n[Task A2] Total users fetched: {len(users)}")

        # Task A3
        companies = [u["company"] for u in processed if u["company"] != "Unknown"]
        print(f"\n[Task A3] All company names: {companies}")

        # Task A4
        print("\n[Task A4] Each user stored as a Python dict with: name, username, email, company.")

        # Task A5
        self.save_data(processed)


def fetch_api_data() -> None:
    """Public entry point used by main.py."""
    APIClient().execute()


if __name__ == "__main__":
    fetch_api_data()
