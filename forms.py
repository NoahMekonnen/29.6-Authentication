from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, PasswordField
from wtforms.validators import NumberRange

class UserForm(FlaskForm):

    username = StringField("Username")

    password = PasswordField("Password")

    email = StringField("Email", validators=[NumberRange(max=50)])

    first_name = StringField("First Name", validators=[NumberRange(max=30)])

    last_name = StringField("Last Name", validators=[NumberRange(max=30)])

class LoginForm(FlaskForm):

    username = StringField("Username")

    password = PasswordField("Password")

class FeedbackForm(FlaskForm):

    title = StringField("Title", validators=[NumberRange(max=100)])

    content = StringField("Title")

    username = StringField("username")