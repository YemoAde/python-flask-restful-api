from config import config_by_name
from flask import Blueprint, Flask, jsonify, make_response
from flask_jwt_extended import JWTManager
from flask_restplus import Api
from Util.response import ResponseHandler as Response
import os


from Models.item import Item
from Models.store import Store
from Models.user import User

from Resources.items import item_ns
from Resources.store import store_ns
from Resources.user import auth_ns

environment = os.getenv('ENVIRONMENT')

app = Flask(__name__)
app.config.from_object(config_by_name[environment])
jwt = JWTManager(app)
api = Api(app)

jwt._set_error_handler_callbacks(api)
api.add_namespace(auth_ns, path='/auth')
api.add_namespace(item_ns, path="/item")
api.add_namespace(store_ns, path="/store")

## Pre Run



##Handling errors
@app.errorhandler(401)
def unauthorized(error):
    return make_response(jsonify( { 'error': 'Unauthorized' } ), 401)

@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify( { 'error': 'Bad request' } ), 400)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'error': 'Resource Not found' } ), 404)

@app.errorhandler(405)
def not_allowed(error):
    return make_response(jsonify( { 'error': 'Method Not Allowed' } ), 405)

@app.errorhandler(500)
def internal_error(error):
    return make_response(jsonify( { 'error': 'Internal Server Error' } ), 500)

# @jwt.expired_token_loader
# def expired_token_callback():
#     return Response.error('The token has expired', Response.UNAUTHORIZED)

# @jwt.invalid_token_loader
# def invalid_token_callback():
#     return Response.error('The token is invalid', Response.UNAUTHORIZED)




# blueprint = Blueprint('api', __name__)
# api = Api(blueprint)
# app.register_blueprint(api, url_prefix='/api')

port = int(os.environ.get('PORT', 5000))
if __name__ == "__main__":
    from Database.db import db
    @app.before_first_request
    def create_tables():
        db.create_all()
    db.init_app(app)
    app.run()