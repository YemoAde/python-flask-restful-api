from auth import Auth
from Database.db import Connection
from flask import Flask, request
from flask_restplus import Api, Namespace, Resource, fields, reqparse
from Models.user import User
from Util.response import ResponseHandler

auth_ns = Namespace('auth', description='Auth related operations')
user = auth_ns.model('auth', {
    'username': fields.String(required=True, description='user email address', help="username is required"),
    'password': fields.String(required=True, description='user password'),
})

@auth_ns.route('/sign-up')
class Register(Resource):
    parser = reqparse.RequestParser(bundle_errors=True)
    parser.add_argument('username', type=str, required=True)
    parser.add_argument('password', type=str, required=True)

    @auth_ns.response(201, 'User successfully created.')
    @auth_ns.doc('create a new user')
    @auth_ns.expect(user, validate=True)
    def post(self):
        data = Register.parser.parse_args()
        connection = Connection()
        user = User.find_by_username(data.username)
        if user: 
            return ResponseHandler.error('user exists', 400)
        query = "INSERT INTO users (username, password) values(?, ?)"
        connection.insert(query, (data.username, data.password))
        connection.close
        return {'message': 'User added'}, 200

@auth_ns.route('/login')
class Login(Resource):
    parser = reqparse.RequestParser(bundle_errors=True)
    parser.add_argument('username', type=str, required=True)
    parser.add_argument('password', type=str, required=True)

    @auth_ns.response(200, 'User successfully created.')
    @auth_ns.doc('create a new user')
    @auth_ns.expect(user, validate=True)
    def post(self):
        data = Login.parser.parse_args()
        return Auth.authenticate(data.username, data.password)
