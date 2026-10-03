import json

def analyze_data():
    print("--- Part D: Data Analysis ---")
    
    try:
        with open('users.json', 'r') as f:
            users = json.load(f)
        with open('books.json', 'r') as f:
            books = json.load(f)
    except FileNotFoundError:
        print("Required JSON files not found. Please run tasks A and B first.")
        return

    print("\n[User Analysis]")
    total_users = len(users)
    print(f"- Total Users: {total_users}")
    
    companies = [user.get('company') for user in users if user.get('company')]
    unique_companies = list(set(companies))
    print(f"- Unique Companies: {len(unique_companies)}")
    
    # Top 5 Companies (Alphabetically)
    top_5_companies = sorted(unique_companies)[:5]
    print(f"- Top 5 Companies (Alphabetically): {', '.join(top_5_companies)}")
    
    print("\n[Book Analysis]")
    avg_price = sum(b.get('numeric_price', 0) for b in books) / len(books) if len(books) > 0 else 0
    print(f"- Average Price: £{avg_price:.2f}")
    
    # Highest Rated Books
    if books:
        max_rating = max(book.get('rating', 0) for book in books)
        highest_rated = [book['title'] for book in books if book.get('rating', 0) == max_rating]
        print(f"- Highest Rated Books (Rating {max_rating}):")
        for title in highest_rated:
            print(f"  * {title}")
    
    # Number of Books in Each Rating Category
    rating_counts = {}
    for book in books:
        r = book.get('rating', 0)
        rating_counts[r] = rating_counts.get(r, 0) + 1
        
    print("- Number of Books in Each Rating Category:")
    for rating in sorted(rating_counts.keys(), reverse=True):
        print(f"  * Rating {rating}: {rating_counts[rating]} books")
    print()

if __name__ == "__main__":
    analyze_data()
