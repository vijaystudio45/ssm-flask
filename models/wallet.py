from db import db


class WalletModel(db.Model):
    __tablename__ = "wallets"

    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(40))  # unactivated, activated, revoked or banned
    type = db.Column(db.String(20))
    funds = db.Column(db.Float)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    def __init__(self, status, user_id, type):
        self.status = status
        self.type = type
        self.funds = 0.0
        self.user_id = user_id

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    # @classmethod
    # def find_by_username(cls, username):
    #     return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_user(cls, _id):
        return cls.query.filter_by(user_id=_id).first()

    @classmethod
    def topup(cls, _id, amount):
        wallet = cls.find_by_user(_id)
        if wallet.funds == None:
            wallet.funds = 0
        wallet.funds += amount
        wallet.save_to_db()
        return True

    @classmethod
    def charge(cls, _id, amount):
        wallet = cls.find_by_id(_id)
        if wallet is None:
            return (False, "Fatal error: No wallet")
        if wallet.funds - amount >= 0:
            wallet.funds -= amount
            wallet.save_to_db()
            return (True, "Sucessfull")
        return (False, "Insufficient Funds")

    def check_bal(self):
        return self.funds