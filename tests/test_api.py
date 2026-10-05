"""
tests/test_api.py — Unit tests for api_data.py

Tests cover:
  - Successful API response processing
  - Extraction of all four required fields (name, username, email, company)
  - Handling of malformed/missing records
  - Empty API response handling
"""
import sys
import os
import unittest
from unittest.mock import MagicMock, patch

# Ensure the parent directory is on the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api_data import APIClient


SAMPLE_USERS = [
    {
        "id": 1,
        "name": "Leanne Graham",
        "username": "Bret",
        "email": "Sincere@april.biz",
        "company": {"name": "Romaguera-Crona", "catchPhrase": "Multi-layered client-server"}
    },
    {
        "id": 2,
        "name": "Ervin Howell",
        "username": "Antonette",
        "email": "Shanna@melissa.tv",
        "company": {"name": "Deckow-Crist", "catchPhrase": "Proactive didactic"}
    },
]


class TestAPIClientProcessUsers(unittest.TestCase):
    """Tests for APIClient.process_users()"""

    def setUp(self) -> None:
        self.client = APIClient()

    def test_all_four_fields_extracted(self) -> None:
        """All four required fields must be present in each processed record."""
        result = self.client.process_users(SAMPLE_USERS)
        for record in result:
            self.assertIn("name", record)
            self.assertIn("username", record)
            self.assertIn("email", record)
            self.assertIn("company", record)

    def test_correct_values_extracted(self) -> None:
        """Field values must match the raw API data."""
        result = self.client.process_users(SAMPLE_USERS)
        self.assertEqual(result[0]["name"], "Leanne Graham")
        self.assertEqual(result[0]["username"], "Bret")
        self.assertEqual(result[0]["email"], "Sincere@april.biz")
        self.assertEqual(result[0]["company"], "Romaguera-Crona")

    def test_correct_count(self) -> None:
        """The processed list must contain one entry per valid raw user."""
        result = self.client.process_users(SAMPLE_USERS)
        self.assertEqual(len(result), len(SAMPLE_USERS))

    def test_non_dict_records_skipped(self) -> None:
        """Non-dict entries in the raw list must be silently skipped."""
        mixed = [SAMPLE_USERS[0], "invalid_string", None, 42]
        result = self.client.process_users(mixed)
        self.assertEqual(len(result), 1)

    def test_empty_input_returns_empty_list(self) -> None:
        """An empty input list must produce an empty output."""
        result = self.client.process_users([])
        self.assertEqual(result, [])

    def test_missing_company_defaults_to_unknown(self) -> None:
        """A record with no company dict must use 'Unknown' as the company."""
        user_no_company = [{"name": "Test", "username": "t", "email": "t@t.com", "company": None}]
        result = self.client.process_users(user_no_company)
        self.assertEqual(result[0]["company"], "Unknown")

    def test_nested_company_name_extracted(self) -> None:
        """Company name must be extracted from the nested 'company.name' field."""
        result = self.client.process_users(SAMPLE_USERS)
        self.assertEqual(result[1]["company"], "Deckow-Crist")

    @patch("api_data.requests.get")
    def test_fetch_users_success(self, mock_get: MagicMock) -> None:
        """fetch_users() must return the parsed list on HTTP 200."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = SAMPLE_USERS
        mock_get.return_value = mock_response

        result = self.client.fetch_users()
        self.assertEqual(len(result), 2)

    @patch("api_data.requests.get")
    def test_fetch_users_non_200_returns_empty(self, mock_get: MagicMock) -> None:
        """fetch_users() must return [] on a non-200 HTTP response."""
        import requests
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("404")
        mock_get.return_value = mock_response

        result = self.client.fetch_users()
        self.assertEqual(result, [])

    @patch("api_data.requests.get")
    def test_fetch_users_connection_error_returns_empty(self, mock_get: MagicMock) -> None:
        """fetch_users() must return [] on a ConnectionError."""
        import requests
        mock_get.side_effect = requests.exceptions.ConnectionError("down")

        result = self.client.fetch_users()
        self.assertEqual(result, [])

    @patch("api_data.requests.get")
    def test_fetch_users_timeout_returns_empty(self, mock_get: MagicMock) -> None:
        """fetch_users() must return [] on a Timeout."""
        import requests
        mock_get.side_effect = requests.exceptions.Timeout()

        result = self.client.fetch_users()
        self.assertEqual(result, [])


if __name__ == "__main__":
    unittest.main()
