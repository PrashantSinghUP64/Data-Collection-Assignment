"""
Shared utility module for common data-loading and validation operations.
Eliminates duplicate code across modules.
"""
import json
import logging
from typing import List, Dict, Any

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


def load_json_file(filepath: str) -> List[Dict[str, Any]]:
    """
    Loads a JSON file and validates that the root element is a list.
    Also performs per-record validation to ensure each element is a dict.

    Args:
        filepath: Path to the JSON file.

    Returns:
        A validated list of dictionaries, or an empty list on failure.
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        if not isinstance(data, list):
            logging.error(f"Invalid schema in '{filepath}': root element must be a list.")
            return []

        # Per-record validation
        valid_records = []
        for i, record in enumerate(data):
            if not isinstance(record, dict):
                logging.warning(f"Skipping invalid record at index {i} in '{filepath}': expected dict.")
                continue
            valid_records.append(record)

        return valid_records

    except FileNotFoundError:
        logging.error(f"File not found: '{filepath}'. Please generate it first.")
        return []
    except json.JSONDecodeError as e:
        logging.error(f"JSON decode error in '{filepath}': {e}")
        return []
