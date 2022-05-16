# import sys
# sys.path.append("/Users/christinewang/rest_api_course")

from db import db


class StoreModel(db.Model):
    __tablename__ = 'stores'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80))

    items = db.relationship('ItemModel', lazy='dynamic')
# So, if we have many stores and we have many items, whenever we create a store model,
# we're going to go and create an object for each item
# in a database that matches that store id.
# If we have many items, it could be expensive
# lazy='dynamic' tells sqlalchemy do not go into the items table and create an object for each item yet.



    def __init__(self, name):
        self.name = name

    def json(self):
        return{'name':self.name, 'items': [item.json() for item in self.items.all()]}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name = name).first()
        # query is a function in sqlalchemy

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

