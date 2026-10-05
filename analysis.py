"""
analysis.py — Part D: Data Analysis

Performs quantitative analysis on collected user and book data using Pandas.
Produces multi-dimensional statistics on pricing, ratings, and company distribution.
"""
from collections import Counter
from typing import Any, Dict, List

import pandas as pd

import config
from utils import get_logger, load_json_file

logger = get_logger(__name__)


class DataAnalyzer:
    """
    Performs structured analysis on user and book datasets.

    Uses Pandas DataFrames for vectorised operations and
    collections.Counter for frequency analysis.
    """

    def __init__(self) -> None:
        self.users_file: str = config.USERS_FILE
        self.books_file: str = config.BOOKS_FILE

    # ------------------------------------------------------------------ #
    #  Data Loading
    # ------------------------------------------------------------------ #

    def _load_dataframe(self, filepath: str) -> pd.DataFrame:
        """Loads validated JSON records into a Pandas DataFrame."""
        records: List[Dict[str, Any]] = load_json_file(filepath)
        if not records:
            return pd.DataFrame()
        return pd.DataFrame(records)

    # ------------------------------------------------------------------ #
    #  User Analysis
    # ------------------------------------------------------------------ #

    def analyze_users(self, df: pd.DataFrame) -> None:
        """
        Computes user-level statistics:
          - Total user count
          - Unique company count
          - Company frequency distribution (Top 5)
          - Email domain distribution
        """
        print("\n[User Analysis]")

        if df.empty or "company" not in df.columns:
            print("  No user data available.")
            return

        total: int = len(df)
        print(f"  1. Total Users: {total}")

        # Unique companies (exclude 'Unknown')
        valid_companies: pd.Series = (
            df["company"]
            .dropna()
            .str.strip()
            .replace("Unknown", pd.NA)
            .dropna()
        )
        unique_count: int = valid_companies.nunique()
        print(f"  2. Unique Companies: {unique_count}")

        # Top 5 companies by user frequency (meaningful metric)
        top5 = valid_companies.value_counts().head(5)
        print("  3. Top 5 Companies by User Count:")
        for company, count in top5.items():
            print(f"       {company}: {count} user(s)")

        # Email domain distribution
        if "email" in df.columns:
            domains = df["email"].str.split("@").str[-1].value_counts()
            print("  4. Email Domain Distribution (Top 5):")
            for domain, cnt in domains.head(5).items():
                print(f"       @{domain}: {cnt}")

    # ------------------------------------------------------------------ #
    #  Book Analysis
    # ------------------------------------------------------------------ #

    def analyze_books(self, df: pd.DataFrame) -> None:
        """
        Computes book-level statistics:
          - Descriptive price statistics (mean, median, std, min, max)
          - Price quartile distribution
          - Highest and lowest rated books
          - Rating frequency distribution
          - Books above and below average price
        """
        print("\n[Book Analysis]")

        if df.empty or "numeric_price" not in df.columns or "rating" not in df.columns:
            print("  No book data available.")
            return

        prices: pd.Series = df["numeric_price"]

        # 1. Full descriptive price statistics
        mean_price: float  = round(prices.mean(), 2)
        median_price: float = round(prices.median(), 2)
        std_price: float   = round(prices.std(), 2)
        min_price: float   = round(prices.min(), 2)
        max_price: float   = round(prices.max(), 2)

        print(f"  1. Price Statistics (GBP):")
        print(f"       Mean   : \u00a3{mean_price}")
        print(f"       Median : \u00a3{median_price}")
        print(f"       Std Dev: \u00a3{std_price}")
        print(f"       Min    : \u00a3{min_price}")
        print(f"       Max    : \u00a3{max_price}")

        # 2. Price quartile distribution
        q1 = round(prices.quantile(0.25), 2)
        q3 = round(prices.quantile(0.75), 2)
        iqr = round(q3 - q1, 2)
        print(f"  2. Quartiles: Q1=\u00a3{q1}  Q3=\u00a3{q3}  IQR=\u00a3{iqr}")

        # 3. Books above and below average price
        above_avg: int = int((prices > mean_price).sum())
        below_avg: int = int((prices < mean_price).sum())
        print(f"  3. Books above average price: {above_avg}  |  Below average: {below_avg}")

        # 4. Highest rated books
        max_rating: int = int(df["rating"].max())
        top_books: List[str] = df[df["rating"] == max_rating]["title"].tolist()
        print(f"  4. Highest Rated Books (Rating {max_rating}/5):")
        for title in top_books:
            print(f"       * {title}")

        # 5. Rating frequency distribution (1–5, no category omitted)
        rating_counts: Counter = Counter(df["rating"].tolist())
        print("  5. Rating Distribution:")
        for star in range(5, 0, -1):
            bar = "\u2588" * rating_counts.get(star, 0)  # visual bar
            print(f"       {star}\u2605: {bar} ({rating_counts.get(star, 0)})")

        # 6. Most affordable highly-rated book (rating ≥ 4)
        quality_picks = df[df["rating"] >= 4].nsmallest(3, "numeric_price")
        print("  6. Best Value Books (Rating \u2265 4, Cheapest):")
        for _, row in quality_picks.iterrows():
            print(f"       {row['title'][:50]} — \u00a3{row['numeric_price']:.2f} (Rating {row['rating']})")

    # ------------------------------------------------------------------ #
    #  Orchestration
    # ------------------------------------------------------------------ #

    def execute(self) -> None:
        """Runs the complete data-analysis workflow."""
        print("=" * 60)
        print("  Part D: Data Analysis")
        print("=" * 60)

        df_users: pd.DataFrame = self._load_dataframe(self.users_file)
        df_books: pd.DataFrame = self._load_dataframe(self.books_file)

        if df_users.empty or df_books.empty:
            logger.error("Required data files are missing — run Parts A and B first.")
            return

        self.analyze_users(df_users)
        self.analyze_books(df_books)
        print()


def analyze_data() -> None:
    """Public entry point consumed by main.py."""
    DataAnalyzer().execute()


if __name__ == "__main__":
    analyze_data()
