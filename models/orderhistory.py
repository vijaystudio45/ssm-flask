from db import db


class OrderHistory(db.Model):
    __tablename__ = "orderhistory"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    task_id = db.Column(db.Integer)
    name = db.Column(db.String(100))
    link = db.Column(db.String(200))
    base_rate = db.Column(db.Float)
    rate = db.Column(db.Float)
    issued_at = db.Column(db.DateTime)
    dripfeed = db.Column(db.Boolean)
    quantity = db.Column(db.Integer)
    task_status = db.Column(db.String(100))

    def __init__(self, user_id, task_id, name, link, base_rate, rate, issued_at, dripfeed, quantity, task_status):
        self.user_id = user_id
        self.name = name
        self.task_id = task_id
        self.link = link
        self.base_rate = base_rate
        self.rate = rate
        self.issued_at = issued_at
        self.dripfeed = dripfeed
        self.quantity = quantity
        self.task_status = task_status

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_order_id(cls, _id):
        return cls.query.filter_by(task_id=_id).first()

    @classmethod
    def find_by_user_id(cls, _id):
        return cls.query.filter_by(user_id=_id).all()

    @classmethod
    def user_spent(cls, _id):
        orders = cls.find_by_user_id(_id)
        sum = 0
        for order in orders:
            sum += float(order.quantity) * float(order.rate) / 1000

        return sum

    @classmethod
    def find_all(cls):
        return cls.query.all()

    @classmethod
    def execute_query(cls, query):
        return db.engine.execute(query)
