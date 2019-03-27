from werkzeug.security import safe_str_cmp, check_password_hash
from Models.user import User
from flask_jwt_extended import create_access_token, get_jwt_identity
import json

class Auth:
    def __init__(self):
        pass
    
    @staticmethod
    def authenticate(username, password):
        user = User.find_by_username(username)
        if user and check_password_hash(user.password, password):
            return Auth.authenticatebyUser(user)
        return {'message': 'invalid credentials '}, 401

    @staticmethod
    def authenticatebyUser(user):
        if isinstance(user, User):
            token = create_access_token(identity=user.id)
            return {'token': token}, 200
        return None

    @staticmethod
    def getUser():
        userid = get_jwt_identity()
        return User.find_by_id(userid)
    
    @staticmethod
    def identity(payload):
        userid = payload['identity']
        return User.find_by_id(userid)