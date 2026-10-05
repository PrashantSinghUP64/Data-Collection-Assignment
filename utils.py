"""
utils.py — Shared utility functions for the Data Collection Pipeline.

Centralises JSON I/O and logging setup so that no module
duplicates these concerns.
"""
import json
import logging
import logging.handlers
from pathlib import Path
from typing import Any, Dict, List

from config import LOG_FILE, LOG_FORMAT, LOG_DATE_FORMAT


def get_logger(name: str) -> logging.Logger:
    """
    Returns a named logger that writes to both the console and a rotating
    log file (pipeline.log, max 1 MB, 3 back-ups).

    Args:
        name: Typically __name__ of the calling module.

    Returns:
        Configured Logger instance.
    """
    logger = logging.getLogger(name)

    # Avoid adding duplicate handlers when the module is imported multiple times
    if logger.handlers:
        return logger

    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(LOG_FORMAT, datefmt=LOG_DATE_FORMAT)

    # Console handler (INFO and above)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    # Rotating file handler (DEBUG and above)
    file_handler = logging.handlers.RotatingFileHandler(
        LOG_FILE, maxBytes=1_048_576, backupCount=3, encoding="utf-8"
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger


def load_json_file(filepath: str) -> List[Dict[str, Any]]:
    """
    Loads a JSON file and performs structural validation:
      - Root element must be a list.
      - Every element must be a dict (per-record validation).

    Args:
        filepath: Path to the JSON file.

    Returns:
        A validated list of dicts, or [] on any failure.
    """
    logger = get_logger(__name__)
    path = Path(filepath)

    if not path.exists():
        logger.error("File not found: '%s'. Run the data-collection step first.", filepath)
        return []

    if path.stat().st_size == 0:
        logger.error("File is empty: '%s'.", filepath)
        return []

    try:
        with open(path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
    except json.JSONDecodeError as exc:
        logger.error("JSON decode error in '%s': %s", filepath, exc)
        return []

    if not isinstance(data, list):
        logger.error(
            "Schema error in '%s': expected a JSON array, got %s.",
            filepath, type(data).__name__
        )
        return []

    # Per-record validation
    valid: List[Dict[str, Any]] = []
    for idx, record in enumerate(data):
        if not isinstance(record, dict):
            logger.warning(
                "Skipping non-dict record at index %d in '%s'.", idx, filepath
            )
            continue
        valid.append(record)

    logger.debug("Loaded %d valid records from '%s'.", len(valid), filepath)
    return valid


def save_json_file(filepath: str, data: Any, logger: logging.Logger) -> bool:
    """
    Saves data to a UTF-8 JSON file with 4-space indentation.

    Args:
        filepath: Destination path.
        data:     Serialisable Python object.
        logger:   Logger instance for error reporting.

    Returns:
        True on success, False on failure.
    """
    try:
        with open(filepath, "w", encoding="utf-8") as fh:
            json.dump(data, fh, indent=4, ensure_ascii=False)
        logger.info("Saved data to '%s'.", filepath)
        return True
    except (IOError, OSError) as exc:
        logger.error("Failed to write '%s': %s", filepath, exc)
        return False
