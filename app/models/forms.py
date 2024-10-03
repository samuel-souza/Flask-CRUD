from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Email, NumberRange, Optional, Length

class LoginForm(Form):
    email = StringField("email", validators=[Optional()])
    username = StringField("username", validators = [DataRequired()])
    password = PasswordField("password", validators = [DataRequired()])
    remember_me = BooleanField("remember_me")

class RegisterForm(Form):
    email = StringField("email", validators = [DataRequired(), Email()])
    name = StringField("name", validators=[DataRequired()])
    age = IntegerField("age", validators=[DataRequired(), NumberRange(18, 100, message = "Você deve ter entre 18 e 100 anos de idade.")])
    # gender = StringField("gender", validators=[Optional()])
    username = StringField("username", validators=[DataRequired(), Length(5,12)])
    password = PasswordField("password", validators=[DataRequired(), Length(5,15)])


