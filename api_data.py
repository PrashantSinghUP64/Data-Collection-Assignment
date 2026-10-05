"""
api_data.py — Part A: API Data Collection

Fetches user records from the JSONPlaceholder REST API, validates and
extracts the four required fields (Name, Username, Email, Company Name),
then persists the cleaned dataset to users.json.
"""
from typing import Any, Dict, List

import requests

import config
from utils import get_logger, save_json_file

logger = get_logger(__name__)


class APIClient:
    """
    Handles all communication with the JSONPlaceholder Users API.

    Responsibilities:
        - Fetching raw JSON from the remote endpoint.
        - Validating the HTTP response and the JSON schema.
        - Extracting and sanitising the four required user fields.
        - Persisting the processed dataset.
    """

    # Required fields that every processed user record must contain
    REQUIRED_FIELDS: tuple = ("name", "username", "email", "company")

    def __init__(self) -> None:
        self.api_url: str = config.API_URL
        self.output_file: str = config.USERS_FILE

    # ------------------------------------------------------------------ #
    #  Network Layer
    # ------------------------------------------------------------------ #

    def fetch_users(self) -> List[Dict[str, Any]]:
        """
        Fetches the raw user array from the API.

        Returns:
            A list of raw user dicts, or [] on any network / parse failure.
        """
        logger.info("Fetching users from: %s", self.api_url)
        try:
            response = requests.get(
                self.api_url,
                headers=config.REQUEST_HEADERS,
                timeout=config.REQUEST_TIMEOUT,
            )

            # Explicit HTTP status validation
            if response.status_code != 200:
                logger.error(
                    "API returned HTTP %d — expected 200.", response.status_code
                )
                response.raise_for_status()

            payload = response.json()

            # Schema validation: root must be a list
            if not isinstance(payload, list):
                logger.error(
                    "Unexpected API response type: %s — expected list.",
                    type(payload).__name__,
                )
                return []

            logger.info("Fetched %d raw user records.", len(payload))
            return payload

        except requests.exceptions.HTTPError as exc:
            logger.error("HTTP error: %s", exc)
        except requests.exceptions.ConnectionError as exc:
            logger.error("Connection error (check network): %s", exc)
        except requests.exceptions.Timeout:
            logger.error("Request timed out after %ds.", config.REQUEST_TIMEOUT)
        except requests.exceptions.RequestException as exc:
            logger.error("Request failed: %s", exc)
        except ValueError as exc:
            logger.error("JSON parse error: %s", exc)

        return []

    # ------------------------------------------------------------------ #
    #  Data Processing
    # ------------------------------------------------------------------ #

    def _extract_company_name(self, user: Dict[str, Any]) -> str:
        """Safely traverses the nested company object."""
        company = user.get("company")
        if isinstance(company, dict):
            return str(company.get("name", "Unknown")).strip()
        return "Unknown"

    def process_users(self, users: List[Dict[str, Any]]) -> List[Dict[str, str]]:
        """
        Extracts and sanitises the four required fields from each raw user record.
        Skips malformed records and logs a warning for each one.

        Args:
            users: Raw user dicts returned by the API.

        Returns:
            A list of clean user dicts containing name, username, email, company.
        """
        processed: List[Dict[str, str]] = []

        print("\n[Task A1] User Records:")
        for idx, user in enumerate(users):
            if not isinstance(user, dict):
                logger.warning("Skipping non-dict record at index %d.", idx)
                continue

            record: Dict[str, str] = {
                "name":     str(user.get("name", "Unknown")).strip(),
                "username": str(user.get("username", "Unknown")).strip(),
                "email":    str(user.get("email", "Unknown")).strip(),
                "company":  self._extract_company_name(user),
            }

            # Validate that no required field is empty after extraction
            for field in self.REQUIRED_FIELDS:
                if not record[field]:
                    logger.warning(
                        "Record %d has empty field '%s' — defaulting to 'Unknown'.",
                        idx, field,
                    )
                    record[field] = "Unknown"

            print(
                f"  Name: {record['name']:<28} | Username: {record['username']:<20} "
                f"| Email: {record['email']:<32} | Company: {record['company']}"
            )
            processed.append(record)

        return processed

    # ------------------------------------------------------------------ #
    #  Orchestration
    # ------------------------------------------------------------------ #

    def execute(self) -> None:
        """Runs the complete API data-collection workflow (Tasks A1–A5)."""
        print("=" * 60)
        print("  Part A: API Data Collection")
        print("=" * 60)

        raw_users = self.fetch_users()
        if not raw_users:
            logger.error("No user data retrieved. Aborting Part A.")
            return

        processed = self.process_users(raw_users)

        # Task A2 — Total user count
        print(f"\n[Task A2] Total users fetched: {len(raw_users)}")

        # Task A3 — All company names
        companies = [u["company"] for u in processed if u["company"] != "Unknown"]
        print(f"\n[Task A3] Company names:\n  {companies}")

        # Task A4 — Dict structure confirmation
        print(
            "\n[Task A4] Each record is a Python dict with keys: "
            + ", ".join(self.REQUIRED_FIELDS)
        )

        # Task A5 — Persist
        if save_json_file(self.output_file, processed, logger):
            print(f"\n[Task A5] Saved {len(processed)} records to '{self.output_file}'.")


def fetch_api_data() -> None:
    """Public entry point consumed by main.py."""
    APIClient().execute()


if __name__ == "__main__":
    fetch_api_data()
