# BIN Information API

A Python project that scrapes BIN/IIN information, stores the data in MySQL, and provides CRUD API endpoints using FastAPI.

## Features

- Scrape BIN/IIN data using Requests and BeautifulSoup
- Store scraped data in MySQL
- Create BIN records
- Find BIN records
- Update BIN records
- Delete BIN records
- FastAPI Swagger documentation

## Technologies Used

- Python
- FastAPI
- MySQL
- Requests
- BeautifulSoup
- Pydantic
- python-dotenv

## API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/bin` | Find a BIN |
| POST | `/bin/create` | Create a BIN |
| PUT | `/bin/update` | Update a BIN |
| DELETE | `/bin/delete` | Delete a BIN |

## Project Structure

```text
main.py          # FastAPI application
scraper.py       # Web scraper
test_mysql.py    # CSV to MySQL importer
bin_data.csv     # Scraped BIN data
.env             # Local database credentials
.gitignore       # Files excluded from Git