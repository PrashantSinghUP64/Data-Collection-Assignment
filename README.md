# Data Collection and Processing Assignment

> **Course:** Python for Data Engineering | **Total Marks:** 100

---

## Project Overview

A modular, multi-stage data-engineering pipeline that:

1. Fetches user records from a REST API (JSONPlaceholder)
2. Scrapes book listings across **multiple pages** of [books.toscrape.com](https://books.toscrape.com)
3. Processes and cross-joins both datasets into structured JSON
4. Performs multi-dimensional statistical analysis using **Pandas**

---

## Project Structure

```
Assignment/
├── config.py            # Central configuration (URLs, paths, constants)
├── utils.py             # Shared utilities: JSON I/O, rotating logger
├── api_data.py          # Part A — API Data Collection
├── web_scraping.py      # Part B — Multi-page Web Scraping
├── json_processing.py   # Part C — JSON Processing & Reporting
├── analysis.py          # Part D — Pandas-powered Data Analysis
├── main.py              # Menu-driven CLI entry point
├── requirements.txt     # Python dependencies
├── tests/
│   ├── test_api.py      # 11 unit tests for api_data.py
│   └── test_scraper.py  # 13 unit tests for web_scraping.py
├── users.json           # Generated — API output (name, username, email, company)
├── books.json           # Generated — Scraper output (100 books, 5 pages)
├── report.json          # Generated — Combined summary report
├── pipeline.log         # Generated — Rotating log file
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

### 2. Install All Dependencies
```bash
pip install -r requirements.txt
```

> **Dependencies:** `requests`, `beautifulsoup4`, `pandas`, `pytest`

---

## Running the Project

### Option 1 — Interactive Menu (Recommended)
```bash
python main.py
```
Select from the on-screen menu:
- `[1]` Fetch API Data (Part A)
- `[2]` Scrape Book Data (Part B)
- `[3]` Process JSON Data (Part C)
- `[4]` Analyse Data (Part D)
- `[5]` Run Full Pipeline (A → D automatically)
- `[6]` Exit

### Option 2 — Run Each Module Directly
```bash
python api_data.py        # Part A → users.json
python web_scraping.py    # Part B → books.json (100 books from 5 pages)
python json_processing.py # Part C → report.json
python analysis.py        # Part D → console statistical output
```

### Option 3 — Run Unit Tests
```bash
python -m pytest tests/ -v
```
> Expected: **24 tests passed**

---

## Output Files

| File | Description |
|---|---|
| `users.json` | 10 user records: name, **username**, email, company |
| `books.json` | Up to 100 books: title, price (`£X.XX`), numeric_price, rating |
| `report.json` | Summary: totals, avg price, high-rated count, group-company users |
| `pipeline.log` | Rotating log file (INFO/DEBUG, max 1 MB, 3 back-ups) |

---

## Key Features

| Feature | Implementation Detail |
|---|---|
| **Central Config** | `config.py` — zero hardcoded values in pipeline modules |
| **No Code Duplication** | `utils.py` — shared `load_json_file`, `save_json_file`, `get_logger` |
| **Multi-Page Scraping** | Follows pagination links up to `SCRAPE_MAX_PAGES` (default: 5 pages = 100 books) |
| **Encoding Safety** | `response.encoding = "utf-8"` + Unicode `\u00a3` for clean `£` in JSON |
| **Per-Record Validation** | Every record validated for type and required fields before processing |
| **Layered Exception Handling** | `HTTPError`, `ConnectionError`, `Timeout`, `FileNotFoundError`, `JSONDecodeError` |
| **File + Console Logging** | `RotatingFileHandler` (1 MB, 3 back-ups) + StreamHandler via `utils.get_logger()` |
| **Rich Data Analysis** | Mean, median, std dev, quartiles, IQR, email domains, value picks |
| **Unit Tests** | 24 tests covering API, scraper helpers, pagination, error cases |

---

## Analysis Outputs (Part D)

**User Analysis:**
- Total user count
- Unique company count
- Top 5 companies by user frequency
- Email domain distribution

**Book Analysis:**
- Full price descriptive stats (mean, median, std, min, max)
- Quartile distribution (Q1, Q3, IQR)
- Count of books above/below average price
- Highest-rated books (5★)
- Rating frequency distribution (1★–5★)
- Best-value picks (rating ≥ 4, sorted by price)

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

## Assignment Coverage

| Part | Module | Tasks Covered |
|---|---|---|
| A — API Data Collection | `api_data.py` | A1 (display), A2 (count), A3 (companies), A4 (dict), A5 (save) |
| B — Web Scraping | `web_scraping.py` | B1–B3 (extract), B4 (stats), B5 (save) |
| C — JSON Processing | `json_processing.py` | C1 (counts), C2 (filter), C3 (search), C4 (report) |
| D — Data Analysis | `analysis.py` | Full multi-dimensional statistical analysis |
