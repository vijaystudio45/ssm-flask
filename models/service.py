from db import db


class ServiceModel(db.Model):
    __tablename__ = "services"
    
    id = db.Column(db.Integer, primary_key=True)
    enabled = db.Column(db.Boolean)
    name = db.Column(db.String(100))  # unactivated, activated, revoked or banned
    type = db.Column(db.String(20))  # default
    base_rate = db.Column(db.Float)
    rate = db.Column(db.Float)
    min = db.Column(db.Integer)
    max = db.Column(db.Integer)
    dripfeed = db.Column(db.Boolean)
    refill = db.Column(db.Boolean)
    category = db.Column(db.String(50))

    def __init__(self, id, name, type, rate, min, max, dripfeed, refill, category):
        self.id = id
        self.enabled = True
        self.name = name
        self.type = type
        self.rate = rate
        self.base_rate = rate
        self.min = min
        self.max = max
        self.dripfeed = dripfeed
        self.refill = refill
        self.category = category

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    # @classmethod
    # def execute_query(cls, query):
    #     return db.engine.execute(query)

    @classmethod
    def enable_service(cls, _id):
        print(f"enabling {_id}")
        service = cls.query.filter_by(id=_id).first()
        service.enabled = True
        db.session.add(service)
        db.session.commit()
    
    @classmethod
    def disable_service(cls, _id):
        print(f"disabling {_id}")
        service = cls.query.filter_by(id=_id).first()
        service.enabled = False
        db.session.add(service)
        db.session.commit()
        

    @classmethod
    def update_price(cls, _id, new_rate):
        service = cls.query.filter_by(id=_id).first()
        service.rate = new_rate
        db.session.add(service)
        db.session.commit()

    @classmethod
    def update_name(cls, _id, new_name):
        service = cls.query.filter_by(id=_id).first()
        service.name = new_name
        db.session.add(service)
        db.session.commit()
