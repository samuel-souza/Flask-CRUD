from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Email, NumberRange, Optional, Length, EqualTo

# Classe para o formulário de login
class LoginForm(Form):
    # Campo para o nome de usuário, obrigatório e com comprimento entre 5 e 12 caracteres
    username = StringField("username", validators=[DataRequired(), Length(5, 12)])
    # Campo para a senha, obrigatório e com comprimento entre 5 e 15 caracteres
    password = PasswordField("password", validators=[DataRequired(), Length(5, 15)])
    # Campo opcional para lembrar o login do usuário
    remember_me = BooleanField("remember_me")

# Classe para o formulário de registro de novos usuários
class RegisterForm(Form):
    # Campo para o email, obrigatório e validado como um formato de email correto
    email = StringField("email", validators=[DataRequired(), Email()])
    # Campo para o nome, obrigatório e com comprimento entre 5 e 20 caracteres
    name = StringField("name", validators=[DataRequired(), Length(5, 20)])
    # Campo para a idade, obrigatório e validado para estar entre 18 e 100 anos
    age = IntegerField("age", validators=[DataRequired(), NumberRange(18, 100, message="Você deve ter entre 18 e 100 anos de idade.")])
    # Campo para o nome de usuário, obrigatório e com comprimento entre 5 e 12 caracteres
    username = StringField("username", validators=[DataRequired(), Length(5, 12)])
    # Campo para a senha, obrigatório e com comprimento entre 5 e 15 caracteres
    password = PasswordField("password", validators=[DataRequired(), Length(5, 15)])

# Classe para o formulário de atualização dos dados do usuário
class UpdateForm(Form):
    # Campo para o email, opcional e validado como um formato de email correto
    email = StringField("email", validators=[Email(), Optional()])
    # Campo para o nome, opcional e com comprimento entre 5 e 20 caracteres
    name = StringField("name", validators=[Length(5, 20), Optional()])
    # Campo para a idade, opcional e validado para estar entre 18 e 100 anos
    age = IntegerField("age", validators=[NumberRange(18, 100, message="Você deve ter entre 18 e 100 anos de idade."), Optional()])
    # Campo para o nome de usuário, opcional e com comprimento entre 5 e 12 caracteres
    username = StringField("username", validators=[Length(5, 12), Optional()])
    # Campo para a senha, opcional e com comprimento entre 5 e 15 caracteres
    password = PasswordField("password", validators=[Length(5, 15), Optional()])
    # Campo para repetir a senha, necessário ser igual ao campo 'password'
    repeat_password = PasswordField("repeat password", validators=[EqualTo('password', message="As senhas devem coincidir.")])


