"""
web_scraping.py — Part B: Web Scraping

Scrapes book listings across multiple pages of books.toscrape.com.
Extracts Title, Price (clean £ string + float), and Star Rating (int 1–5).
Persists the full dataset to books.json.
"""
import re
from typing import Any, Dict, List, Optional
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

import config
from utils import get_logger, save_json_file

logger = get_logger(__name__)


class BookScraper:
    """
    Scrapes paginated book listings from books.toscrape.com.

    Features:
        - Multi-page crawling (configurable via config.SCRAPE_MAX_PAGES).
        - Explicit UTF-8 encoding enforcement to prevent Â£ artifacts.
        - Per-field validation of every extracted record.
        - Count validation against config.MIN_EXPECTED_BOOKS.
    """

    def __init__(self) -> None:
        self.start_url: str = config.SCRAPE_START_URL
        self.base_url: str = config.SCRAPE_BASE_URL
        self.output_file: str = config.BOOKS_FILE
        self.max_pages: int = config.SCRAPE_MAX_PAGES

    # ------------------------------------------------------------------ #
    #  Network Layer
    # ------------------------------------------------------------------ #

    def _fetch_page(self, url: str) -> Optional[str]:
        """
        Fetches the HTML of a single page.

        Args:
            url: Target URL.

        Returns:
            UTF-8 decoded HTML string, or None on failure.
        """
        try:
            response = requests.get(
                url,
                headers=config.REQUEST_HEADERS,
                timeout=config.REQUEST_TIMEOUT,
            )
            if response.status_code != 200:
                logger.error("HTTP %d for URL: %s", response.status_code, url)
                return None

            # Force UTF-8 decoding to prevent encoding artefacts (Â£ → £)
            response.encoding = "utf-8"
            return response.text

        except requests.exceptions.HTTPError as exc:
            logger.error("HTTP error fetching '%s': %s", url, exc)
        except requests.exceptions.ConnectionError as exc:
            logger.error("Connection error fetching '%s': %s", url, exc)
        except requests.exceptions.Timeout:
            logger.error("Timeout fetching '%s' (limit %ds).", url, config.REQUEST_TIMEOUT)
        except requests.exceptions.RequestException as exc:
            logger.error("Request failed for '%s': %s", url, exc)

        return None

    # ------------------------------------------------------------------ #
    #  Parsing Helpers
    # ------------------------------------------------------------------ #

    @staticmethod
    def _clean_price(raw: str) -> str:
        """
        Reconstructs a clean £X.XX price string from any scraped text.
        Uses Unicode U+00A3 (£) directly to avoid all encoding ambiguity.
        """
        match = re.search(r"[\d.]+", raw)
        return f"\u00a3{match.group()}" if match else "£0.00"

    @staticmethod
    def _to_float(price_str: str) -> float:
        """Extracts the numeric value from a clean price string."""
        match = re.search(r"[\d.]+", price_str)
        try:
            return float(match.group()) if match else 0.0
        except ValueError:
            return 0.0

    def _parse_page(self, html: str) -> List[Dict[str, Any]]:
        """
        Parses all book articles from a single page's HTML.

        Args:
            html: Raw HTML content of one catalogue page.

        Returns:
            List of book dicts; malformed articles are skipped with a warning.
        """
        soup = BeautifulSoup(html, "html.parser")
        articles = soup.find_all("article", class_="product_pod")
        books: List[Dict[str, Any]] = []

        for idx, article in enumerate(articles):
            try:
                # Title — inside <h3><a title="...">
                h3 = article.find("h3")
                a_tag = h3.find("a") if h3 else None
                title: str = a_tag.get("title", "").strip() if a_tag else ""

                # Price — inside <p class="price_color">
                price_elem = article.find("p", class_="price_color")
                raw_price: str = price_elem.get_text(strip=True) if price_elem else ""
                clean_price: str = self._clean_price(raw_price)
                numeric_price: float = self._to_float(clean_price)

                # Star rating — second CSS class of <p class="star-rating X">
                rating_p = article.find("p", class_="star-rating")
                classes = rating_p.get("class", []) if rating_p else []
                rating_word: str = classes[1] if len(classes) > 1 else "None"
                rating_int: int = config.RATING_MAP.get(rating_word, 0)

                # Per-record validation
                if not title:
                    logger.warning("Article %d on page has no title — skipping.", idx)
                    continue
                if numeric_price <= 0:
                    logger.warning("Article '%s' has invalid price '%s'.", title, raw_price)

                books.append({
                    "title":         title,
                    "price":         clean_price,
                    "numeric_price": numeric_price,
                    "rating":        rating_int,
                })

            except (AttributeError, KeyError, TypeError) as exc:
                logger.warning("Error parsing article %d: %s — skipping.", idx, exc)

        return books

    @staticmethod
    def _next_page_url(html: str, base_url: str) -> Optional[str]:
        """
        Extracts the URL of the next catalogue page from pagination links.

        Returns:
            Absolute URL of the next page, or None if this is the last page.
        """
        soup = BeautifulSoup(html, "html.parser")
        next_btn = soup.find("li", class_="next")
        if next_btn:
            a_tag = next_btn.find("a")
            if a_tag and a_tag.get("href"):
                return urljoin(base_url, a_tag["href"])
        return None

    # ------------------------------------------------------------------ #
    #  Orchestration
    # ------------------------------------------------------------------ #

    def scrape_all_pages(self) -> List[Dict[str, Any]]:
        """
        Crawls up to config.SCRAPE_MAX_PAGES pages and aggregates results.

        Returns:
            Combined list of all book dicts collected across all pages.
        """
        all_books: List[Dict[str, Any]] = []
        current_url: Optional[str] = self.start_url
        page_num: int = 0

        while current_url and page_num < self.max_pages:
            page_num += 1
            logger.info("Scraping page %d: %s", page_num, current_url)

            html = self._fetch_page(current_url)
            if not html:
                logger.error("Failed to fetch page %d — stopping pagination.", page_num)
                break

            page_books = self._parse_page(html)
            logger.info("  Extracted %d books from page %d.", len(page_books), page_num)
            all_books.extend(page_books)

            current_url = self._next_page_url(html, self.base_url)

        return all_books

    def execute(self) -> None:
        """Runs the complete web-scraping workflow (Tasks B1–B5)."""
        print("=" * 60)
        print("  Part B: Web Scraping")
        print("=" * 60)

        books = self.scrape_all_pages()

        # Validate record count
        print(f"\n[Tasks B1, B2 & B3] Extracted {len(books)} book records "
              f"from {config.SCRAPE_MAX_PAGES} page(s).")

        if len(books) < config.MIN_EXPECTED_BOOKS:
            logger.warning(
                "Expected >= %d books but only got %d.",
                config.MIN_EXPECTED_BOOKS, len(books),
            )

        if books:
            most_expensive = max(books, key=lambda b: b["numeric_price"])
            least_expensive = min(books, key=lambda b: b["numeric_price"])
            avg_price = round(
                sum(b["numeric_price"] for b in books) / len(books), 2
            )

            print("\n[Task B4] Price Statistics:")
            print(f"  Most Expensive : {most_expensive['title'][:55]}")
            print(f"                   → {most_expensive['price']}")
            print(f"  Least Expensive: {least_expensive['title'][:55]}")
            print(f"                   → {least_expensive['price']}")
            print(f"  Average Price  : \u00a3{avg_price:.2f}")

        if save_json_file(self.output_file, books, logger):
            print(f"\n[Task B5] Saved {len(books)} records to '{self.output_file}'.")


def scrape_book_data() -> None:
    """Public entry point consumed by main.py."""
    BookScraper().execute()


if __name__ == "__main__":
    scrape_book_data()
