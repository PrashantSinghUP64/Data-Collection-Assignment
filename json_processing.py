"""
Module for loading, processing, and aggregating JSON datasets.
"""
import json
import logging
from typing import List, Dict, Any

USERS_FILE = 'users.json'
BOOKS_FILE = 'books.json'
REPORT_FILE = 'report.json'

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

def load_json_file(filepath: str) -> List[Dict[str, Any]]:
    """Loads and returns data from a JSON file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        logging.error(f"File not found: {filepath}. Please generate it first.")
        return []
    except json.JSONDecodeError as e:
        logging.error(f"Error decoding JSON from {filepath}: {e}")
        return []
    except Exception as e:
        logging.error(f"Unexpected error occurred loading {filepath}: {e}")
        return []

def process_json_data() -> None:
    """Main execution function for Part C."""
    print("--- Part C: JSON Processing ---")
    
    users = load_json_file(USERS_FILE)
    books = load_json_file(BOOKS_FILE)
    
    if not users or not books:
        print("Missing required JSON data. Please run tasks A and B first.")
        return
        
    if not isinstance(users, list) or not isinstance(books, list):
        logging.error("Invalid JSON schema: Root element must be a list.")
        return
        
    print(f"\n[Task C1] Total Users Records: {len(users)}")
    print(f"[Task C1] Total Books Records: {len(books)}")
    
    print("\n[Task C2] Books with rating greater than 4:")
    high_rating_books = [book['title'] for book in books if book.get('rating', 0) > 4]
    for title in high_rating_books:
        print(f"- {title}")
        
    print("\n[Task C3] Users in companies containing 'Group':")
    group_users = [user for user in users if "Group" in user.get('company', '')]
    for user in group_users:
        print(f"- {user.get('name')} ({user.get('company')})")
        
    avg_price = sum(b.get('numeric_price', 0) for b in books) / len(books) if books else 0.0
    
    report = {
        "total_users": len(users),
        "total_books": len(books),
        "average_price": round(avg_price, 2)
    }
    
    try:
        with open(REPORT_FILE, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=4)
        print(f"\n[Task C4] Saved combined report to {REPORT_FILE}: {report}\n")
    except IOError as e:
        logging.error(f"Failed to save {REPORT_FILE}: {e}")

if __name__ == "__main__":
    process_json_data()
