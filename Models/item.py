from Database.db import db

class Item(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key= True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))

    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))

    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price
        }

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self.id

    @classmethod
    def get_item(cls, name):
        return cls.query.filter_by(name=name).first()
        
    
    @classmethod
    def get_items(cls):
        return cls.query.all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self.id