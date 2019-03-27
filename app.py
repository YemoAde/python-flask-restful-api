from flask import Flask, Blueprint, make_response, jsonify
from flask_restplus import Api
from flask_jwt_extended import JWTManager

from config import Configuration

from Resources.user import auth_ns
from Resources.items import item_ns

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = Configuration.getJwtKey()

@app.errorhandler(401)
def not_found(error):
    return make_response(jsonify( { 'error': 'Unauthorized' } ), 401)

@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify( { 'error': 'Bad request' } ), 400)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'error': 'Not found' } ), 404)

@app.errorhandler(405)
def not_found(error):
    return make_response(jsonify( { 'error': 'Method Not Allowed' } ), 405)

@app.errorhandler(500)
def not_found(error):
    return make_response(jsonify( { 'error': 'Internal Server Error' } ), 500)

jwt = JWTManager(app)
api = Api(app)
jwt._set_error_handler_callbacks(api)
api.add_namespace(auth_ns, path='/auth')
api.add_namespace(item_ns, path="/item")


# blueprint = Blueprint('api', __name__)
# api = Api(blueprint)
# app.register_blueprint(api, url_prefix='/api')


if __name__ == "__main__":
    app.run(port=5000, debug=True)