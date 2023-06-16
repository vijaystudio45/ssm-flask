from db import db
from .wallet import WalletModel
from datetime import datetime
from .transaction import TransactionModel


class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))
    email = db.Column(db.String(60))
    date_created = db.Column(db.DateTime)
    last_login = db.Column(db.DateTime)
    mail_activation_code = db.Column(db.String(40))
    activated = db.Column(db.Boolean)

    wallets = db.relationship("WalletModel", backref="users", lazy="dynamic")
    transactions = db.relationship("TransactionModel", backref="users", lazy="dynamic")

    def __init__(self, email, username, password, mail_activation_code):
        self.email = email
        self.username = username
        self.password = password
        self.date_created = datetime.utcnow()
        self.last_login = datetime.utcnow()
        self.mail_activation_code = mail_activation_code
        self.activated = False

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    @classmethod
    def update_login_time(cls, _id):
        user = cls.query.filter_by(id=_id).first()
        user.last_login = datetime.utcnow()
        db.session.add(user)
        db.session.commit()

    @classmethod
    def activate_user(cls, code):
        user = cls.query.filter_by(mail_activation_code=code).first()
        if user:
            user.activated = True
            db.session.add(user)
            db.session.commit()
            return 1
        return 0

    @classmethod
    def create_wallet_if_not_exists(cls, id):
        wallet = WalletModel.find_by_id(id)
        if wallet == None:
            wallet = WalletModel("active", id, "paypal/coinbase")
            wallet.funds = 0
            wallet.save_to_db()

        return 1
