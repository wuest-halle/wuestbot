#!/usr/bin/env python3
#-*- coding: utf-8 -*-
# written by softbobo October 2019

"""Update/Insert-Script for Items in the Database 
    
    Purpose:
        This script formulates the logic behind inputs for the database, which the bot 
        uses. It is intended for use from the command line and run locally like any 
        script via ``./db-update.py``  

    To Do:
        * validity checks for proper date format etc
        * default values for data 
"""

from db_objects import Artist, Event, PlaysAt

def new_event():

    """input-wrapper for Event class

        asks for the data, makes a new instance of event, and inserts data via the 
        member function
    """

    event_name = input("Enter Event-name: ")
    date = input("Enter date (format DD.MM.YYYY): ")
    time = input("Enter event time: ")
    admission = input("Enter admission: ")
    description = input("Enter description: ")
    locaation = input("Enter location name: ")
    event_pic_id = input("Enter the PicID: ")
    
    event = Event(event_name, date, time, admission, description, location, event_pic_id)
    event.insert_event()

def new_artist():

    """input-wrapper for Artist class

        asks for the data, makes a new instance of artist, and inserts data via the 
        member function
    """

    artist_name = input("Enter the artists's name: ")
    website = input("Enter Website: ")
    soundcloud = input("Enter Soundcloud account: ")
    bandcamp = input("Enter Bandcamp Profile: ")
    bio = input("Enter Bio: ")
    artist_pic_id = input("Enter the PicID: ")
    
    artist = Artist(artist_name, website, soundcloud, bandcamp, bio, artist_pic_id)
    artist.insert_artist()

def plays_at_relation():

    artist_name = find_artist()
    
    try:
        event_name, date = find_event()
    except TypeError:
        return

    plays_at = PlaysAt(artist_name, event_name, date)
    plays_at.insert_plays_at()
    
def find_artist():

    """input-wrapper for the Artist class' find_artist() member

        asks for the data, makes a new instance of artist, and initiates db 
        queries as long as the user wants
    """

    proceed = "Y"

    while proceed == "Y":
        name = input("Enter artist name: ")
        artist = Artist(name)

        if artist.is_artist():
            print("Entry found")
            return name
        else:
            print("Entry not found")
            proceed = input("Continue querying? [Y/n] ")

def find_event():

    """input-wrapper for the Event class' find_event() member

        asks for the data, makes a new instance of Event, and initiates db 
        queries as long as the user wants
    """

    proceed = "Y"

    while proceed == "Y":
        name = input("Enter event name: ")
        date = input("Enter event date (format DD.MM.YYYY): ")
        event = Event(name, date)

        if event.is_event():
            print("Entry found")
            return [name, date]
        else:
            print("Entry not found")
            proceed = input("Continue querying? [Y/n] ")

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
            ev = new_event()
        elif rel_type == "A":
            ar = new_artist()
        elif rel_type == "P":
            pa = plays_at_relation()
        else:
            print("Program is shut down")
            exit()

        proceed = input("Enter more data? [Y/n]")