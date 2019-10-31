"""
Helper class for all database operations the bot needs to do

For now, it needs to (not in particular order):
    - query the database for all users (id)
    - add a user to the db. parameters to be added are:
        - user-id (INTEGER PRIMARY KEY)
        - name (TEXT)
        - is_bot (bool) 
    - remove a user from the database (take care b/c of degeneration)
    - close the connection upon shutdown

TO DO:
    - check, if aplication is threadsafe. unclear, how to find out yet
    (for now, check_same_thread is set to False in the connect object)
    - write errorcheck for when a uid is inserted into the db which is
    already there (PRIMARY KEY)
"""

import sqlite3

class Datahandler:

    try:
        conn = sqlite3.connect('tryout.db', check_same_thread=False)
        curs = conn.cursor()
    except:
        print('Database cannot be reached')

    def __init__(self):
        pass

    def add_user(self, uid, name, is_bot):
        if not self.is_user(uid):
            self.curs.execute("INSERT INTO users VALUES (?, ?, ?)", (uid, name, is_bot))
            self.conn.commit()
    
    def is_user(self, uid):
        self.curs.execute("SELECT name, is_bot FROM users WHERE id=?", (uid, ))
        usr = self.curs.fetchone()
        return usr

    def all_users(self):
        self.curs.execute("SELECT id FROM users")
        usrs = self.curs.fetchall()
        return usrs
    
    def remove_user():
        pass

    def __exit__(self):
        self.conn.close()