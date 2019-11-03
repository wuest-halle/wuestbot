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

        e_name = input("Enter Event-name: ")
        date = input("Enter date (format DD.MM.YYYY): ")
        time = input("Enter event time: ")
        admission = input("Enter admission: ")
        desc = input("Enter description: ")
        loca = input("Enter location name: ")
        e_pic_id = input("Enter the PicID: ")

        event = Event(e_name, date, time, admission, desc, loca, e_pic_id)
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