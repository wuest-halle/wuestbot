#-*- coding: utf-8 -*-

"""Classes representing database items 

To Do :

    playsAt:
        * insert functionality into Event and Artist Classes

    all:
        * fix documentation strings in functions to include: 
            * what database item
            * which operations incl. parameters
        * add logging, catch errors to log
"""

import sqlite3
import logging
import os

logging.basicConfig(os.path.abspath('../log.txt', level=logging.DEBUG))

DB_NAME = 'data.sqlite'

class Event:

    """
    An instance of the Event relation 
    """

    def __init__(self, name, date, time, admission, description, location, pic_id):
        
        
        self.name = name
        self.date = date
        self.time = time
        self.admission = admission
        self.description = description
        self.location = location
        self.pic_id = pic_id
    
    def insert_event(self):
        
        conn = sqlite3.connect(DB_NAME)
        curs = conn.cursor()

        try:
            curs.execute("""
                insert into Events values (?,?,?,?,?,?)""",
                (self.e_name, self.date, self.time, self.admission, self.description, \
                self.pic_id))
            self.conn.commit()
        except sqlite3.IntegrityError as e:
            logging.error(e)
        
        curs.close()
        conn.close()
        
class Artist:

    def __init__(self, name, website, soundcloud, bandcamp, bio, pic_id):

        self.name = name
        self.website = website
        self.soundcloud = soundcloud
        self.bandcamp = bandcamp
        self.bio = bio
        self.pic_id = pic_id
        
    def insert_artist(self):
        
        conn = sqlite3.connect(DB_NAME)
        curs = conn.cursor()

        try:
            curs.execute("""
                insert into Artists values (?,?,?,?,?,?)""",
                (self.name, self.website, self.soundcloud, self.bandcamp, self.bio, \
                self.pic_id))
            self.conn.commit() 
        except sqlite3.IntegrityError as e:
            logging.error(e)
        
        curs.close()
        conn.close()

class PlaysAt:

    """
    Instance represents Artist-Event connection (aka playsAt Table)
    """

    def __init__(self, artist_name, event_name, date):
        
        self.artist_name = artist_name
        self.event_name = event_name
        self.date = date

    def check_for_artist(self):
        
        conn = sqlite3.connect(DB_NAME)
        curs = conn.cursor()
        
        curs.execute("select * from Artists where name=?", (self.name, ))
        artist = curs.fetchone()
        
        if artist:
            print("Corresponding artist found! Check: \n", artist)
            answ = input("Is this the right entry? [Y/n]" )
            if answ == "Y":
                pass
            else:
                self.name = input("Please re-enter artist-name: ")
                check_for_artist()
        else: 
            self.name = input("Please re-enter artist-name: ")
            self.check_for_artist()

        curs.close()
        conn.close()

    def check_for_event(self):
        
        conn = sqlite3.connect(DB_NAME)
        curs = conn.cursor()
        
        curs.execute("select * from Events where eName=? and date=?", (self.event_name, self.date))
        event = curs.fetchone()

        if event:
            print("Corresponding event found! Check: \n", event)
            answ = input("Is this the right entry? [Y/n]" )
            if answ == "Y":
                pass
            else:
                self.e_name = input("Please re-enter event-name: ")
                check_for_event()
        else: 
            self.e_name = input("Please re-enter event-name: ")
            self.check_for_event()

        curs.close()
        conn.close()

    def insert_plays_at(self):
        
        conn = sqlite3.connect(DB_NAME)
        curs = conn.cursor()

        try:
            curs.execute("""
                insert into playsAt values (?,?,?)""",
                (self.artist_name, self.event_name, self.date))
            self.conn.commit()
       except sqlite3.IntegrityError as e:
            logging.error(e)
        
        curs.close()
        conn.close()

class User:

    def __init__(self, u_id, u_name, is_bot):

        self.u_id = u_id
        self.u_name = u_name
        self.is_bot = is_bot

    def get_user(u_id):

    conn = sqlite3.connect(DB_NAME)
    curs = conn.cursor()

    curs.execute("select * from Users where uID=?", (u_id, ))
    user = curs.fetchone()

    curs.close()
    conn.close()

    if user: 
        return True
    else:
        return False

    def add_user(u_id, u_name, is_bot):

    conn = sqlite3.connect(DB_NAME)
    curs = conn.cursor()

    try:
        curs.execute("insert into Users values (?,?,?)" (u_id, u_name, is_bot))
        conn.commit()
    except Error as e:
        logging.error(e)

    curs.close()
    conn.close()

    def all_users():

    conn = sqlite3.connect(DB_NAME)
    curs = conn.cursor()

    curs.execute("select * from Users where isBot=0")
    users = curs.fetchall()
    
    conn.close()
    curs.close()
    
    return users