import os.path

basedir = os.path.abspath(os.path.dirname(__file__))  
DATABASE = os.path.join(basedir, 'storage.db')  # O arquivo app.db será criado na raiz do projeto  
SQLALCHEMY_DATABASE_URI = f'sqlite:///{DATABASE}'

# import os  

# basedir = os.path.abspath(os.path.dirname(__file__))  
# DATABASE = os.path.join(basedir, 'data', 'storage.db')  # Banco de dados é armazenado na pasta 'data'  

# SQLALCHEMY_DATABASE_URI = f'sqlite:///{DATABASE}'

# SQLALCHEMY_DATABASE_URI = 'sqlite:///storage.db' # Base de dados SQLite
SQLALCHEMY_TRACK_MODIFICATIONS = True # Evitar warnings
SECRET_KEY = 'senha-bem-segura'