#!/usr/bin/env python3

"""
This script sets up the database as needed for the project. It is not really a
module of the bot since it is not imported somewhere but just resides here for
later reference and if the re-creation of the db should be necessary.
For further understanding see corresponding UML diagram.
"""

""" to do:
- might check for long strings in descriptions etc
"""

import sqlite3
import logging
import os
from database.db_objects import db_name


logging.basicConfig(filename=os.path.abspath('log.txt'), level=logging.DEBUG)

def create_db(db_name):
    conn = sqlite3.connect(db_name)
    curs = conn.cursor()

    curs.execute("""
        create table if not exists Users (
        uID integer primary key,
        uName text,
        isBot bool)
        """)

    curs.execute("""
        create table if not exists Events (
        eName text,
        date text,
        time text,
        desc text,
        admission text,
        ePicID text,
        loca text,
        unique (eName, date))
        """)

    curs.execute("""
        create table if not exists Artists (
        aName text primary key,
        website text,
        soundcloud text,
        bandcamp text,
        bio text,
        aPicID text)
        """)

    curs.execute("""
        create table if not exists PlaysAt (
        aName text,
        eName text,
        date text,
        foreign key (aName) references Artists (aName),
        foreign key (eName, date) references Events (eName, date)
        )
        """)

if __name__ == "__main__":
    print(f"setting up {db_name()}")
    create_db(db_name())
