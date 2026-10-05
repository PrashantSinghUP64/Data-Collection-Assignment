# Data Collection and Processing Assignment
> **Course:** Python for Data Engineering | **Total Marks:** 100

---

## Project Overview

A modular data-engineering pipeline that:
1. Fetches user records from a REST API (JSONPlaceholder)
2. Scrapes book listings from [books.toscrape.com](https://books.toscrape.com)
3. Processes and combines both datasets into structured JSON
4. Performs quantitative analysis using **Pandas**

---

## Project Structure

```
Assignment/
├── api_data.py          # Part A — API Data Collection
├── web_scraping.py      # Part B — Web Scraping
├── json_processing.py   # Part C — JSON Processing
├── analysis.py          # Part D — Data Analysis
├── utils.py             # Shared utility (JSON loading + validation)
├── main.py              # Menu-driven CLI entry point
├── requirements.txt     # Python dependencies
├── users.json           # Generated — API output
├── books.json           # Generated — Scraper output
├── report.json          # Generated — Combined summary
├── screenshots/         # Assignment output screenshots
└── README.md
```

---

## Setup

### 1. Clone the Repository
```bash
git clone https://github.com/PrashantSinghUP64/Data-Collection-Assignment.git
cd Data-Collection-Assignment
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

> **Dependencies:** `requests`, `beautifulsoup4`, `pandas`

---

## Running the Project

### Option 1 — Interactive Menu (Recommended)
```bash
python main.py
```
Follow the on-screen menu to run each part individually or the full pipeline.

### Option 2 — Run Each Module Directly
```bash
python api_data.py        # Part A — Fetch API data → users.json
python web_scraping.py    # Part B — Scrape books   → books.json
python json_processing.py # Part C — Process JSON   → report.json
python analysis.py        # Part D — Analyse data
```

---

## Output Files

| File | Description |
|---|---|
| `users.json` | 10 user records with name, username, email, company |
| `books.json` | 20 book records with title, price (clean £), rating |
| `report.json` | Combined summary: totals, averages, counts |

---

## Features

| Feature | Detail |
|---|---|
| API Integration | `requests` with timeout, User-Agent header, layered exception handling |
| Web Scraping | `BeautifulSoup` with `response.encoding = utf-8` to prevent `Â£` artifacts |
| JSON Processing | Per-record schema validation, UTF-8 storage, combined report |
| Data Analysis | Pandas DataFrames, frequency-based company ranking, rating distribution |
| Code Design | OOP classes, shared `utils.py`, no code duplication |
| Error Handling | `HTTPError`, `ConnectionError`, `Timeout`, `FileNotFoundError`, `JSONDecodeError` |

---

## Screenshots

### 1. API Data Collection Output
![API Output](screenshots/api_output.png)

### 2. Web Scraping Output
![Scraping Output](screenshots/scraping_output.png)

### 3. JSON Processing Output
![JSON Output](screenshots/json_processing_output.png)

### 4. Data Analysis Output
![Analysis Output](screenshots/analysis_output.png)

### 5. Main Menu
![Main Menu](screenshots/main_menu.png)

---

## Assignment Parts Covered

| Part | Module | Marks |
|---|---|---|
| A — API Data Collection | `api_data.py` | 30 |
| B — Web Scraping | `web_scraping.py` | 30 |
| C — JSON Processing | `json_processing.py` | 20 |
| D — Data Analysis | `analysis.py` | 20 |
