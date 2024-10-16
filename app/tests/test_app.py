import pytest  
from app import app, db, migrate
from app.models.tables import User  
from app.src.test_user_generate import generate_random_user
from flask_bcrypt import Bcrypt  
from sqlalchemy import  create_engine


bcrypt = Bcrypt(app)
random_existing_user = generate_random_user()
random_new_user = generate_random_user()
random_create_user = generate_random_user()
random_authenticated_user = generate_random_user()

def test_app_configuration_testing_mode():  
    app.config.from_object('test_config')  # Simula a configuração de teste  
    assert app.config['SECRET_KEY'] == 'senha-bem-segura-2'   
    assert app.config['WTF_CSRF_ENABLED'] == False
    assert app.config['LOGIN_DISABLED'] == True

def test_app_configuration_production_mode():  
    # app.config['TESTING'] = False  
    app.config.from_object('config')  # Simula a configuração de produção  
    assert app.config['SECRET_KEY'] == 'senha-bem-segura'
    assert app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] == True

def test_create_engine():  
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use um URI de teste  
    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])  
    assert engine is not None  # Verifica se o engine foi criado

def test_migrate_initialization():  
    assert migrate is not None  # Verifica se o migrate foi inicializado

@pytest.fixture(scope='session')  
def test_client():  
    app.config.from_object('test_config')  # Carrega a configuração de teste

    with app.app_context():  
        db.create_all()
        db.session.begin()
        yield app.test_client()  
        db.session.rollback()
        db.session.close()


@pytest.fixture  
def new_user():  
    """Fixture para criar e retornar um novo usuário novamente, garantindo que não exista o mesmo."""  
    User.query.filter_by(username=random_new_user['username']).delete()  # Remove se existir  
    User.query.filter_by(email=random_new_user['email']).delete()  # Remove se existir  
    db.session.commit()  
    
    user = User(  
        username=random_new_user['username'],  
        name=random_new_user['name'],  
        age=random_new_user['age'],  
        email=random_new_user['email'],  
        password=bcrypt.generate_password_hash(random_new_user['password']).decode('utf-8')  
    )  
    db.session.add(user)  
    db.session.commit()  
    return user  

# @pytest.fixture  
# def existing_user():  
#     """Fixture para criar e retornar um usuário existente."""  
#     user = User(  
#         username=random_existing_user['username'], 
#         name=random_existing_user['name'],  
#         age=random_existing_user['age'],   
#         email=random_existing_user['email'],  
#         password=bcrypt.generate_password_hash(random_existing_user['repeat_password']).decode('utf-8')  
#     )  
#     db.session.add(user)  
#     db.session.commit()  
#     return user  

def test_get_data_authenticated(test_client):
    # Simular um usuário
    user = User(  
        username = random_authenticated_user['username'],  
        password = random_authenticated_user['password'],  
        name = random_authenticated_user['name'],  
        age = random_authenticated_user['age'],  
        email = random_authenticated_user['email']  
    )  

    db.session.add(user)
    db.session.commit()

    # Fazer login do usuário
    with test_client.session_transaction() as sess:
        sess['_user_id'] = str(user.id)  # Simular o usuário autenticado

    # Fazer requisição GET
    response = test_client.get("/data/get")
    
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)
    assert len(response.get_json()) > 0  # Verifica se o conteúdo está presente

def test_check_password(new_user):  
    """Teste para verificar a funcionalidade de checagem de senha"""  
    saved_user = User.query.filter_by(username=random_new_user['username']).first()  
    assert bcrypt.check_password_hash(saved_user.password, random_new_user['password'])  
    assert not bcrypt.check_password_hash(saved_user.password, 'wrongpassword')  

def test_register_new_user(test_client):  
    """Teste para verificar o registro de um novo usuário."""  
    response = test_client.post('/register', data={  
        'username': random_create_user['username'],  
        'password': random_create_user['password'],  
        'name': random_create_user['name'],  
        'age': random_create_user['age'],  
        'email': random_create_user['email']  
    })  
    assert response.status_code == 302  
    assert response.location.endswith('/login')
    assert User.query.filter_by(username=random_create_user['username']).first() is not None  

def test_login_sucess(test_client, new_user):  
    """Teste para verificar o login de um usuário existente."""  
    response = test_client.post('/login', data={  
        'username': random_new_user['username'],  
        'password': random_new_user['password']  
    })  

    assert response.status_code == 302  


def test_login_failure(test_client, new_user):  
    """Teste para verificar o login de um usuário existente."""  
    response = test_client.post('/login', data={  
        'username': '',  
        'password': ''  
    })  
    assert response.status_code == 302
    assert response.location.endswith('/login')  

def test_login_invalid(test_client):  
    """Teste para verificar o login com credenciais inválidas."""  
    response = test_client.post('/login', data={  
        'username': 'invaliduser',  
        'password': 'wrongpassword'  
    })  
    assert response.status_code == 400  
    assert b"Invalid Login." in response.data 

def test_logout(test_client):  
    """Teste para verificar se o logout funciona corretamente."""  
    response = test_client.post('/login', data={  
        'username': random_new_user['username'],  
        'password': random_new_user['password']  
    })  

    assert response.status_code == 302

    response = test_client.get('/logout')  
    assert response.status_code == 302  
    assert response.location.endswith('/login')

def test_update_user_success(test_client):  
    """Teste para verificar a atualização dos dados do usuário."""  
    # Faça o login do usuário recém-criado antes de tentar acessar o endpoint de atualização.  
    test_client.post('/login', data={  
        'username': random_new_user['username'],  
        'password': random_new_user['password']  
    })  

    # O e-mail não pode ser o mesmo que o existente.  
    new_email = 'updated@example.com'  
    if User.query.filter_by(email=new_email).first():  
        User.query.filter_by(email=new_email).delete()  # Remove se existir  
        db.session.commit()  

    response = test_client.post('/update', data={  
        'email': new_email,  
        'name': '',  
        'age': None,  
        'username': '',   
        'password': '',
        'repeat_password': ''  
    })  

    assert response.status_code == 302  # Espera-se um redirecionamento após atualização bem-sucedida  
    updated_user = User.query.filter_by(username=random_new_user['username']).first()  
    assert updated_user is not None  
    assert updated_user.email == new_email  

def test_delete_user(test_client, new_user):  
    """Teste para verificar a exclusão da conta do usuário."""  
    test_client.post('/login', data={  
        'username': random_new_user['username'],  # Corrigido para random_new_user['username']
        'password': random_new_user['password'] 
    }) 
    response = test_client.get('/delete')  
    assert response.status_code == 302  
    assert User.query.filter_by(username = random_new_user['username']).first() is None  # Corrigido para random_new_user['username']
