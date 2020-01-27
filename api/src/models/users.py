from db import db

from log import Logger

LOGGER = Logger(__name__)

class User(db.Model):
    """Class representing a single instance of an user record

    Arguments:
        * id (int) = the user's unique ID, equivalent to Telegram's ID
        * name (str) = user's first name
        * is_bot (bool) = whether the user is a chatbot or not
    
    To Do:
        * introduce handling/logging to get() if user id is not found
        * write checks if actual temporary testing db is being used
        * change update(), so that an User object is given as Argument
        * introduce error handling to update(), if record to be updated is not found
    """

    __tablename__ = 'Users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), index=True, nullable=False)
    is_bot = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return f'<User {self.name}, ID {self.id}>'

    def save(self):
        """Saves a single user to the database"""

        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            LOGGER.error(msg=f"""Encountered following exception while trying to save 
                user {self.id, self.name} to the DB {e}""")
            return
            
    @classmethod
    def get(cls,id):
        """Classmethod, retrieves a single user from the DB

        Arguments:
            * id: id of the user in question

        Returns:
            single user object
        """

        return cls.query.get(id)
    
    @classmethod
    def delete(cls, id): 
        """Classmethod, deletes single user record from the DB

        Arguments:
            * id: id of the user in question

        Returns:
            nothing
        """
        
        with cls.get(id) as user:
            db.session.delete(user)
            db.session.commit()

    @staticmethod
    def update(id, name, is_bot):
        """Classmethod, updates attributes of a single user's record

        Arguments:
            * id: id of the user which should be updated
            * name: new name of the user
            * is_bot: new status of the user as bot

        Returns:
            nothing
        """

        User.query.filter_by(id=id).update({'id': id, 'name': name, 'is_bot': is_bot})

    @staticmethod
    def get_all():
        """Static method, retrieves all users from the DB

        Arguments:
            none
        
        Returns:
            List of User objects
        """

        return User.query.all()