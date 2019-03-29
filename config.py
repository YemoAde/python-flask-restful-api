import os
import datetime
from dotenv import load_dotenv
load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))

class Configuration:
    SECRET_KEY = os.getenv('SECRET_KEY', 'my_secret_key')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'my_jwt_secret_key')
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(1440000)

class DevConfiguration(Configuration):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///' + os.path.join(basedir, 'data.db'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class TestingConfiguration(Configuration):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data_test.db')
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfiguration(Configuration):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///' + os.path.join(basedir, 'data.db'))

config_by_name = dict(
    dev=DevConfiguration,
    test=TestingConfiguration,
    prod=ProductionConfiguration
)

key = Configuration.SECRET_KEY
    
# class Configuration:
#     def __init__(self):
#         self.jwt_key = os.getenv('JWT_SECRET', 'helloworld')

#     @staticmethod
#     def getJwtKey():
#         return os.getenv('JWT_SECRET', 'helloworld')
    
#     @staticmethod
#     def getDatabaseURI():
#         return os.getenv('DATABASE_URI', 'sqlite:///data.db')
