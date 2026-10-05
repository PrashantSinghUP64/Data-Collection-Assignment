"""
config.py — Central configuration for the Data Collection Pipeline.

All tunable parameters are defined here. No module should
contain hardcoded URLs, file paths, or magic numbers.
"""

# ── API ─────────────────────────────────────────────────────────────────────
API_URL: str = "https://jsonplaceholder.typicode.com/users"
REQUEST_TIMEOUT: int = 10          # seconds
REQUEST_HEADERS: dict = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}

# ── Web Scraping ─────────────────────────────────────────────────────────────
SCRAPE_BASE_URL: str = "https://books.toscrape.com/catalogue/"
SCRAPE_START_URL: str = "https://books.toscrape.com/catalogue/page-1.html"
SCRAPE_MAX_PAGES: int = 5          # scrape up to 5 pages (100 books)
MIN_EXPECTED_BOOKS: int = 20       # raise a warning below this count

RATING_MAP: dict = {
    "One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5
}

# ── Output Files ─────────────────────────────────────────────────────────────
USERS_FILE: str = "users.json"
BOOKS_FILE: str = "books.json"
REPORT_FILE: str = "report.json"
LOG_FILE: str = "pipeline.log"

# ── Logging ──────────────────────────────────────────────────────────────────
LOG_FORMAT: str = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
LOG_DATE_FORMAT: str = "%Y-%m-%d %H:%M:%S"
