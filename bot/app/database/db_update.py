#!/usr/bin/env python3

"""
updater script for the database. Each Table (except Users) is represented in a 
class, objects get created after the logic in the __main__ clause at the end

written by softbobo October 2019
"""

""" To Do:
- validity checks for proper date format etc
- input functions for data
- default values for data 
"""

from db_objects import Artist, Event, PlaysAt

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

def new_event():

        e_name = input("Enter Event-name: ")
        date = input("Enter date (format DD.MM.YYYY): ")
        time = input("Enter event time: ")
        admission = input("Enter admission: ")
        desc = input("Enter description: ")
        e_pic_id = input("Enter the PicID: ")

        event = Event(e_name, date, time, admission, desc, e_pic_id)
        event.insert_event()

def new_artist():

        a_name = input("Enter the Artist's name: ")
        webs = input("Enter Website: ")
        soundc = input("Enter Soundcloud account: ")
        bandc = input("Enter Bandcamp Profile: ")
        bio = input("Enter Bio: ")
        a_pic_id = input("Enter the PicID: ")

        artist = Artist(a_name, webs, soundc, bandc, bio, a_pic_id)
        artist.insert_artist()

def plays_at_relation():

        a_name = input("Enter the Artist's name: ")
        e_name = input("Enter the Event's name: ")
        date = input("Enter the Event's date (format DD.MM.YYYY): ")

        plays_at = PlaysAt(a_name, e_name, date)
        PlaysAt.check_for_artist()
        PlaysAt.check_for_event()
        PlaysAt.insert_plays_at()