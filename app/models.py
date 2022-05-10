from datetime import datetime
from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    email = db.Column(db.String(128), unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.email)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Profile(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    age = db.Column(db.Integer)
    gender = db.Column(db.String(32))
    birthday = db.Column(db.Date, default=datetime.utcnow)
    average_rating = db.Column(db.Float(5, True, 1), index=True)  # POTENTIAL ISSUES WITH PARAMETERS, TEST THIS
    is_claimed = db.Column(db.Boolean)
    job_title = db.Column(db.String(128))
    political_affiliation = db.Column(db.String(32))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    p2a_list = db.relationship("ProfileToAddress", backref="profile", lazy="dynamic")

    def __repr__(self):
        return '<Name {}>'.format(self.name)


class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    housing_type = db.Column(db.String(32))
    street_address = db.Column(db.String(128), unique=True)
    township = db.Column(db.String(64))
    state = db.Column(db.String(32))
    zip_code = db.Column(db.String(5))
    p2a_list = db.relationship("ProfileToAddress", backref="address", lazy="dynamic")

    def __repr__(self):
        return '<Address {}>'.format(self.street_address)


class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Float(5, True, 1))
    description = db.Column(db.String(256))

    def __repr__(self):
        return '<Rating {}>'.format(self.rating)


class ProfileToAddress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(db.Integer, db.ForeignKey('profile.id'))
    address_id = db.Column(db.Integer, db.ForeignKey('address.id'))
    rating_id = db.Column(db.Integer, db.ForeignKey('rating.id'))
    is_current_address = db.Column(db.Boolean)
