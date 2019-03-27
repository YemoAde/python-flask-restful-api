from Database.db import Connection

class User:
    def __init__(self, _id, username, password, **args):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        query = "SELECT * FROM users WHERE username = ?"
        connection = Connection()
        result = connection.select(query, (username,))
        if result:
            user = cls(*result)
        else:
            user = None
        
        connection.close()
        return user

    @classmethod
    def find_by_id(cls, _id):
        query = "SELECT * FROM users WHERE id = ?"
        connection = Connection()
        result = connection.select(query, (_id,))
        if result:
            user = cls(*result)
        else:
            user = None

        connection.close()
        return user
    
    @classmethod
    def serialize(cls, user):
        return {
            'id': user.id,
            'username': user.username
        }

