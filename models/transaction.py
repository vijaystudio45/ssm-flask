import datetime
from db import db


class TransactionModel(db.Model):
    __tablename__ = "transactions"

    id = db.Column(db.Integer, primary_key=True)
    transaction_id = db.Column(db.String(50))
    type = db.Column(db.String(20))  # paypal or coinbase
    amount = db.Column(db.Integer)
    date_issued = db.Column(db.DateTime)
    date_closed = db.Column(db.DateTime)
    status = db.Column(db.String(50))  # paid, pending, canceled, expired.
    transaction_owner_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    def __init__(self, transaction_id, transaction_owner_id, type, amount):
        self.transaction_id = transaction_id
        self.transaction_owner_id = transaction_owner_id
        self.type = type
        self.amount = amount
        self.date_issued = datetime.datetime.utcnow()
        self.status = "pending"

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    @classmethod
    def update_status(cls, transaction_id, new_status):
        transaction = cls.query.filter_by(transaction_id=transaction_id).first()
        transaction.date_closed = datetime.datetime.utcnow()
        transaction.status = new_status
        db.session.add(transaction)
        db.session.commit()

    @classmethod
    def get_coinbase_pending(cls):
        t = cls.query.filter_by(status="pending", type="coinbase").all()
 
 