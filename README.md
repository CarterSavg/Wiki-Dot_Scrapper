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

### Enpoints
`/` Return all spells <br>
`/spell/like/<spell_name>` Return all spells with the name passed within the spell name (not case sensitive). <br>
`/spell/strict/<spell_name>` Return all spells with the exact name passed (not case sensitive). <br>
`/spell/level/upper/<spell_level>` Returns all the spells of the level provided or lower. <br>
`/spell/level/range` Returns all the spells within the given level range. <br>
`/spell/time/<casting_time>` Returns all the spells with the given casting time. <br>
`/spell/time/range/<casting_time>` Returns all the spells with the given casting time range. <br>
`/spell/user/<caster>` Returns all the spells that the specified caster is able to cast. <br>
`/spell/school/<school>` Returns all the spells that are in the specific school. (Comma delimited) <br>
`/spell/duration/<duration>` TODO <br>
`/spell/range/<range>` TODO <br>
`/spell/filter/all` Returns all the spells within the given parameters. Input: Level (Upper and lower), Casting time, Name, Level, School, Users