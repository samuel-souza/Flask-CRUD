from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, UserMixin
from flask_bcrypt import Bcrypt
from sqlalchemy import create_engine

# Instanciando app
app = Flask(__name__) 
bcrypt = Bcrypt(app)  

# Configurando database
if app.config['TESTING']:
    app.config.from_object('test_config')
else:
    app.config.from_object('config')
# app.config.from_object('config') # Adicionando configurações a partir de um arquivo

engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])  
db = SQLAlchemy(app)

# Inicializando SQLite
migrate = Migrate(app, db)
lm = LoginManager()
lm.init_app(app)

# Importando módulos 
from app.models import tables, forms
from app.controllers import default