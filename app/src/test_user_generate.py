import random
import string
from faker import Faker

# Inicializando o gerador de dados fictícios
fake = Faker()

def generate_random_user():
    # Gerando um e-mail aleatório
    new_email = fake.email()
    
    # Gerando um nome aleatório
    name = fake.name()
    
    # Gerando uma idade aleatória entre 18 e 99
    age = random.randint(18, 100)
    
    # Gerando um nome de usuário aleatório
    username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    
    # Gerando uma senha aleatória
    password = ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=12))
    
    # A senha de repetição será igual à senha gerada
    repeat_password = password
    
    # Criando o dicionário com os valores gerados
    user_data = {
        'email': new_email,
        'name': name,
        'age': age,
        'username': username,
        'password': password,
        'repeat_password': repeat_password
    }
    
    return user_data

# print(generate_random_user())
