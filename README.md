## About This Project
This project scrappes the data from wikidot 5e and stores the data in a postgreSQL database.

## Technologies
This project uses python to scrape the data and a docker instance of postgreSQL as the database.

## Installation
* Ensure [Python 3.8+](https://www.python.org/downloads/) is installed 
* Ensure [Docker](https://docs.docker.com/get-started/get-docker/) is installed
* Python Libraries 
```sh
pip install requests beautifulsoup4 psycopg2 dotenv flask
```

## Usage
In order to run this us `docker-compose up -d` and once the container is up run the python script `python scrapper.py`

## Database
Connect to the PGAdmin by using the login and email specified in the `.env` file. <br>
Then in the connection tab enter the hostname as the service name in the docker-compose file (default db).

## API
The default for the flask API is localhost `127.0.0.1` port 5000 <br>
Specify multiple variables using the following notation `{Endpoint}?{Varibale}={value}&{Additional variable}={value}`
