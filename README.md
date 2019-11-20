# WUESTbot

Telegram Newsletter Bot for WUEST in the making.

Installation on your local machine:

Note, that this was written in Python 3.7. If you are still on 2.7, upgrade!

1. Clone this folder and change to your new local directory (aka the clone)

``` bash
git clone git@github.com:wuest-halle/wuestbot.git
cd wuestbot
```

2. Create a new Python venv:

``` bash
python3 -m venv venv
source venv/bin/activate
```

3. Install the dependencies:

``` bash
pip install -r requirements.txt
```

## Startup

First configure your environment:

```shell
cat > .env <<EOF
# The API token to authenticate against Telegram
API_TOKEN=abcd123
# The Telegam user / chat IDs that are allowed to push messages
# to all users in the database
ADMINS=1235123,67342347,89945234
EOF
```

Use `start.sh` to setup the database and create a `gunicorn` server in front
of the bot:

```shell
./start.sh
```

Alternatively you can set up the DB manually:

```shell
cd bot/app/database
./db_create.py
```

## Populating the DB

You can enter data by running `app/database/db_update.py`:

```shell
# Needs to be run from the wuestbot/bot directory.
$ ./app/database/db_update.py

        What should be entered in the DB?
        E - Event
        A - Artist
        P - Artist-Event Relation
        C - Cancel


```

## Database

The database schema can be recreated at any time via `bot/app/database/db_create.py`.
Database population is twofold: users are automatically added via the `\start` command upon first conversation initilization. Events, artists and their relations are added via `db_update.py` also residing in the `app/database` subdirectory. It provides a very small CLI to insert new data, using the classes provided in `db_objects.py`. Manual inputs to the db have to look like this:

- __Events__:
    - eName: string
    - date: string, Format DD.MM.YYYY
    - time: string, Format HH:MM
    - description: string, must not exceed 150 characters
    - admission: string
    - ePicID: string, 6 ciphers long, begins with a 0. followed by file ending - e.g. 002378.jpg
- __Artist__:
    - aName: string
    - website: string
    - soundcloud: string
    - bandcamp: string
    - bio: string, must not exceed 150 characters
    - aPicID: string, 6 ciphers long, begins with a 1. followed by file ending - e.g. 100356.jpg
- __PlaysAt__:
    - aName: str, same as Artist.aName
    - eName: str, same as Event.eName
    - date: str, same as Event.date

The EMR of the database is as follows:

![Database EMR](static/dbuml.png)

## License

[GPLv3](https://choosealicense.com/licenses/gpl-3.0/)