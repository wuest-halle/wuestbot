#!/usr/bin/env python3

"""
updater script for the database. Each Table (except Users) is represented in a 
class, objects get created after the logic in the __main__ clause at the end

written by softbobo October 2019
"""

""" To Do:
- validity checks for proper date format etc
- input functions for data

"""

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

def new_user():

        self.eName = input("Enter Event-name: ")
        self.date = input("Enter date (format DD.MM.YYYY): ")
        self.time = input("Enter event time: ")
        self.admission = input("Enter admission: ")
        self.desc = input("Enter description: ")
        self.ePicID = input("Enter the PicID: ")

def new_event():

        self.aName = input("Enter the Artist's name: ")
        self.webs = input("Enter Website: ")
        self.soundc = input("Enter Soundcloud account: ")
        self.bandc = input("Enter Bandcamp Profile: ")
        self.bio = input("Enter Bio: ")
        self.aPicID = input("Enter the PicID: ")
