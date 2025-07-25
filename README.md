# Weather Scraper
Quick script for scraping and parsing weather data. Format is a table that contains a superset of columns avaliable from historic ncdc data (https://www.ncei.noaa.gov/).
NCDC currently provides a lagged historic data set so this will allow complete T-1 data when used together. 

## Setup
1. Install Poetry: `pip install poetry`
2. Install dependencies: `poetry install`
3. Run the platform: `poetry run python src/main.py`


## Extract of Example Output 

|FIELD1|STATION                      |NAME  |DATE                                         |RELEASE_DATE|TIME |AWND|PGTM|PRCP|SNOW|SNWD|TAVG|TMAX|TMIN|WDF2|WDF5|WSF2|WSF5|WT01|WT02|WT03|WT06|WT08|
|------|-----------------------------|------|---------------------------------------------|------------|-----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|
|1     |CLINYC                       |Central Park NY|2025-07-24                                   |2025-07-25  |02:18|4.3 |    |0.0 |0.0 |0.0 |79  |87  |70  |210 |240 |10  |20  |0   |0   |0   |0   |0   |
|2     |CLINYC                       |Central Park NY|2025-07-24                                   |2025-07-24  |16:32|4.5 |    |    |    |0.0 |79  |87  |70  |210 |240 |10  |20  |0   |0   |0   |0   |0   |
