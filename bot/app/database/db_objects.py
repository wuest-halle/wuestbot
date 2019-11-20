#-*- coding: utf-8 -*-

"""Classes representing database items

To Do :

    playsAt:
        * insert functionality into Event and Artist Classes

    all:
        * fix documentation strings in functions to include:
            * what database item
            * which operations incl. parameters
"""

import sqlite3
import logging
import os

from traceback import print_exc

logging.basicConfig(filename=os.path.abspath('../log.txt'), level=logging.DEBUG)

DB_NAME = os.path.abspath('app/database/data.sqlite')

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
        # TODO: put this in constructor. Also make it possible to
        # automatically create necessary relation.
        self.artists = None

    def insert_event(self):
        """Insert the object into the DB."""

        with sqlite3.connect(DB_NAME) as conn:
            curs = conn.cursor()

            try:
                curs.execute("""
                    insert into Events values (null,?,?,?,?,?,?,?)""",
                    (self.name, self.date, self.time, self.admission, self.description, \
                    self.location, self.pic_id))
                conn.commit()
            except sqlite3.IntegrityError as e:
                logging.error(e)
                print_exc()


    def is_event(self):
        """Checks if the object exists in the database.

        Returns:
            bool
        """

        with sqlite3.connect(DB_NAME) as conn:
            curs = conn.cursor()
            curs.execute("""select * from Events where eName=? and date=?""", (self.name, self.date))
            search = curs.fetchone()

            return search is not None

    @classmethod
    def next(cls):
        """Retrieves the next upcoming event from the db.

        Returns:
            Event object, or None if event doesn't exist.
        """

        with sqlite3.connect(DB_NAME) as conn:
            curs = conn.cursor()

            # Get event from DB.
            curs.execute("""select max(eventID) from Events""")
            event_id = curs.fetchone()
            curs.execute("""select * from Events where eventID=?""", event_id)
            result = curs.fetchone()
            if not result:
                return None

            # Unpack DB result into Event object.
            try:
                event = Event(*result[1:])
            except Exception as e:
                logging.error(f"unable to unpack into Event: {e}")
                print_exc()
                return None

            # Retrieve and set Artists for Event.
            artists_temp = get_artists_event(event.name)
            if artists_temp:
                event.artists = [a.name for a in artists_temp]
            else:
                event.artists = []

            return event


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

    @classmethod
    def get_user(cls, u_id):
        """Retrieves a User from the database.

        Args:
            uid (string): The user ID given by Telegram

        Returns:
            A User object or None, if not found in the DB.
        """

        with sqlite3.connect(DB_NAME) as conn:
            curs = conn.cursor()
            curs.execute("select * from Users where uID=?", (u_id, ))
            result = curs.fetchone()
            if not result:
                return None

            try:
                user = User(*result)
            except Exception as e:
                logging.error(e)
                print_exc()

            return user

    @classmethod
    def exists_in_db(cls, u_id):
        """Checks if a user ID is present in the database.

        Args:
            u_id (str): The user ID to be checked.

        Returns:
            True if the user exists, False otherwise.
        """

        return User.get_user(u_id) is not None

    @classmethod
    def all_in_db(cls):
        """Retrieves all users from the DB.

        Returns:
            A list of User objects, or None.
        """

        with sqlite3.connect(DB_NAME) as conn:
            curs = conn.cursor()
            curs.execute("select * from Users where isBot=0")
            result = curs.fetchall()
            if not result:
                return None

            users = [User(*e) for e in result]
            return users

    def delete_from_db(self):
        """Deletes the user from the database.

        Checks if the user exists first.

        Returns:
            True if user has been deleted, False otherwise.
        """

        if not User.exists_in_db(self.u_id):
            return False

        with sqlite3.connect(DB_NAME) as conn:
            curs = conn.cursor()
            curs.execute("DELETE FROM Users WHERE uID=?", (self.u_id, ))
            conn.commit()
            return not User.exists_in_db(self.u_id)

    def add_user(self):
        """Adds a User to the database."""

        with sqlite3.connect(DB_NAME) as conn:
            curs = conn.cursor()
            try:
                curs.execute("insert into Users values (?,?,?)", (self.u_id, \
                    self.name, self.is_bot))
                conn.commit()
            except sqlite3.IntegrityError as e:
                # TODO: print with app.pex()
                logging.error(e)
                print_exc()


def get_artists_event(e_name):

    """Retrieves all artists playing at a certain event.

    Arguments:
        e_name (str): name of the event to look for

    Returns:
        A list of PlaysAt Objects, or None.
    """
    with sqlite3.connect(DB_NAME) as conn:
        curs = conn.cursor()
        curs.execute("select aName from PlaysAt where eName=?", (e_name, ))
        result = curs.fetchall()

        if not result:
            logging.debug(f"no artists for event '{e_name}'")
            return None

        result = [item[0] for item in result]

        artists = None
        try:
            artists = [get_artist(artist) for artist in result]
        except Exception as e:
            # TODO: print with app.pex()
            logging.error(e)
            print_exc()

        return artists

def get_artist(a_name):

    """Retrieves artist from db

    Arguments:
        a_name (str): name of the artist to look for

    Returns:
        Artist object
    """

    with sqlite3.connect(DB_NAME) as conn:
        curs = conn.cursor()
        artist = None
        try:
            curs.execute("select * from Artists where aName=?", (a_name, ))
            artist = Artist(*curs.fetchone())
        except Exception as e:
            # TODO: print with app.pex()
            logging.error(e)
            print_exc()

        return artist
