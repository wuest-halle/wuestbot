#!/usr/bin/env python3

"""
updater script for the database. every entry has to be added manually
"""

""" Do Do - Events:
- error checks for proper string formats in date, ePicID
- might make datetime() object for the date column

playsAt:

- the check functions are really bulky and do the same things over and over
so they should really be streamlined

all:

- close the connection somewhere (might be at __exit__)
- add program logic to constructors
"""

import sqlite3

class Event:

    """
    An instance of the Event relation 
    """

    def __init__(self):
        
        self.conn = sqlite3.connect('data.sqlite')
        
        self.eName = input("Enter Event-name: ")
        self.date = input("Enter date (format DD.MM.YYYY): ")
        self.time = input("Enter event time: ")
        self.admission = input("Enter admission: ")
        self.desc = input("Enter description: ")
        self.ePicID = input("Enter the PicID: ")

        self.insert_event()
        self.conn.close()
    
    def insert_event(self):
        
        curs = self.conn.cursor()

        try:
            curs.execute("""
                insert into Events values (?,?,?,?,?,?)""",
                (self.eName, self.date, self.time, self.admission, self.desc, \
                self.ePicID))
            self.conn.commit()
        
        except sqlite3.IntegrityError:
            print("Event already exists in DB")
            return
        
        curs.close()
        
class Artist:

    def __init__(self):

        self.conn = sqlite3.connect('data.sqlite')
        
        self.aName = input("Enter the Artist's name: ")
        self.webs = input("Enter Website: ")
        self.soundc = input("Enter Soundcloud account: ")
        self.bandc = input("Enter Bandcamp Profile: ")
        self.bio = input("Enter Bio: ")
        self.aPicID = input("Enter the PicID: ")

        self.insert_artist()
        
        self.conn.close()

    def insert_artist(self):
        
        curs = self.conn.cursor()

        try:
            curs.execute("""
                insert into Artists values (?,?,?,?,?,?)""",
                (self.aName, self.webs, self.soundc, self.bandc, self.bio, \
                self.aPicID))
            self.conn.commit()
        
        except sqlite3.IntegrityError:
            print("Artist already exists in DB")
            return
        
        curs.close()

class playsAt:

    """
    Instance represents Artist-Event connection (aka playsAt Table)
    """

    def __init__(self):

        self.conn = sqlite3.connect('data.sqlite')
        
        self.aName = input("Enter the Artist's name: ")
        self.eName = input("Enter the Event's name: ")
        self.date = input("Enter the Event's date (format DD.MM.YYYY): ")

        self.check_for_artist()
        self.check_for_event()
        self.insert_plays_at()

        self.conn.close()

    def check_for_artist(self):
        
        curs = self.conn.cursor()
        curs.execute("select * from Artists where aName=?", (self.aName, ))
        artist = curs.fetchone()
        
        if artist:
            print("Corresponding artist found! Check: \n", artist)
            answ = input("Is this the right entry? [Y/n]" )
            if answ == "Y":
                pass
            else:
                self.aName = input("Please re-enter artist-name: ")
                check_for_artist()
        else: 
            self.aName = input("Please re-enter artist-name: ")
            self.check_for_artist()

    def check_for_event(self):

        curs = self.conn.cursor()
        curs.execute("select * from Events where eName=? and date=?", (self.eName, self.date))
        event = curs.fetchone()

        if event:
            print("Corresponding event found! Check: \n", event)
            answ = input("Is this the right entry? [Y/n]" )
            if answ == "Y":
                pass
            else:
                self.eName = input("Please re-enter event-name: ")
                check_for_event()
        else: 
            self.eName = input("Please re-enter event-name: ")
            self.check_for_event()

    def insert_plays_at(self):
        
        curs = self.conn.cursor()

        try:
            curs.execute("""
                insert into playsAt values (?,?,?)""",
                (self.aName, self.eName, self.date))
            self.conn.commit()
        
        except sqlite3.IntegrityError:
            print("Connection already exists in DB")
            return
        
        curs.close()

if __name__ == "__main__":
    
    proceed = "Y"

    while proceed == "Y":
        
        rel_type = input("""
        What should be entered in the DB? 
        E - Event
        A - Artist
        P - Artist-Event Relation
        C - Cancel  \n
        """)
    
        if rel_type == "E":
            ev = Event()
        elif rel_type == "A":
            ar = Artist()
        elif rel_type == "P":
            pa = playsAt()
        else:
            print("Program is shut down")
            exit()

        proceed = input("Enter more data? [Y/n]")