from app import db, UserMixin
# from flask_login import login_manager

# Definição da classe User, que representa a tabela "users" no banco de dados
class User(db.Model, UserMixin):

    # Nome da tabela no banco de dados
    __tablename__ = "users"

    # Colunas da tabela com seus respectivos tipos
    id = db.Column(db.Integer, primary_key=True)  # Identificador único do usuário (chave primária)
    username = db.Column(db.String, unique=True)  # Nome de usuário, deve ser único
    password = db.Column(db.String)  # Senha do usuário
    name = db.Column(db.String)  # Nome real do usuário
    age = db.Column(db.Integer)  # Idade do usuário
    email = db.Column(db.String, unique=True)  # Email do usuário, deve ser único

    # Propriedades para integração com Flask-Login
    @property
    def is_authenticated(self):
        return True
    
    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False
    
    # Função que retorna o ID do usuário como string (necessária para o Flask-Login)
    def get_id(self):
        return str(self.id)
    
    # Construtor da classe User, inicializa um novo objeto User com os parâmetros fornecidos
    def __init__(self, username: str, password: str, name: str, age: int, email: str) -> None:
        self.username = username
        self.password = password
        self.name = name
        self.age = age
        self.email = email

    # Representação do objeto User, retorna o nome de usuário quando o objeto for impresso
    def __repr__(self):
        return "<User %r>" % self.username
    
    # Método para converter o objeto User para um dicionário, útil para retornos em APIs
    def to_dict(self):  
        return {  
            "id": self.id,  
            "username": self.username,  
            "name": self.name,  
            "age": self.age,  
            "email": self.email  
        }  

#### Abaixo estão as classes para Posts e Follow, mas estão comentadas. 
#### Estas classes poderiam ser usadas para criar um sistema de postagem e relacionamento entre usuários.

# Classe Post, que representa a tabela "posts" no banco de dados
# class Post(db.Model):

#     __tablename__ = "posts"

#     # Colunas da tabela
#     id = db.Column(db.Integer, primary_key=True)  # Identificador único da postagem
#     content = db.Column(db.String)  # Conteúdo da postagem
#     user_id = db.Column(db.Integer, db.ForeignKey("users.id"))  # Chave estrangeira referenciando a tabela "users"

#     # Relacionamento com o modelo User
#     user = db.relationship("User", foreign_keys=user_id)

#     # Construtor da classe Post
#     def __init__(self, content: str, user_id: int) -> None:
#         self.content = content
#         self.user_id = user_id

#     # Representação do objeto Post
#     def __repr__(self) -> str:
#         return "<Post %r>" % self.id
    
#     # Método para converter o objeto Post para um dicionário
#     def to_dict(self):  
#         return {  
#             "id": self.id,  
#             "content": self.content,  
#             "user_id": self.user_id
#         }  

# Classe Follow, que representa a tabela "follows" no banco de dados
# class Follow(db.Model):

#     __tablename__ = "follows"

#     # Colunas da tabela
#     id = db.Column(db.Integer, primary_key=True)  # Identificador único do relacionamento de seguidores
#     user_id = db.Column(db.Integer, db.ForeignKey("users.id"))  # Chave estrangeira para o usuário seguido
#     follower_id = db.Column(db.Integer, db.ForeignKey("users.id"))  # Chave estrangeira para o seguidor

#     # Relacionamento com o modelo User
#     user = db.relationship("User", foreign_keys=user_id)
#     follower = db.relationship("User", foreign_keys=follower_id)

#     # Construtor da classe Follow
#     def __init__(self, user_id: int, follower_id: int) -> None:
#         self.user_id = user_id
#         self.follower_id = follower_id

#     # Representação do objeto Follow
#     def __repr__(self) -> str:
#         return "<Follow %r>" % self.id
    
#     # Método para converter o objeto Follow para um dicionário
#     def to_dict(self):  
#         return {  
#             "id": self.id,  
#             "user_id": self.user_id,  
#             "follower_id": self.follower_id
#         }  
