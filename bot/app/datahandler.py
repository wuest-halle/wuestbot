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
"""

import sqlite3

class Datahandler:

    try:
        conn = sqlite3.connect('tryout.db')
        curs = conn.cursor()
    except:
        print('Database cannot be reached')

    def __init__(self):
        pass

    def add_user(self, uid, name, is_bot):
        if not self.is_user(uid):
            self.curs.execute(f'''INSERT INTO users VALUES ({uid}, {name}, {is_bot})''')
            self.conn.commit()
    
    def is_user(self, uid):
        self.curs.execute(f'''SELECT name, is_bot FROM users WHERE id={uid}''')
        usr = self.curs.fetchall()
        return usr

    def all_users(self):
        pass
    
    def remove_user():
        pass

    def __exit__(self):
        self.conn.close()