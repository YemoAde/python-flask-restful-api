
class ResponseHandler:
    OK = 200
    NOT_FOUND = 404
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    CREATED = 401

    def __init__(self, message, data = None):
        pass
        
    @classmethod
    def success(cls, message, code, data=None):
        if data:
            return {
                'status' : 'success',
                'message': message,
                'data': data
            }, code
        return {
            'status' : 'success',
            'message': message,
        }, code

    @classmethod
    def error(cls, message, code):
        return {
            'status' : 'error',
            'message': message,
        }, code