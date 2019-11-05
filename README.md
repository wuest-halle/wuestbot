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
python -m venv venv
```
3. Install the dependencies:

``` bash
pip install -r requirements.txt
```

## Database
The database schema can be recreated at any time via `bot/app/database/db_create.py`.
Database population is twofold: users are automatically added via the `\start` command upon first conversation initilization. Events, artists and their relations are added via `db_update.py` also residing in the `app/database` subdirectory. It provides a very small CLI to insert new data, using the classes provided in `db_objects.py`.

The EMR of the database is as follows:

![Database EMR](static/dbuml.png)

## License

[GPLv3](https://choosealicense.com/licenses/gpl-3.0/)