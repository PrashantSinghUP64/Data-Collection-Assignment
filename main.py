"""
main.py — CLI entry point for the Data Collection and Processing Pipeline.

Provides a validated menu-driven interface so each pipeline stage
can be executed independently or in sequence.
"""
import sys

from api_data import fetch_api_data
from web_scraping import scrape_book_data
from json_processing import process_json_data
from analysis import analyze_data
from utils import get_logger

logger = get_logger(__name__)

MENU_OPTIONS: dict = {
    "1": ("Fetch API Data         (Part A)", fetch_api_data),
    "2": ("Scrape Book Data       (Part B)", scrape_book_data),
    "3": ("Process JSON Data      (Part C)", process_json_data),
    "4": ("Analyse Data           (Part D)", analyze_data),
    "5": ("Run Full Pipeline      (A → D)",  None),
    "6": ("Exit", None),
}


def display_menu() -> None:
    """Prints the interactive CLI menu."""
    print("\n" + "=" * 60)
    print("   Data Collection & Processing Pipeline")
    print("=" * 60)
    for key, (label, _) in MENU_OPTIONS.items():
        print(f"  [{key}] {label}")
    print("=" * 60)


def run_full_pipeline() -> None:
    """Executes all four pipeline stages sequentially."""
    logger.info("Starting full pipeline execution.")
    fetch_api_data()
    scrape_book_data()
    process_json_data()
    analyze_data()
    logger.info("Full pipeline completed successfully.")


def main() -> None:
    """Main event loop — validates input and dispatches pipeline stages."""
    while True:
        display_menu()

        try:
            choice: str = input("Enter your choice (1-6): ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nInterrupted. Exiting.")
            sys.exit(0)

        if choice not in MENU_OPTIONS:
            print(f"  Invalid choice '{choice}'. Please enter a number from 1 to 6.\n")
            continue

        label, fn = MENU_OPTIONS[choice]

        if choice == "5":
            run_full_pipeline()
        elif choice == "6":
            logger.info("User exited the application.")
            print("Goodbye!")
            sys.exit(0)
        else:
            logger.info("Executing: %s", label)
            fn()


if __name__ == "__main__":
    main()
