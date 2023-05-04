from datetime import datetime
from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(32))
    last_name = db.Column(db.String(32))
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    u2a_list = db.relationship('UserToAddress', backref='user', lazy='dynamic')

    def __repr__(self):
        return '<User {} {}>'.format(self.first_name, self.last_name)
    

class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    street_address = db.Column(db.String(32), unique=True)
    city = db.Column(db.String(32))
    state = db.Column(db.String(2))
    zip_code = db.Column(db.String(5))
    u2a_list = db.relationship('UserToAddress', backref='address', lazy='dynamic')

    def __repr__(self):
        return 'Address {}, {}, {}, {}'.format(self.street_address, self.city, self.state, self.zip_code)


class UserToAddress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    address_id = db.Column(db.Integer, db.ForeignKey('address.id'))


class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rating_value = db.Column(db.Numeric(precision=3, scale=2))
    description = db.Column(db.String(256))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    u2a_id = db.Column(db.Integer, db.ForeignKey('user_to_address.id'))

    def __repr__(self):
        return 'Rating {} : {}'.format(self.rating_value, self.description)

