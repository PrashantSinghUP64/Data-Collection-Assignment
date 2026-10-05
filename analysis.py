"""
analysis.py — Part D: Data Analysis

Performs quantitative analysis on collected user and book data using Pandas.
Produces statistics on companies, book pricing, and star-rating distributions.
"""
import logging
from collections import Counter
from typing import List

import pandas as pd

from utils import load_json_file  # shared utility — eliminates code duplication

USERS_FILE = "users.json"
BOOKS_FILE = "books.json"

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


class DataAnalyzer:
    """Performs structured analysis on user and book datasets using Pandas DataFrames."""

    def __init__(self) -> None:
        self.users_file = USERS_FILE
        self.books_file = BOOKS_FILE

    def _to_dataframe(self, filepath: str) -> pd.DataFrame:
        """Loads validated JSON records into a Pandas DataFrame."""
        records = load_json_file(filepath)
        if not records:
            return pd.DataFrame()
        return pd.DataFrame(records)

    # ------------------------------------------------------------------ #
    #  User Analysis
    # ------------------------------------------------------------------ #
    def analyze_users(self, df: pd.DataFrame) -> None:
        """Reports user-level statistics from the dataset."""
        print("\n[User Analysis]")

        if df.empty or "company" not in df.columns:
            print("  No user data available.")
            return

        # 1. Total Users
        print(f"  Total Users: {len(df)}")

        # 2. Unique Companies (excluding 'Unknown')
        valid_companies: pd.Series = (
            df["company"]
            .dropna()
            .str.strip()
            .replace("Unknown", pd.NA)
            .dropna()
        )
        unique_companies: List[str] = valid_companies.unique().tolist()
        print(f"  Unique Companies: {len(unique_companies)}")

        # 3. Top 5 Companies by frequency (meaningful ranking, not alphabetical)
        top_5 = (
            valid_companies.value_counts()
            .head(5)
            .reset_index()
            .rename(columns={"index": "company", "company": "count"})
        )
        print("  Top 5 Companies by Frequency:")
        for _, row in top_5.iterrows():
            print(f"    - {row.iloc[0]}: {row.iloc[1]} user(s)")

    # ------------------------------------------------------------------ #
    #  Book Analysis
    # ------------------------------------------------------------------ #
    def analyze_books(self, df: pd.DataFrame) -> None:
        """Reports book-level statistics from the dataset."""
        print("\n[Book Analysis]")

        if df.empty or "numeric_price" not in df.columns or "rating" not in df.columns:
            print("  No book data available.")
            return

        # 1. Average Price
        avg_price: float = df["numeric_price"].mean()
        print(f"  Average Price: £{avg_price:.2f}")

        # 2. Highest Rated Books
        max_rating: int = int(df["rating"].max())
        highest_rated: List[str] = df[df["rating"] == max_rating]["title"].tolist()
        print(f"  Highest Rated Books (Rating {max_rating}/5):")
        for title in highest_rated:
            print(f"    * {title}")

        # 3. Rating Distribution (1–5) using Counter for precise frequency mapping
        rating_counts: Counter = Counter(df["rating"].tolist())
        print("  Books per Rating Category:")
        for rating in range(5, 0, -1):
            print(f"    Rating {rating}: {rating_counts.get(rating, 0)} book(s)")

    # ------------------------------------------------------------------ #
    #  Execution
    # ------------------------------------------------------------------ #
    def execute(self) -> None:
        """Orchestrates the full data-analysis workflow."""
        print("--- Part D: Data Analysis ---")

        df_users = self._to_dataframe(self.users_file)
        df_books = self._to_dataframe(self.books_file)

        if df_users.empty or df_books.empty:
            print("Required data files are missing or empty. Run Parts A and B first.")
            return

        self.analyze_users(df_users)
        self.analyze_books(df_books)
        print()


def analyze_data() -> None:
    """Public entry point used by main.py."""
    DataAnalyzer().execute()


if __name__ == "__main__":
    analyze_data()
