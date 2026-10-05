"""
Module for analyzing user and book data and producing summary reports.
"""
import json
import logging
from typing import List, Dict, Any

USERS_FILE = 'users.json'
BOOKS_FILE = 'books.json'

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

def load_json_file(filepath: str) -> List[Dict[str, Any]]:
    """Loads and returns data from a JSON file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logging.error(f"Failed to load {filepath}: {e}")
        return []

def analyze_users(users: List[Dict[str, Any]]) -> None:
    """Analyzes and prints user statistics."""
    print("\n[User Analysis]")
    print(f"- Total Users: {len(users)}")
    
    companies = [user.get('company') for user in users if isinstance(user, dict) and user.get('company') and user.get('company') != 'Unknown']
    unique_companies = list(set(companies))
    print(f"- Unique Companies: {len(unique_companies)}")
    
    # Sort alphabetically, case-insensitive
    top_5_companies = sorted(unique_companies, key=lambda x: str(x).lower())[:5]
    print(f"- Top 5 Companies (Alphabetically): {', '.join(str(c) for c in top_5_companies)}")

def analyze_books(books: List[Dict[str, Any]]) -> None:
    """Analyzes and prints book statistics."""
    print("\n[Book Analysis]")
    avg_price = sum(b.get('numeric_price', 0.0) for b in books) / len(books) if books else 0.0
    print(f"- Average Price: £{avg_price:.2f}")
    
    if books:
        max_rating = max(book.get('rating', 0) for book in books)
        highest_rated = [book['title'] for book in books if book.get('rating', 0) == max_rating]
        print(f"- Highest Rated Books (Rating {max_rating}):")
        for title in highest_rated:
            print(f"  * {title}")
    
    # Initialize all rating categories (1-5) to 0
    rating_counts: Dict[int, int] = {5: 0, 4: 0, 3: 0, 2: 0, 1: 0}
    for book in books:
        r = book.get('rating', 0)
        if r in rating_counts:
            rating_counts[r] += 1
        
    print("- Number of Books in Each Rating Category:")
    for rating in range(5, 0, -1):
        print(f"  * Rating {rating}: {rating_counts[rating]} books")

def analyze_data() -> None:
    """Main execution function for Part D."""
    print("--- Part D: Data Analysis ---")
    
    users = load_json_file(USERS_FILE)
    books = load_json_file(BOOKS_FILE)
    
    if not users or not books:
        print("Required JSON files missing or corrupt. Run data collection first.")
        return
        
    if not isinstance(users, list) or not isinstance(books, list):
        logging.error("Invalid JSON schema: Expected a list of records.")
        return

    analyze_users(users)
    analyze_books(books)
    print()

if __name__ == "__main__":
    analyze_data()
