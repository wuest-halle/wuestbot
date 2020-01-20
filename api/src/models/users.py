from db import db

class Users(db.Model):

    __tablename__ = 'Users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(120), nullable=false)
    is_bot = db.Column(db.Bool, nullable=false)

    def save(self):

        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            return
            
    @classmethod
    def retrieve_single_user(cls,id):
        
        return cls.query.get(id)
    
    @classmethod
    def delete_user(cls, id): 
        
        with self.retrieve_single_user(id) as user:
            db.session.delete(user)
            db.session.commit()

    @classmethod
    def update_user(cls, id, name, is_bot):

        with self.retrieve_single_user(id) as former_user:
            self.delete_user(former_user.id)
            self.save(cls)


    @staticmethod
    def retrieve_all_users():

        return Users.query.get().all()
