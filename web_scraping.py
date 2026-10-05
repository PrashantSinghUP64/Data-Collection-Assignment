"""
web_scraping.py — Part B: Web Scraping

Scrapes book listings from books.toscrape.com using requests + BeautifulSoup.
Extracts Title, Price (clean UTF-8 string + float), and Star Rating (integer).
"""
import json
import logging
import re
from typing import List, Dict, Any, Optional

import requests
from bs4 import BeautifulSoup

URL = "https://books.toscrape.com/"
OUTPUT_FILE = "books.json"
TIMEOUT_SEC = 10
MIN_EXPECTED_BOOKS = 20
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}
RATING_MAP: Dict[str, int] = {
    "One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5
}

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


class BookScraper:
    """Scrapes and parses book data from books.toscrape.com."""

    def __init__(self) -> None:
        self.url = URL
        self.output_file = OUTPUT_FILE

    def fetch_html(self) -> str:
        """Fetches raw HTML from the target URL with proper error handling."""
        try:
            response = requests.get(self.url, headers=HEADERS, timeout=TIMEOUT_SEC)

            if response.status_code != 200:
                logging.error(f"Non-200 HTTP status: {response.status_code}")
                response.raise_for_status()

            # Force UTF-8 to avoid encoding artifacts (e.g. Â£ instead of £)
            response.encoding = "utf-8"
            return response.text

        except requests.exceptions.HTTPError as e:
            logging.error(f"HTTP Error: {e}")
        except requests.exceptions.ConnectionError as e:
            logging.error(f"Connection Error: {e}")
        except requests.exceptions.Timeout as e:
            logging.error(f"Timeout after {TIMEOUT_SEC}s: {e}")
        except requests.exceptions.RequestException as e:
            logging.error(f"Request failed: {e}")

        return ""

    @staticmethod
    def extract_price_float(price_text: str) -> float:
        """Extracts the numeric part of a price string as a float."""
        match = re.search(r"[\d.]+", price_text)
        if match:
            try:
                return float(match.group())
            except ValueError:
                pass
        return 0.0

    @staticmethod
    def clean_price_text(price_text: str) -> str:
        """
        Returns a clean price string with the £ symbol correctly preserved.
        Handles encoding mismatches by extracting the numeric value and
        reconstructing the price string with the proper pound sign.
        """
        numeric = re.search(r"[\d.]+", price_text)
        if numeric:
            return f"\u00a3{numeric.group()}"  # £ as unicode to avoid all encoding issues
        return price_text.strip()

    def parse_books(self, html_content: str) -> List[Dict[str, Any]]:
        """Parses all book articles and extracts Title, Price, and Rating."""
        soup = BeautifulSoup(html_content, "html.parser")
        articles = soup.find_all("article", class_="product_pod")
        book_list: List[Dict[str, Any]] = []

        for article in articles:
            try:
                # Extract Title
                h3_elem = article.find("h3")
                a_elem = h3_elem.find("a") if h3_elem else None
                title: str = a_elem.get("title", "Unknown") if a_elem else "Unknown"

                # Extract and clean Price
                price_elem = article.find("p", class_="price_color")
                raw_price: str = price_elem.text.strip() if price_elem else "£0.00"
                clean_price: str = self.clean_price_text(raw_price)
                numeric_price: float = self.extract_price_float(clean_price)

                # Extract Star Rating and convert to integer
                rating_elem = article.find("p", class_="star-rating")
                rating_word: str = (
                    rating_elem["class"][1]
                    if rating_elem and len(rating_elem.get("class", [])) > 1
                    else "None"
                )
                rating_num: int = RATING_MAP.get(rating_word, 0)

                book_list.append({
                    "title": title,
                    "price": clean_price,
                    "numeric_price": numeric_price,
                    "rating": rating_num,
                })

            except (AttributeError, KeyError, TypeError) as e:
                logging.warning(f"Skipping malformed book article: {e}")

        return book_list

    def execute(self) -> None:
        """Orchestrates the web-scraping workflow (Tasks B1–B5)."""
        print("--- Part B: Web Scraping ---")

        html_content = self.fetch_html()
        if not html_content:
            print("No HTML content retrieved. Check network connectivity.")
            return

        book_list = self.parse_books(html_content)

        # Validate that enough books were scraped
        print(f"\n[Tasks B1, B2 & B3] Extracted {len(book_list)} books.")
        if len(book_list) < MIN_EXPECTED_BOOKS:
            logging.warning(
                f"Expected at least {MIN_EXPECTED_BOOKS} books, "
                f"but only {len(book_list)} were found."
            )

        if book_list:
            most_expensive = max(book_list, key=lambda b: b["numeric_price"])
            least_expensive = min(book_list, key=lambda b: b["numeric_price"])
            avg_price = round(
                sum(b["numeric_price"] for b in book_list) / len(book_list), 2
            )

            print("\n[Task B4]")
            print(f"  Most Expensive : {most_expensive['title']} — {most_expensive['price']}")
            print(f"  Least Expensive: {least_expensive['title']} — {least_expensive['price']}")
            print(f"  Average Price  : £{avg_price:.2f}")

        try:
            with open(self.output_file, "w", encoding="utf-8") as f:
                json.dump(book_list, f, indent=4, ensure_ascii=False)
            logging.info(f"[Task B5] Saved {len(book_list)} books to '{self.output_file}'.")
        except IOError as e:
            logging.error(f"Failed to write '{self.output_file}': {e}")


def scrape_book_data() -> None:
    """Public entry point used by main.py."""
    BookScraper().execute()


if __name__ == "__main__":
    scrape_book_data()
