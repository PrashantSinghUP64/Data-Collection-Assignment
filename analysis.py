"""
Module for robustly analyzing user and book datasets using standard Python structures.
"""
import json
import logging
from typing import List, Dict, Any
from collections import Counter

USERS_FILE = 'users.json'
BOOKS_FILE = 'books.json'

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

def load_json_file(filepath: str) -> List[Dict[str, Any]]:
    """Loads, decodes, and returns JSON array data securely."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        logging.error(f"Failed to load {filepath}: File does not exist.")
        return []
    except json.JSONDecodeError as e:
        logging.error(f"JSON schema parsing failed in {filepath}: {e}")
        return []

def analyze_users(users: List[Dict[str, Any]]) -> None:
    """Computes analytical metrics securely on the Users dataset."""
    print("\n[User Analysis]")
    
    # 1. Total Users
    print(f"- Total Users: {len(users)}")
    
    # Filter valid companies and ensure rigorous data cleaning
    companies = [
        user.get('company').strip() for user in users 
        if isinstance(user, dict) and user.get('company') and user.get('company') != 'Unknown'
    ]
    
    # 2. Unique Companies
    unique_companies = list(set(companies))
    print(f"- Unique Companies: {len(unique_companies)}")
    
    # 3. Top 5 Companies (Alphabetically) using safe case-insensitive sorting
    top_5_companies = sorted(unique_companies, key=lambda x: str(x).lower())[:5]
    print(f"- Top 5 Companies (Alphabetically): {', '.join(str(c) for c in top_5_companies)}")

def analyze_books(books: List[Dict[str, Any]]) -> None:
    """Computes analytical metrics securely on the Books dataset."""
    print("\n[Book Analysis]")
    
    if not books:
        print("No book data available for analysis.")
        return

    # 1. Average Price (rounded mathematically to 2 decimals)
    total_price = sum(b.get('numeric_price', 0.0) for b in books)
    avg_price = round(total_price / len(books), 2)
    print(f"- Average Price: £{avg_price:.2f}")
    
    # 2. Highest Rated Books
    max_rating = max((book.get('rating', 0) for book in books), default=0)
    highest_rated = [book.get('title', 'Unknown') for book in books if book.get('rating', 0) == max_rating]
    print(f"- Highest Rated Books (Rating {max_rating}):")
    for title in highest_rated:
        print(f"  * {title}")
    
    # 3. Number of Books in Each Rating Category
    # Utilizing collections.Counter for Pythonic and efficient frequency counting
    rating_frequencies = Counter(book.get('rating', 0) for book in books)
    
    print("- Number of Books in Each Rating Category:")
    # Loop over 5 to 1 inclusive to ensure no valid category is omitted, even if 0
    for rating in range(5, 0, -1):
        count = rating_frequencies.get(rating, 0)
        print(f"  * Rating {rating}: {count} books")

def analyze_data() -> None:
    """Main execution block to orchestrate data analysis steps."""
    print("--- Part D: Data Analysis ---")
    
    users = load_json_file(USERS_FILE)
    books = load_json_file(BOOKS_FILE)
    
    if not users or not books:
        print("Required JSON files missing or corrupt. Run data collection first.")
        return
        
    if not isinstance(users, list) or not isinstance(books, list):
        logging.error("Invalid JSON schema: Expected an array/list of records.")
        return

    analyze_users(users)
    analyze_books(books)
    print()

if __name__ == "__main__":
    analyze_data()
