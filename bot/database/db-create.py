#!/usr/bin/env python3

"""
This script sets up the database as needed for the project. It is not really a 
module of the bot since it is not imported somewhere but just resides here for
later reference and if the re-creation of the db should be necessary. 
For further understanding see corresponding UML diagram.
"""

""" to do:
- error management
- understand, how another table might be necessary for artist - event relation
"""

import sqlite3

conn = sqlite3.connect('data.sqlite')
curs = conn.cursor()

curs.execute("""
    create table Users (integer uID primary key, text name)
    """)

curs.execute("""
    create table Events (integer eID primary key, text name, text date, 
    text time, text desc, text admission, text picID)
    """)

curs.execute("""
    create table Artists (text name primary key, text website, text soundcloud, 
    text bandcamp, text bio, text picID)
    """)