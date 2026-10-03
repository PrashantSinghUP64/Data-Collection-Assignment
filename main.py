import sys
from api_data import fetch_api_data
from web_scraping import scrape_book_data
from json_processing import process_json_data
from analysis import analyze_data

def display_menu():
    print("="*40)
    print(" Data Collection and Processing Menu ")
    print("="*40)
    print("1. Fetch API Data")
    print("2. Scrape Book Data")
    print("3. Generate JSON Files (Processing)")
    print("4. Analyze Data")
    print("5. Exit")
    print("="*40)

def main():
    while True:
        display_menu()
        choice = input("Enter your choice (1-5): ")
        
        if choice == '1':
            fetch_api_data()
        elif choice == '2':
            scrape_book_data()
        elif choice == '3':
            process_json_data()
        elif choice == '4':
            analyze_data()
        elif choice == '5':
            print("Exiting program")
            sys.exit(0)
        else:
            print("Invalid choice. Please enter a number between 1 and 5.\n")

if __name__ == "__main__":
    main()
