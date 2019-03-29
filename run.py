from app import app
from Database.db import db

db.init_app(app)

## Pre Run
@app.before_first_request
def create_tables():
    db.create_all()
