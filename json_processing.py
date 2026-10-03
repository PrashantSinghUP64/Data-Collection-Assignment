import json

def process_json_data():
    print("--- Part C: JSON Processing ---")
    
    try:
        with open('users.json', 'r') as f:
            users = json.load(f)
        with open('books.json', 'r') as f:
            books = json.load(f)
    except FileNotFoundError:
        print("Required JSON files not found. Please run tasks A and B first.")
        return
        
    # Task C1: Print total records
    print(f"\n[Task C1] Total Users Records: {len(users)}")
    print(f"[Task C1] Total Books Records: {len(books)}")
    
    # Task C2: Display all book titles with rating greater than 4
    print("\n[Task C2] Books with rating greater than 4:")
    high_rating_books = [book['title'] for book in books if book.get('rating', 0) > 4]
    for title in high_rating_books:
        print(f"- {title}")
        
    # Task C3: Display all users belonging to companies whose name contains "Group"
    print("\n[Task C3] Users in companies containing 'Group':")
    group_users = [user for user in users if "Group" in user.get('company', '')]
    for user in group_users:
        print(f"- {user.get('name')} ({user.get('company')})")
        
    # Task C4: Create a combined JSON report
    avg_price = sum(b.get('numeric_price', 0) for b in books) / len(books) if len(books) > 0 else 0
    
    report = {
        "total_users": len(users),
        "total_books": len(books),
        "average_price": round(avg_price, 2)
    }
    
    with open('report.json', 'w') as f:
        json.dump(report, f, indent=4)
        
    print(f"\n[Task C4] Saved combined report to report.json: {report}\n")

if __name__ == "__main__":
    process_json_data()
