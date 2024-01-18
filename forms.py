from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, PasswordField
from wtforms.validators import Length

class UserForm(FlaskForm):

    username = StringField("Username")

    password = PasswordField("Password")

    email = StringField("Email", validators=[Length(max=50)])

    first_name = StringField("First Name", validators=[Length(max=30)])

    last_name = StringField("Last Name", validators=[Length(max=30)])

class LoginForm(FlaskForm):

    username = StringField("Username")

    password = PasswordField("Password")

class FeedbackForm(FlaskForm):

    title = StringField("Title", validators=[Length(max=100)])

    content = StringField("Title")

    username = StringField("username")