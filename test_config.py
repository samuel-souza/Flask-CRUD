import os.path

basedir = os.path.abspath(os.path.dirname(__file__))  
DATABASE = os.path.join(basedir, 'storage.db')  # O arquivo app.db será criado na raiz do projeto  
# SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
SQLALCHEMY_DATABASE_URI = 'sqlite:///{DATABASE}'
TESTING = True
WTF_CSRF_ENABLED = False
LOGIN_DISABLED = True
SECRET_KEY = 'senha-bem-segura-2'