"""
json_processing.py — Part C: JSON Processing

Loads, validates, filters, and aggregates the user and book datasets.
Writes a structured summary report to report.json.
"""
from typing import Any, Dict, List

import config
from utils import get_logger, load_json_file, save_json_file

logger = get_logger(__name__)


def _validate_user_record(record: Dict[str, Any], idx: int) -> bool:
    """Returns True if a user record contains all expected fields."""
    required = {"name", "username", "email", "company"}
    missing = required - record.keys()
    if missing:
        logger.warning("User record %d is missing fields: %s", idx, missing)
        return False
    return True


def _validate_book_record(record: Dict[str, Any], idx: int) -> bool:
    """Returns True if a book record contains all expected fields."""
    required = {"title", "price", "numeric_price", "rating"}
    missing = required - record.keys()
    if missing:
        logger.warning("Book record %d is missing fields: %s", idx, missing)
        return False
    return True


def process_json_data() -> None:
    """Executes the JSON processing workflow (Tasks C1–C4)."""
    print("=" * 60)
    print("  Part C: JSON Processing")
    print("=" * 60)

    users: List[Dict[str, Any]] = load_json_file(config.USERS_FILE)
    books: List[Dict[str, Any]] = load_json_file(config.BOOKS_FILE)

    if not users or not books:
        logger.error("Required data files are missing — run Parts A and B first.")
        return

    # Deep per-record schema validation
    valid_users = [u for i, u in enumerate(users) if _validate_user_record(u, i)]
    valid_books = [b for i, b in enumerate(books) if _validate_book_record(b, i)]

    # Task C1 — Record counts
    print(f"\n[Task C1]")
    print(f"  Valid user records : {len(valid_users)}")
    print(f"  Valid book records : {len(valid_books)}")

    # Task C2 — Books with rating > 4
    high_rated: List[str] = [
        b["title"] for b in valid_books if b.get("rating", 0) > 4
    ]
    print(f"\n[Task C2] Books with rating > 4 ({len(high_rated)} found):")
    for title in high_rated:
        print(f"  - {title}")
    if not high_rated:
        print("  None found.")

    # Task C3 — Users whose company name contains "Group"
    group_users = [
        u for u in valid_users if "Group" in u.get("company", "")
    ]
    print(f"\n[Task C3] Users in 'Group' companies ({len(group_users)} found):")
    for u in group_users:
        print(f"  - {u.get('name')} | {u.get('company')}")
    if not group_users:
        print("  None found.")

    # Task C4 — Build and save the combined summary report
    prices = [b.get("numeric_price", 0.0) for b in valid_books]
    avg_price: float = round(sum(prices) / len(prices), 2) if prices else 0.0

    report: Dict[str, Any] = {
        "total_users": len(valid_users),
        "total_books": len(valid_books),
        "average_book_price_gbp": avg_price,
        "books_rated_above_4": len(high_rated),
        "users_in_group_companies": len(group_users),
        "high_rated_titles": high_rated,
    }

    if save_json_file(config.REPORT_FILE, report, logger):
        print(f"\n[Task C4] Saved combined report to '{config.REPORT_FILE}'.")
        print(f"  → {report}")


if __name__ == "__main__":
    process_json_data()
