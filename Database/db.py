import sqlite3
import os
from Util.response import ResponseHandler

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Connection:
    def __init__(self):
        self.connection = sqlite3.connect(os.getenv('DB_URL'))
        self.cursor = self.connection.cursor()
    
    # values is a tuple of values
    def insert(self, query, values):
        try:
            if (self.cursor.execute(query, values)):
                return True
            return None
        except:
            return ResponseHandler.error('Something went wrong', 500)
        
    # id is a tuple of values
    def select(self, query, params=None):
        try:
            if params:
                result = self.cursor.execute(query, params)
                return result.fetchone()
            else:
                result = self.cursor.execute(query)
                return result.fetchall()

            return None
        except:
            return ResponseHandler.error('Something went wrong', 500)

    
    def delete(self, query, params):
        try:
            if self.cursor.execute(query, params).rowcount > 0:
                return True
            return None
        except:
            return ResponseHandler.error('Something went wrong', 500)

    def close(self):
        self.connection.commit()
        self.connection.close()
    
