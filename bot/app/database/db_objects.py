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

logging.basicConfig(filename=os.path.abspath('../log.txt'), level=logging.DEBUG)

DB_NAME = 'app/database/data.sqlite'

class Event:

    """An instance of the Event relation 

    Arguments:
        * name (str): event's name
        * date (str): event's date
        * time (str): event's start time
        * admission (str): admission required at entry
        * description (str): short descriptive text. keep it 150 characters or less
        * location (str): where the event takes place
        * pic_id (str): ID for pictures repository. 6+4 characters long, 
        starts with 0, then number, then file ending like `.jpg`

    The primary key, eventID is added automatically via the query in get_max_event() 
    """

    def __init__(self, name, date, time=None, admission=None, description=None,\
        location=None, pic_id=None):
        
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
                insert into Events values (null,?,?,?,?,?,?,?)""",
                (self.name, self.date, self.time, self.admission, self.description, \
                self.location, self.pic_id))
            conn.commit()
        except sqlite3.IntegrityError as e:
            logging.error(e)
        
        curs.close()
        conn.close()

    def is_event(self):

        conn = sqlite3.connect(DB_NAME)
        curs = conn.cursor()

        curs.execute("""select * from Events where eName=? and date=?""", (self.name, self.date))
        search = curs.fetchone()
        
        curs.close()
        conn.close()

        return search is not None
        
class Artist:

    """An Instance of the Artist relation

    Arguments:
        * name(str): artist's name
        * website(str): artist's website
        * soundcloud(str): artist's soundcloud profile
        * bandcamp(str): artist's bandcamp profile
        * bio(str): short descriptive text about the artist. keep it under 150 characters
        * pic_id(str): ID for corresponding in the repo. 6+4 characters long, 
        starts with 0, then number, then file ending like `.jpg`
    """

    def __init__(self, name, website=None, soundcloud=None, bandcamp=None, \
        bio=None, pic_id=None):

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
            conn.commit() 
        except sqlite3.IntegrityError as e:
            logging.error(e)
        
        curs.close()
        conn.close()

    def is_artist(self):

        conn = sqlite3.connect(DB_NAME)
        curs = conn.cursor()

        curs.execute("""select * from Artists where aName=?""", (self.name, ))
        search = curs.fetchone()
        
        curs.close()
        conn.close()

        return search is not None

class PlaysAt:

    """
    Instance represents Artist-Event connection (aka playsAt Table)
    """

    def __init__(self, artist_name, event_name, date):
        
        self.artist_name = artist_name
        self.event_name = event_name
        self.date = date

    def insert_plays_at(self):
        
        conn = sqlite3.connect(DB_NAME)
        curs = conn.cursor()

        try:
            curs.execute("""
                insert into playsAt values (?,?,?)""",
                (self.artist_name, self.event_name, self.date))
            conn.commit()
        except sqlite3.IntegrityError as e:
            logging.error(e)
        
        curs.close()
        conn.close()

class User:

    """Instance of the User relation:

    Arguments:
        * u_id(str): User-ID, same as the User-ID which Telegram uses
        * name(str): First name of the user
        * is_bot(bool): True if the account is a bot
    """

    def __init__(self, u_id, name, is_bot):

        self.u_id = u_id
        self.name = name
        self.is_bot = is_bot

    def user_exists(self, u_id):

        conn = sqlite3.connect(DB_NAME)
        curs = conn.cursor()

        curs.execute("select * from Users where uID=?", (self.u_id, ))
        user = curs.fetchone()

        curs.close()
        conn.close()

        return user is not None 

    def add_user(self):

        conn = sqlite3.connect(DB_NAME)
        curs = conn.cursor()

        try:
            curs.execute("insert into Users values (?,?,?)", (self.u_id, \
                self.name, self.is_bot))
            conn.commit()
        except sqlite3.IntegrityError as e:
            logging.error(e)

        curs.close()
        conn.close()

    def all_users(self):

        conn = sqlite3.connect(DB_NAME)
        curs = conn.cursor()

        curs.execute("select * from Users where isBot=0")
        users = curs.fetchall()

        conn.close()
        curs.close()

        return users

def get_next_event():

    """Retrieves the next upcoming event from the db

    Returns:
        Event object
    """

    conn = sqlite3.connect(DB_NAME)
    curs = conn.cursor()
    
    curs.execute("""select max(eventID) from Events""")
    event_id = curs.fetchone()
    
    curs.execute("""select * from Events where eventID=?""", event_id)
    temp = [item for item in curs.fetchone()]
    del temp[0]

    try:
        next_event = Event(*temp)
    
        curs.close()
        conn.close()  

        return next_event
    
    except:
        logging.error()

        curs.close()
        conn.close() 

        return None

def get_artists_event(e_name):

    """Retrieves all artists playing at a certain event, returns a list

    Arguments:
        * e_name (str): name of the event to look for
    """

    conn = sqlite3.connect(DB_NAME)
    curs = conn.cursor()

    curs.execute("select aName from PlaysAt where eName=?", (e_name, ))
    artists = curs.fetchall()
    artists = [artist[0] for artist in artists]

    curs.close()
    conn.close()  

    return artists

def get_artist(a_name):

    """Retrieves artist from db

    Arguments:
        a_name (str): name of the artist to look for

    Returns:
        Artist object
    """

    conn = sqlite3.connect(DB_NAME)
    curs = conn.cursor()

    curs.execute("select * from Artists where aName=?", (a_name, ))
    temp = curs.fetchone()

    try:
        artist = Artist(*temp)

        curs.close()
        conn.close()  

        return artist

    except:
        logging.error()

        curs.close()
        conn.close()  

        return None