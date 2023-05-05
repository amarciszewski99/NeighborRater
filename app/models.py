from datetime import datetime
from hashlib import md5
from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True)
    first_name = db.Column(db.String(32))
    last_name = db.Column(db.String(32))
    email = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    u2a_list = db.relationship('UserToAddress', backref='user', lazy='dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<User {} {}>'.format(self.first_name, self.last_name)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
    

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

