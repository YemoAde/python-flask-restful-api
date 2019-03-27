import os
import uuid
from dotenv import load_dotenv
load_dotenv()


class Configuration:
    def __init__(self):
        self.jwt_key = os.getenv('JWT_SECRET', 'helloworld')

    @staticmethod
    def getJwtKey():
        return os.getenv('JWT_SECRET', )
