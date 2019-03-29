from flask import make_response, jsonify

class ErrorHandler:
    def __init__(self, app):
        pass

    @staticmethod
    def not_found_400(error):
        return make_response(jsonify( { 'error': 'Bad request' } ), 400)

    @staticmethod
    def not_found_404(error):
        return make_response(jsonify( { 'error': 'Not found' } ), 404)

    @staticmethod
    def not_found_405(error):
        return make_response(jsonify( { 'error': 'Method Not Allowed' } ), 405)
        
    @staticmethod
    def internal_error_500(error):
        return make_response(jsonify( { 'error': 'Internal Server Error' } ), 500)
