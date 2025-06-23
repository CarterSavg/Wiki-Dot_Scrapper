## About This Project
This project scrappes the data from wikidot 5e and stores the data in a postgreSQL database.

## Technologies
This project uses python to scrape the data and a docker instance of postgreSQL as the database.

## Installation
* Ensure [Python 3.8+](https://www.python.org/downloads/) is installed 
* Ensure [Docker](https://docs.docker.com/get-started/get-docker/) is installed
* Python Libraries 
```sh
pip install requests beautifulsoup4 psycopg2 dotenv
```

## Usage
In order to run this us `docker-compose up -d` and once the container is up run the python script `python scrapper.py`
