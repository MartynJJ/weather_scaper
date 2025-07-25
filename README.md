# Weather Scraper
Quick script for scraping and parsing weather data. Format is a table that contains a superset of columns avaliable from historic ncdc data (https://www.ncdc.noaa.gov/cdo-web/cart).
NCDC currently provides a lagged historic data set so this will allow complete T-1 data when used together. 

## Setup
1. Install Poetry: `pip install poetry`
2. Install dependencies: `poetry install`
3. Run the platform: `poetry run python src/main.py`
