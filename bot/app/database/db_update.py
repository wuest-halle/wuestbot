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

from db_objects import event, Event, PlaysAt

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

def new_event():

    a_name = input("Enter the event's name: ")
    webs = input("Enter Website: ")
    soundc = input("Enter Soundcloud account: ")
    bandc = input("Enter Bandcamp Profile: ")
    bio = input("Enter Bio: ")
    a_pic_id = input("Enter the PicID: ")
    
    event = event(a_name, webs, soundc, bandc, bio, a_pic_id)
    event.insert_event()

def plays_at_relation():

    a_name = find_event()
    e_name = input("Enter the Event's name: ")
    date = input("Enter the Event's date (format DD.MM.YYYY): ")
    
    plays_at = PlaysAt(a_name, e_name, date)
    PlaysAt.check_for_event()
    PlaysAt.insert_plays_at()

def find_event():

    proceed = "Y"

    while proceed == "Y":
        name = input("Enter event name: ")
        event = event(name)

        if event.is_event():
            print("Entry found")
            return name
        else:
            proceed = ("Continue querying? [Y/n] ")

def find_event():

    proceed = "Y"

    while proceed == "Y":
        name = input("Enter event name: ")
        date = input("Enter event date (format DD.MM.YYYY): ")
        event = Event(name, date)

        if event.is_event():
            print("Entry found")
            return [name, date]
        else:
            proceed = ("Continue querying? [Y/n] ")

if __name__ == "__main__":
    
    proceed = "Y"

    while proceed == "Y":
        
        rel_type = input("""
        What should be entered in the DB? 
        E - Event
        A - event
        P - event-Event Relation
        C - Cancel  \n
        """)
    
        if rel_type == "E":
            ev = new_event()
        elif rel_type == "A":
            ar = new_event()
        elif rel_type == "P":
            pa = plays_at_relation()
        else:
            print("Program is shut down")
            exit()

        proceed = input("Enter more data? [Y/n]")