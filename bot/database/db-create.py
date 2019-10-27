#!/usr/bin/env python3

"""
This script sets up the database as needed for the project. It is not really a 
module of the bot since it is not imported somewhere but just resides here for
later reference and if the re-creation of the db should be necessary. 
For further understanding see corresponding UML diagram.
"""

""" to do:
- error management
- introduce foreign keys to playsAt table
"""

import sqlite3

conn = sqlite3.connect('data.sqlite')
curs = conn.cursor()

curs.execute("""
    create table Users (uID integer primary key, uName text)
    """)

curs.execute("""
    create table Events (eID integer primary key, eName text, date text, 
    time text, desc text, admission text, ePicID text)
    """)

curs.execute("""
    create table Artists (aName text primary key, website text, soundcloud text, 
    bandcamp text, bio text, aPicID text)
    """)

curs.execute("""
    create table playsAt (aName text, eID integer, foreign key (aName, eID) 
    references Artists (aName), Events (eID)
    )
    """)