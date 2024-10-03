from app import db, UserMixin
# from flask_login import login_manager

class User(db.Model, UserMixin):

    # Nome databela
    __tablename__ = "users"

    # Colunas da tabela
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String, unique = True)
    password = db.Column(db.String)
    name = db.Column(db.String)
    age = db.Column(db.Integer)
    email = db.Column(db.String, unique = True)

    @property
    def is_authenticated(self):
        return True
    
    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False
    
    def get_id(self):
        return str(self.id)
    
    # Constructor

    def __init__(self, username: str, password: str, name: str, age: int ,email: str) -> None:

        self.username = username
        self.password = password
        self.name = name
        self.age = age
        self.email = email

    # Representação do objeto

    def __repr__(self):
        return "<User %r>" % self.username
    
    def to_dict(self):  
        return {  
            "id": self.id,  
            "username": self.username,  
            "name": self.name,  
            "age": self.age,  
            "email": self.email  
        }  
    
# class Post(db.Model):

#     # Nome da tabela

#     __tablename__ = "posts"

#     # Colunas da tabela

#     id = db.Column(db.Integer, primary_key = True)
#     content = db.Column(db.String)
#     user_id = db.Column(db.Integer, db.ForeignKey("users.id"))


#     # Relacionamento

#     user = db.relationship("User", foreign_keys = user_id)


#     # Constructor

#     def __init__(self, content: str, user_id: int) -> None:
#         self.content = content
#         self.user_id = user_id

    
#     def __repr__(self) -> str:
#         return "<Post %r>" % self.id
    
#     def to_dict(self):  
#         return {  
#             "id": self.id,  
#             "content": self.content,  
#             "user_id": self.user_id
#         }  
    

# class Follow(db.Model):

#     # Nome da tabela

#     __tablename__ = "follows"

#     # Colunas

#     id = db.Column(db.Integer, primary_key = True)
#     user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
#     follower_id = db.Column(db.Integer, db.ForeignKey("users.id"))

#     # Relacionamentos

#     user = db.relationship("User", foreign_keys = user_id)
#     follower = db.relationship("User", foreign_keys = follower_id)

#     # Constructor

#     def __init__(self, user_id: int, follower_id: int) -> None:
#         self.user_id = user_id
#         self.follower_id = follower_id

#     def __repr__(self) -> str:
#         return "<Follow %r>" % self.id
    
#     def to_dict(self):  
#         return {  
#             "id": self.id,  
#             "user_id": self.user_id,  
#             "follower_id": self.follower_id
#         }  