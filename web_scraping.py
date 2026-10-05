"""
Module for securely scraping book information from books.toscrape.com.
Implemented using Object-Oriented Programming (OOP) for enterprise scalability.
"""
import json
import logging
import re
from typing import List, Dict, Any
import requests
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

class BookScraper:
    """Scraper class for extracting book data."""
    
    RATING_MAP = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}

    def __init__(self) -> None:
        self.url = "https://books.toscrape.com/"
        self.output_file = "books.json"
        self.timeout_sec = 10
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }

    def fetch_html(self) -> str:
        """Fetches HTML content securely."""
        try:
            response = requests.get(self.url, headers=self.headers, timeout=self.timeout_sec)
            if response.status_code == 200:
                return response.text
            else:
                logging.error(f"Non-200 status code: {response.status_code}")
                response.raise_for_status()
        except requests.exceptions.RequestException as e:
            logging.error(f"Request Failed: {e}")
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
        return ""

    def extract_price(self, price_text: str) -> float:
        """Safely extracts the numerical value from a scraped price string."""
        match = re.search(r"[\d\.]+", price_text)
        if match:
            try:
                return float(match.group())
            except ValueError:
                pass
        return 0.0

    def parse_books(self, html_content: str) -> List[Dict[str, Any]]:
        """Parses required book data fields safely."""
        soup = BeautifulSoup(html_content, 'html.parser')
        articles = soup.find_all('article', class_='product_pod')
        book_list = []
        
        for article in articles:
            try:
                h3_elem = article.find('h3')
                a_elem = h3_elem.find('a') if h3_elem else None
                title = a_elem.get('title', 'Unknown') if a_elem else 'Unknown'
                
                price_elem = article.find('p', class_='price_color')
                price_text = price_elem.text if price_elem else '0.0'
                price_num = self.extract_price(price_text)
                
                rating_elem = article.find('p', class_='star-rating')
                if rating_elem and rating_elem.has_attr('class') and len(rating_elem['class']) > 1:
                    rating_class = rating_elem['class'][1]
                else:
                    rating_class = 'None'
                
                rating_num = self.RATING_MAP.get(rating_class, 0)
                
                book_list.append({
                    "title": title,
                    "price": price_text, 
                    "numeric_price": price_num, 
                    "rating": rating_num
                })
            except Exception as e:
                logging.warning(f"Error parsing a book article: {e}")
                
        return book_list

    def execute(self) -> None:
        """Main execution workflow."""
        print("--- Part B: Web Scraping ---")
        html_content = self.fetch_html()
        
        if not html_content:
            print("No HTML content retrieved.")
            return
            
        book_list = self.parse_books(html_content)
        print(f"\n[Task B1, B2 & B3] Extracted {len(book_list)} books successfully.")
        
        if book_list:
            most_expensive = max(book_list, key=lambda x: x['numeric_price'])
            least_expensive = min(book_list, key=lambda x: x['numeric_price'])
            avg_price = round(sum(b['numeric_price'] for b in book_list) / len(book_list), 2)
            
            print("\n[Task B4]")
            print(f"Most Expensive Book: {most_expensive['title']} at {most_expensive['price']}")
            print(f"Least Expensive Book: {least_expensive['title']} at {least_expensive['price']}")
            print(f"Average Book Price: £{avg_price:.2f}")
            
        try:
            with open(self.output_file, 'w', encoding='utf-8') as f:
                json.dump(book_list, f, indent=4)
            print(f"\n[Task B5] Successfully saved extracted data to {self.output_file}.\n")
        except IOError as e:
            logging.error(f"Failed to save {self.output_file}: {e}")

def scrape_book_data() -> None:
    scraper = BookScraper()
    scraper.execute()

if __name__ == "__main__":
    scrape_book_data()
