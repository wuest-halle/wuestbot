#!/usr/bin/env python3

"""
updater script for the database. every entry has to be added manually
"""

""" Do Do - Events:
- error checks for proper string formats in date, ePicID
- might make datetime() object for the date column
- close the connection somewhere (might be at __exit__)
"""

import sqlite3

class Event:

    """
    The representation of a single row in the Events table
    """

    def __init__(self):
        
        self.conn = sqlite3.connect('data.sqlite')
        
        self.eName = input("Enter Event-name: ")
        self.date = input("Enter date (format DD.MM.YYYY): ")
        self.time = input("Enter event time: ")
        self.admission = input("Enter admission: ")
        self.desc = input("Enter description: ")
        self.ePicID = input("Enter the PicID: ")
    
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
        