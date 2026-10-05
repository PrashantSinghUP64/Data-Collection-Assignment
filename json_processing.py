"""
json_processing.py — Part C: JSON Processing

Loads users.json and books.json, filters/aggregates records,
and writes a combined summary to report.json.
"""
import json
import logging
from typing import List, Dict, Any

from utils import load_json_file  # shared utility — eliminates code duplication

USERS_FILE = "users.json"
BOOKS_FILE = "books.json"
REPORT_FILE = "report.json"

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


def process_json_data() -> None:
    """Loads, validates, filters, and aggregates user and book data (Tasks C1–C4)."""
    print("--- Part C: JSON Processing ---")

    users: List[Dict[str, Any]] = load_json_file(USERS_FILE)
    books: List[Dict[str, Any]] = load_json_file(BOOKS_FILE)

    if not users or not books:
        print("Required JSON data is missing. Run Parts A and B first.")
        return

    # Task C1 — Record counts
    print(f"\n[Task C1] Total user records : {len(users)}")
    print(f"[Task C1] Total book records  : {len(books)}")

    # Task C2 — Books with rating > 4
    print("\n[Task C2] Books with rating > 4:")
    high_rated = [b["title"] for b in books if b.get("rating", 0) > 4]
    if high_rated:
        for title in high_rated:
            print(f"  - {title}")
    else:
        print("  None found.")

    # Task C3 — Users whose company name contains "Group"
    print("\n[Task C3] Users in companies containing 'Group':")
    group_users = [u for u in users if "Group" in u.get("company", "")]
    if group_users:
        for u in group_users:
            print(f"  - {u.get('name')} | {u.get('company')}")
    else:
        print("  None found.")

    # Task C4 — Combine into a summary report and save
    avg_price: float = (
        round(sum(b.get("numeric_price", 0.0) for b in books) / len(books), 2)
        if books else 0.0
    )

    report: Dict[str, Any] = {
        "total_users": len(users),
        "total_books": len(books),
        "average_book_price": avg_price,
        "high_rated_books_count": len(high_rated),
        "users_in_group_companies": len(group_users),
    }

    try:
        with open(REPORT_FILE, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=4, ensure_ascii=False)
        logging.info(f"[Task C4] Saved combined report to '{REPORT_FILE}': {report}")
    except IOError as e:
        logging.error(f"Failed to write '{REPORT_FILE}': {e}")


if __name__ == "__main__":
    process_json_data()
