from app import app, db, lm, bcrypt
from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, logout_user, current_user
from app.models.forms import LoginForm, RegisterForm
from app.models.tables import User
from time import sleep


# Home page
@app.route("/home/<user>")
@app.route("/", defaults = {'user': None})
def home(user: str):
    print(current_user.is_authenticated)  # Verifica se o usuário está autenticado
    return render_template("index.html", user = user)
        
@lm.user_loader # Min-video: 20:06
def load_user(id):
    return User.query.filter_by(id=id).first()

# Login page
@app.route("/login", methods = ['GET','POST']) 
def login():
    form = LoginForm(request.form)
    if request.method == "POST" and form.validate():
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=form.username.data).first()

        # if user and user.password == form.password.data:
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            flash("Logged in.", "success")
            return redirect(url_for('home', user = form.username.data))
        else:
            flash("Invalid Login.", "danger")
            
    elif request.method == "POST" and not form.validate():
        flash("Erro de validação! Por favor, corrija os erros e tente novamente.")
        return redirect(url_for('login'))       
    
    return render_template("login.html", form = form)

# Register page
# @app.route("/index", methods = ['GET', 'POST']) 
# @app.route("/register", methods = ['GET', 'POST'])
# def register():
#     register_form = RegisterForm(request.form)
#     if request.method == 'POST' and register_form.validate():
#         flash("Cadastro bem-sucedido!", "success")
#         return redirect(url_for('login'))
#     elif request.method == 'POST' and not register_form.validate():
#         flash("Erro de validação! Por favor, corrija os erros e tente novamente.", "danger")

#     return render_template("register.html", register_form = register_form)

@app.route("/register", methods=['GET', 'POST'])  
def register():  
    register_form = RegisterForm(request.form)  
    
    if request.method == 'POST' and register_form.validate():  
        username = register_form.username.data    
        password = register_form.password.data  
        name = register_form.name.data
        age = register_form.age.data
        email = register_form.email.data  
        
        # Fazendo o hash da senha  
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')  

        # Criação do novo usuário  
        new_user = User(
            username = username, 
            password = hashed_password,
            name = name,
            age = age,
            email = email
        )  

        db.session.add(new_user)  
        db.session.commit()  
        
        flash("Cadastro bem-sucedido!", "success")  
        return redirect(url_for('login'))  
    
    elif request.method == 'POST' and not register_form.validate():  
        flash("Erro de validação! Por favor, corrija os erros e tente novamente.", "danger")  

    return render_template("register.html", register_form=register_form)  

@app.route("/logout")
def logout():
    logout_user()
    flash("Logged out.", 'info')

    return redirect(url_for('logout_success', _method = 'GET'))

@app.route("/logout_success")
def logout_success():
    sleep(1)
    return redirect(url_for('login'))

# View dos dados
@app.route("/data/get",methods = ["GET"])
def get_data():

    # SELECT * FROM User -> Selecionar tudo
    read = User.query.all()
    return jsonify([user.to_dict() for user in read])  # Retorna a lista de usuários como JSON  


# @app.route('/test-auth')
# def test_auth():
#     print(current_user.is_authenticated)  # Verifica se o usuário está autenticado
#     return jsonify({'authenticated': current_user.is_authenticated})




