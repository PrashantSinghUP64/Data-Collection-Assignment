"""
Module for scraping book information from books.toscrape.com.
"""
import json
import logging
import re
from typing import List, Dict, Any
import requests
from bs4 import BeautifulSoup

URL = "https://books.toscrape.com/"
OUTPUT_FILE = "books.json"
TIMEOUT_SEC = 10

RATING_MAP = {
    "One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5
}

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

def fetch_html() -> str:
    """Fetches the HTML content from the website."""
    try:
        response = requests.get(URL, timeout=TIMEOUT_SEC)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to fetch data from website: {e}")
        return ""

def extract_price(price_text: str) -> float:
    """Extracts the numerical value from a price string."""
    match = re.search(r"[\d\.]+", price_text)
    if match:
        try:
            return float(match.group())
        except ValueError:
            pass
    return 0.0

def parse_books(html_content: str) -> List[Dict[str, Any]]:
    """Parses book data from HTML content."""
    soup = BeautifulSoup(html_content, 'html.parser')
    articles = soup.find_all('article', class_='product_pod')
    
    book_list = []
    for article in articles:
        try:
            title_elem = article.h3.a
            title = title_elem['title'] if title_elem else 'Unknown'
            
            price_elem = article.find('p', class_='price_color')
            price_text = price_elem.text if price_elem else '0.0'
            price_num = extract_price(price_text)
            
            rating_elem = article.find('p', class_='star-rating')
            rating_class = rating_elem['class'][1] if rating_elem and len(rating_elem['class']) > 1 else 'None'
            rating_num = RATING_MAP.get(rating_class, 0)
            
            book_list.append({
                "title": title,
                "price": price_text, 
                "numeric_price": price_num, 
                "rating": rating_num
            })
        except (AttributeError, KeyError) as e:
            logging.warning(f"Error parsing a book article: {e}")
            continue
            
    return book_list

def scrape_book_data() -> None:
    """Main execution function for Part B."""
    print("--- Part B: Web Scraping ---")
    html_content = fetch_html()
    
    if not html_content:
        print("No HTML content retrieved.")
        return
        
    book_list = parse_books(html_content)
    print(f"\n[Task B1 & B2 & B3] Extracted {len(book_list)} books.")
    
    if book_list:
        most_expensive = max(book_list, key=lambda x: x['numeric_price'])
        least_expensive = min(book_list, key=lambda x: x['numeric_price'])
        avg_price = sum(b['numeric_price'] for b in book_list) / len(book_list)
        
        print("\n[Task B4]")
        print(f"Most Expensive Book: {most_expensive['title']} at {most_expensive['price']}")
        print(f"Least Expensive Book: {least_expensive['title']} at {least_expensive['price']}")
        print(f"Average Book Price: £{avg_price:.2f}")
        
    try:
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            json.dump(book_list, f, indent=4)
        print(f"\n[Task B5] Saved extracted data to {OUTPUT_FILE}.\n")
    except IOError as e:
        logging.error(f"Failed to save {OUTPUT_FILE}: {e}")

if __name__ == "__main__":
    scrape_book_data()
