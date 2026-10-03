import requests
from bs4 import BeautifulSoup
import json
import re

def scrape_book_data():
    print("--- Part B: Web Scraping ---")
    url = "https://books.toscrape.com/"
    response = requests.get(url)
    
    if response.status_code != 200:
        print("Failed to fetch data from website")
        return
        
    soup = BeautifulSoup(response.text, 'html.parser')
    
    articles = soup.find_all('article', class_='product_pod')
    
    book_list = []
    
    # Mapping string ratings to numbers
    rating_map = {
        "One": 1,
        "Two": 2,
        "Three": 3,
        "Four": 4,
        "Five": 5
    }
    
    # Task B1 & B2: Extract and store
    for article in articles:
        title = article.h3.a['title']
        price_text = article.find('p', class_='price_color').text
        
        # Clean price (e.g., '£51.77' to 51.77)
        # Using regex to extract numeric part for numerical operations
        price_match = re.search(r"[\d\.]+", price_text)
        price_num = float(price_match.group()) if price_match else 0.0
        
        rating_class = article.find('p', class_='star-rating')['class'][1]
        
        # Task B3: Convert ratings to numerical values
        rating_num = rating_map.get(rating_class, 0)
        
        book_list.append({
            "title": title,
            "price": price_text, 
            "numeric_price": price_num, 
            "rating": rating_num
        })
        
    # Task B1 verification
    print(f"\n[Task B1 & B2 & B3] Extracted {len(book_list)} books.")
    
    if len(book_list) > 0:
        # Task B4: Find most expensive, least expensive, average price
        most_expensive = max(book_list, key=lambda x: x['numeric_price'])
        least_expensive = min(book_list, key=lambda x: x['numeric_price'])
        avg_price = sum(b['numeric_price'] for b in book_list) / len(book_list)
        
        print(f"\n[Task B4]")
        print(f"Most Expensive Book: {most_expensive['title']} at {most_expensive['price']}")
        print(f"Least Expensive Book: {least_expensive['title']} at {least_expensive['price']}")
        print(f"Average Book Price: £{avg_price:.2f}")
        
    # Task B5: Save into books.json
    with open('books.json', 'w') as f:
        json.dump(book_list, f, indent=4)
    print("\n[Task B5] Saved extracted data to books.json.\n")

if __name__ == "__main__":
    scrape_book_data()
