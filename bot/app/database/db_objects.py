""" Do Do :

playsAt:
- insert functionality into Event and Artist Classes

all:
- close the connection somewhere (might be at __exit__)
- fix documentation strings in functions to include: 
    - what database item
    - which operations incl. parameters
- add logging, catch errors to log
"""

import sqlite3
import logging

DB_NAME = 'data.sqlite'

class Event:

    """
    An instance of the Event relation 
    """

    def __init__(self, e_name, date, time, admi, desc, e_pic_id):
        
        
        self.e_name = e_name
        self.date = date
        self.time = time
        self.admi = admi
        self.desc = desc
        self.e_pic_id = e_pic_id

        self.insert_event()
    
    def insert_event(self):
        
        conn = sqlite3.connect(DB_NAME)
        curs = conn.cursor()

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
        conn.close()
        
class Artist:

    def __init__(self, a_name, webs, soundc, bandc, bio, a_pic_id):

        self.a_name = a_name
        self.webs = webs
        self.soundc = soundc
        self.bandc = bandc
        self.bio = bio
        self.aPicID = a_pic_id

        self.insert_artist()
        

    def insert_artist(self):
        
        conn = sqlite3.connect(DB_NAME)
        curs = conn.cursor()

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
        conn.close()

class playsAt:

    """
    Instance represents Artist-Event connection (aka playsAt Table)
    """

    def __init__(self):

        self.conn = sqlite3.connect(DB_NAME)
        
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
        loggin.error(e)

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
