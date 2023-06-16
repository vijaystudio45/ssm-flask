from db import db
from app import app

from models.transaction import TransactionModel

def create_app():
    db.init_app(app)
    return app
