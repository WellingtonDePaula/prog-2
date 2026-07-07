from wtforms import IntegerField, StringField, EmailField, PasswordField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, EqualTo, InputRequired

class UserRegister(FlaskForm):
    id = IntegerField("Id", validators=[InputRequired(message='User must have a ID.')])
    username = StringField("Username", validators=[DataRequired(message='User must have a username.')])
    email = EmailField("Email", validators=[DataRequired(message='User must have a email.')])
    password = PasswordField("Password", validators=[DataRequired(message='User must have a password.')])
    confirm_password = PasswordField("Confirm Password", validators=[EqualTo('password', message='Passwords must be the same.')])

class UserLogin(FlaskForm):
    id = IntegerField("Id", validators=[InputRequired(message='User must have a ID.')])
    username = StringField("Username", validators=[DataRequired(message='User must have a username.')])
    email = EmailField("Email", validators=[DataRequired(message='User must have a email.')])
    password = PasswordField("Password", validators=[DataRequired(message='User must have a password.')])