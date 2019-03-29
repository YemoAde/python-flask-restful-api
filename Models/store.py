from Database.db import db


class Store(db.Model):
    __tablename__ = 'stores'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    items = db.relationship('Item', lazy='dynamic')

    def __init__(self, name):
        self.name = name

    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'items': [item.json() for item in self.items.all()]
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
    

