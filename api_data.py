import requests
import json

def fetch_api_data():
    print("--- Part A: API Data Collection ---")
    url = "https://jsonplaceholder.typicode.com/users"
    response = requests.get(url)
    
    if response.status_code != 200:
        print("Failed to fetch data from API")
        return
    
    users = response.json()
    
    # Task A1: Fetch all user records and display specific fields
    print("\n[Task A1] User Records:")
    for user in users:
        print(f"Name: {user.get('name')}, Username: {user.get('username')}, Email: {user.get('email')}, Company: {user.get('company', {}).get('name')}")
        
    # Task A2: Count total number of users
    total_users = len(users)
    print(f"\n[Task A2] Total Users: {total_users}")
    
    # Task A3: Extract all company names
    company_names = [user.get('company', {}).get('name') for user in users if user.get('company')]
    print(f"\n[Task A3] Company Names: {company_names}")
    
    # Task A4: Create Python dictionary
    processed_users = []
    for user in users:
        processed_users.append({
            "name": user.get('name'),
            "email": user.get('email'),
            "company": user.get('company', {}).get('name')
        })
    print("\n[Task A4] Created processed user list of dictionaries.")
        
    # Task A5: Save into users.json
    with open('users.json', 'w') as f:
        json.dump(processed_users, f, indent=4)
    print("[Task A5] Saved processed API data to users.json.\n")

if __name__ == "__main__":
    fetch_api_data()
