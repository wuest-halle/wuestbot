from db import db

class Users(db.Model):
    """Class representing a single instance of an user record

    Arguments:
        id (int) = the user's unique ID, equivalent to Telegram's ID
        first_name (str) = user's first name
        is_bot (bool) = whether the user is a chatbot or not
    """

    __tablename__ = 'Users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(120), nullable=False)
    is_bot = db.Column(db.Boolean, nullable=False)

    def save(self):
    """Saves a single user to the database"""

        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            return
            
    @classmethod
    def retrieve_single_user(cls,id):
    """Classmethod, retrieves a single user from the DB

    Arguments:
        id: id of the user in question

    Returns:
        single user object
    """

        return cls.query.get(id)
    
    @classmethod
    def delete_user(cls, id): 
    """Classmethod, deletes single user record from the DB

    Arguments:
        id: id of the user in question

    Returns:
        nothing
    """
        
        with self.retrieve_single_user(id) as user:
            db.session.delete(user)
            db.session.commit()

    @classmethod
    def update_user(cls, id, first_name, is_bot):
    """Classmethod, updates attributes of a single user's record

    Works with a dirty hack right now: It deletes the record of the user with 
    the provided ID and then saves a new record with provided parameters

    Arguments:
        * id: id of the user which should be updated
        * first_name: new name of the user
        * is_bot: new status of the user as bot
    
    Returns:
        nothing
    """

        with self.retrieve_single_user(id) as former_user:
            self.delete_user(former_user.id)
            self.save(cls)


    @staticmethod
    def retrieve_all_users():
        """Static method, retrieves all users from the DB

        Arguments:
            none
        
        Returns:
            List of User objects
        """

        return Users.query.get().all()