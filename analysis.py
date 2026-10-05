"""
Module for robustly analyzing user and book datasets using Pandas (Industry Standard).
"""
import logging
import pandas as pd

USERS_FILE = 'users.json'
BOOKS_FILE = 'books.json'

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

class DataAnalyzer:
    """Class to perform industry-standard data analysis using Pandas."""

    def __init__(self) -> None:
        self.users_file = USERS_FILE
        self.books_file = BOOKS_FILE

    def load_data(self, filepath: str) -> pd.DataFrame:
        """Loads JSON data into a Pandas DataFrame."""
        try:
            return pd.read_json(filepath)
        except ValueError as e:
            logging.error(f"JSON schema parsing failed in {filepath}: {e}")
            return pd.DataFrame()
        except FileNotFoundError:
            logging.error(f"Failed to load {filepath}: File does not exist.")
            return pd.DataFrame()

    def analyze_users(self, df: pd.DataFrame) -> None:
        """Computes analytical metrics securely on the Users dataset."""
        print("\n[User Analysis]")
        
        if df.empty:
            print("No user data available.")
            return
            
        # 1. Total Users
        print(f"- Total Users: {len(df)}")
        
        # 2. Unique Companies
        # Drop NaN/Unknown companies
        if 'company' in df.columns:
            valid_companies = df['company'].dropna()
            valid_companies = valid_companies[valid_companies != 'Unknown'].str.strip()
            unique_companies = valid_companies.unique()
            print(f"- Unique Companies: {len(unique_companies)}")
            
            # 3. Top 5 Companies (Alphabetically) using safe case-insensitive sorting
            top_5_companies = sorted(unique_companies, key=lambda x: str(x).lower())[:5]
            print(f"- Top 5 Companies (Alphabetically): {', '.join(str(c) for c in top_5_companies)}")
        else:
            print("- Unique Companies: 0\n- Top 5 Companies: None")

    def analyze_books(self, df: pd.DataFrame) -> None:
        """Computes analytical metrics securely on the Books dataset."""
        print("\n[Book Analysis]")
        
        if df.empty or 'numeric_price' not in df.columns or 'rating' not in df.columns:
            print("No book data available for analysis.")
            return

        # 1. Average Price (rounded mathematically to 2 decimals)
        avg_price = df['numeric_price'].mean()
        print(f"- Average Price: £{avg_price:.2f}")
        
        # 2. Highest Rated Books
        max_rating = df['rating'].max()
        highest_rated = df[df['rating'] == max_rating]['title'].tolist()
        print(f"- Highest Rated Books (Rating {max_rating}):")
        for title in highest_rated:
            print(f"  * {title}")
        
        # 3. Number of Books in Each Rating Category
        rating_counts = df['rating'].value_counts().to_dict()
        
        print("- Number of Books in Each Rating Category:")
        for rating in range(5, 0, -1):
            count = rating_counts.get(rating, 0)
            print(f"  * Rating {rating}: {count} books")

    def execute(self) -> None:
        """Main execution block."""
        print("--- Part D: Data Analysis (Powered by Pandas) ---")
        
        df_users = self.load_data(self.users_file)
        df_books = self.load_data(self.books_file)
        
        if df_users.empty or df_books.empty:
            print("Required JSON data missing or corrupt. Run data collection first.")
            return

        self.analyze_users(df_users)
        self.analyze_books(df_books)
        print()

def analyze_data() -> None:
    analyzer = DataAnalyzer()
    analyzer.execute()

if __name__ == "__main__":
    analyze_data()
