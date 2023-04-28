from flask_wtf import FlaskForm
from wtforms import StringField, PassWordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, EqualTo

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PassWordField('Password', validators=[DataRequired()])
    password2 = PassWordField('Retype Password', validators=[DataRequired(), EqualTo('password')])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')