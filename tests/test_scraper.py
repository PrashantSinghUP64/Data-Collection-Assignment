"""
tests/test_scraper.py — Unit tests for web_scraping.py

Tests cover:
  - Price extraction and cleaning
  - Star-rating conversion
  - Next-page URL detection
  - HTML parsing with known fixtures
  - Handling of malformed articles
"""
import sys
import os
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from web_scraping import BookScraper


# Minimal HTML article fixture mimicking books.toscrape.com
BOOK_HTML_FIXTURE = """
<html><body>
<article class="product_pod">
  <h3><a title="A Light in the Attic" href="...">A Light in ...</a></h3>
  <p class="price_color">Â£51.77</p>
  <p class="star-rating Three"></p>
</article>
<article class="product_pod">
  <h3><a title="Tipping the Velvet" href="...">Tipping ...</a></h3>
  <p class="price_color">Â£53.74</p>
  <p class="star-rating One"></p>
</article>
</body></html>
"""

NEXT_PAGE_HTML = """
<html><body>
  <ul class="pager">
    <li class="next"><a href="page-2.html">next</a></li>
  </ul>
</body></html>
"""

LAST_PAGE_HTML = """
<html><body>
  <ul class="pager"></ul>
</body></html>
"""


class TestBookScraperHelpers(unittest.TestCase):
    """Tests for static helper methods."""

    def setUp(self) -> None:
        self.scraper = BookScraper()

    # ── Price Cleaning ─────────────────────────────────────────────────
    def test_clean_price_strips_symbol(self) -> None:
        """clean_price must return a string starting with £ (U+00A3)."""
        result = BookScraper._clean_price("Â£51.77")
        self.assertTrue(result.startswith("\u00a3"))

    def test_clean_price_correct_value(self) -> None:
        """clean_price must preserve the numeric component."""
        result = BookScraper._clean_price("Â£51.77")
        self.assertIn("51.77", result)

    def test_clean_price_empty_string(self) -> None:
        """clean_price must return a safe default for empty input."""
        result = BookScraper._clean_price("")
        self.assertEqual(result, "\u00a30.00")

    # ── Float Extraction ───────────────────────────────────────────────
    def test_to_float_correct(self) -> None:
        self.assertAlmostEqual(BookScraper._to_float("\u00a351.77"), 51.77)

    def test_to_float_zero_on_invalid(self) -> None:
        self.assertEqual(BookScraper._to_float("no numbers here"), 0.0)

    # ── Page Parsing ───────────────────────────────────────────────────
    def test_parse_page_count(self) -> None:
        """parse_page must return exactly as many books as articles in the HTML."""
        books = self.scraper._parse_page(BOOK_HTML_FIXTURE)
        self.assertEqual(len(books), 2)

    def test_parse_page_title_extracted(self) -> None:
        books = self.scraper._parse_page(BOOK_HTML_FIXTURE)
        self.assertEqual(books[0]["title"], "A Light in the Attic")

    def test_parse_page_rating_converted(self) -> None:
        """Star-rating words must be converted to integers."""
        books = self.scraper._parse_page(BOOK_HTML_FIXTURE)
        self.assertEqual(books[0]["rating"], 3)   # "Three" → 3
        self.assertEqual(books[1]["rating"], 1)   # "One"   → 1

    def test_parse_page_numeric_price_positive(self) -> None:
        """numeric_price must be a positive float."""
        books = self.scraper._parse_page(BOOK_HTML_FIXTURE)
        self.assertGreater(books[0]["numeric_price"], 0)

    def test_parse_empty_html(self) -> None:
        """parse_page must return [] for HTML with no product articles."""
        books = self.scraper._parse_page("<html><body></body></html>")
        self.assertEqual(books, [])

    # ── Pagination ─────────────────────────────────────────────────────
    def test_next_page_url_detected(self) -> None:
        url = BookScraper._next_page_url(NEXT_PAGE_HTML, "https://books.toscrape.com/catalogue/")
        self.assertIsNotNone(url)
        self.assertIn("page-2.html", url)

    def test_last_page_returns_none(self) -> None:
        url = BookScraper._next_page_url(LAST_PAGE_HTML, "https://books.toscrape.com/catalogue/")
        self.assertIsNone(url)

    # ── Required Keys ──────────────────────────────────────────────────
    def test_all_required_keys_present(self) -> None:
        """Every parsed book record must contain all four required keys."""
        books = self.scraper._parse_page(BOOK_HTML_FIXTURE)
        required = {"title", "price", "numeric_price", "rating"}
        for book in books:
            self.assertTrue(required.issubset(book.keys()))


if __name__ == "__main__":
    unittest.main()
