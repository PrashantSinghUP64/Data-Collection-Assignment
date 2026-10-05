"""
Module for securely scraping book information from books.toscrape.com using BeautifulSoup.
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

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

RATING_MAP = {
    "One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5
}

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

def fetch_html() -> str:
    """Fetches the HTML content from the website with explicit validation."""
    try:
        response = requests.get(URL, headers=HEADERS, timeout=TIMEOUT_SEC)
        
        # Explicit status check
        if response.status_code == 200:
            return response.text
        else:
            logging.error(f"Website returned non-200 status code: {response.status_code}")
            response.raise_for_status()
            return ""
            
    except requests.exceptions.HTTPError as e:
        logging.error(f"HTTP Error fetching data from website: {e}")
        return ""
    except requests.exceptions.ConnectionError as e:
        logging.error(f"Connection Error fetching data from website: {e}")
        return ""
    except requests.exceptions.Timeout as e:
        logging.error(f"Timeout Error fetching data from website: {e}")
        return ""
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to fetch data from website: {e}")
        return ""
    except Exception as e:
        logging.error(f"Unexpected error occurred: {e}")
        return ""

def extract_price(price_text: str) -> float:
    """Safely extracts the numerical value from a scraped price string."""
    match = re.search(r"[\d\.]+", price_text)
    if match:
        try:
            return float(match.group())
        except ValueError:
            pass
    return 0.0

def parse_books(html_content: str) -> List[Dict[str, Any]]:
    """Safely parses required book data fields from HTML content using BeautifulSoup."""
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # The assignment specifically requires extraction of at least 20 books.
    # The index page uniquely contains exactly 20 books inside 'product_pod' articles.
    articles = soup.find_all('article', class_='product_pod')
    
    book_list = []
    for article in articles:
        try:
            # Extract Book Title safely using find
            h3_elem = article.find('h3')
            a_elem = h3_elem.find('a') if h3_elem else None
            title = a_elem.get('title', 'Unknown') if a_elem else 'Unknown'
            
            # Extract Price safely
            price_elem = article.find('p', class_='price_color')
            price_text = price_elem.text if price_elem else '0.0'
            price_num = extract_price(price_text)
            
            # Extract Rating and convert to numerical values (Task B3)
            rating_elem = article.find('p', class_='star-rating')
            if rating_elem and rating_elem.has_attr('class') and len(rating_elem['class']) > 1:
                rating_class = rating_elem['class'][1]
            else:
                rating_class = 'None'
            
            rating_num = RATING_MAP.get(rating_class, 0)
            
            # Store extracted data (Task B2)
            book_list.append({
                "title": title,
                "price": price_text, 
                "numeric_price": price_num, 
                "rating": rating_num
            })
            
        except Exception as e:
            logging.warning(f"Error parsing a book article: {e}")
            continue
            
    return book_list

def scrape_book_data() -> None:
    """Main execution block to orchestrate web scraping, extraction, and evaluation."""
    print("--- Part B: Web Scraping ---")
    html_content = fetch_html()
    
    if not html_content:
        print("No HTML content retrieved. Please check network connection.")
        return
        
    book_list = parse_books(html_content)
    
    # Task B1 & B2: Extract and store for at least 20 books
    print(f"\n[Task B1, B2 & B3] Extracted {len(book_list)} books successfully.")
    
    if book_list:
        # Task B4: Find most expensive, least expensive, and average price
        most_expensive = max(book_list, key=lambda x: x['numeric_price'])
        least_expensive = min(book_list, key=lambda x: x['numeric_price'])
        
        # Safely compute the average price
        total_price = sum(b['numeric_price'] for b in book_list)
        avg_price = round(total_price / len(book_list), 2)
        
        print("\n[Task B4]")
        print(f"Most Expensive Book: {most_expensive['title']} at {most_expensive['price']}")
        print(f"Least Expensive Book: {least_expensive['title']} at {least_expensive['price']}")
        print(f"Average Book Price: £{avg_price:.2f}")
        
    # Task B5: Save into books.json
    try:
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            json.dump(book_list, f, indent=4)
        print(f"\n[Task B5] Successfully saved extracted data to {OUTPUT_FILE}.\n")
    except IOError as e:
        logging.error(f"Failed to save {OUTPUT_FILE}: {e}")

if __name__ == "__main__":
    scrape_book_data()
