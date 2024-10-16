## 1.0 - Criar página para atualizar os dados de cadastro de um usuário
    ## 1.1 Criar frontend ✅
    ## 1.2 Criar backend e testar lógica na API ✅ 
## 2.0 - Criar botão e ação para deletar conta ✅
    ## 2.1 Criar botão (Pop-up) ✅
    ## 2.2 Criar backend e testar lógica na API ✅
## 3.0 - Realizar testes unitários e testes manuais ✅
## 4.0 - Arrumar código
## 5.0 - Enviar pro GitHub
## 6.0 - Finalizar projeto com documentação (ver zap)


from app import app, db, lm, bcrypt
from flask import render_template, request, redirect, url_for, flash, jsonify, get_flashed_messages
from flask_login import login_user, logout_user, current_user, login_required
from app.models.forms import LoginForm, RegisterForm, UpdateForm
from app.models.tables import User
from sqlite3 import IntegrityError


# Rota da página inicial (home)
# Se um 'user' for passado na URL, será exibido; caso contrário, será 'None'.
@app.route("/home/<user>")
@app.route("/", defaults={'user': None})
def home(user: str):
    messages = get_flashed_messages(with_categories=True)  # Obtém as mensagens flash (ex. erros ou sucessos)
    return render_template("index.html", user=user)  # Renderiza o template da página inicial

# Função para carregar o usuário com base no ID para uso com Flask-Login
@lm.user_loader 
def load_user(id):
    return User.query.filter_by(id=id).first()  # Busca o usuário pelo ID no banco de dados

# Rota da página de login
@app.route("/login", methods=['GET','POST'])
def login():

    form = LoginForm(request.form)  # Instancia o formulário de login
    if request.method == "POST" and form.validate():  # Verifica se o método é POST e o formulário é válido
        username = request.form['username']  # Pega o nome de usuário inserido no formulário
        password = request.form['password']  # Pega a senha inserida
        user = User.query.filter_by(username=form.username.data).first()  # Busca o usuário no banco

        # Verifica se o usuário existe e a senha está correta
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)  # Realiza o login do usuário
            return redirect(url_for('home', user=user.name))  # Redireciona para a página inicial com o nome do usuário
        else:
            flash("Invalid Login.", "danger")  # Exibe mensagem de erro
            return 'Invalid Login. Reload the page.', 400  # Retorna erro 400

    elif request.method == "POST" and not form.validate():
        flash("Erro de validação! Por favor, corrija os erros e tente novamente.", "danger")  # Mensagem de erro
        return redirect(url_for('login'))  # Redireciona para a página de login
    
    return render_template("login.html", form=form)  # Renderiza o template de login


# Rota da página de cadastro (registro)
@app.route("/register", methods=['GET', 'POST'])  
def register():  
    register_form = RegisterForm(request.form)  # Instancia o formulário de registro
    
    if request.method == 'POST' and register_form.validate():  # Verifica se o método é POST e o formulário é válido
        username = register_form.username.data  # Coleta os dados do formulário
        password = register_form.password.data  
        name = register_form.name.data
        age = register_form.age.data
        email = register_form.email.data  

        existing_user = User.query.filter_by(email=email).first()  # Verifica se o email já está em uso
        if existing_user:
            flash("Este email já está em uso. Escolha outro.", "danger")  # Exibe mensagem de erro
            return redirect(url_for('register'))

        # Hash da senha
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')  

        # Criação de um novo usuário
        new_user = User(
            username=username, 
            password=hashed_password,
            name=name,
            age=age,
            email=email
        )  

        try:
            db.session.add(new_user)  # Adiciona o usuário à sessão
            db.session.commit()  # Comita as alterações
        except IntegrityError:
            db.session.rollback()  # Reverte as operações pendentes no caso de erro
            flash("Erro ao cadastrar usuário. Email, usuário ou pode já estar em uso.", "danger")
            return redirect(url_for('register'))
  
        flash("Cadastro bem-sucedido!", "success")  # Mensagem de sucesso
        return redirect(url_for('login'))  # Redireciona para a página de login
    
    elif request.method == 'POST' and not register_form.validate():
        flash("Erro de validação! Por favor, corrija os erros e tente novamente.", "danger")  # Mensagem de erro de validação

    return render_template("register.html", register_form=register_form)  # Renderiza o template de registro

# Rota para logout
@app.route("/logout")
def logout():
    logout_user()  # Desloga o usuário
    flash("Logged out.", 'info')  # Mensagem de sucesso no logout
    return redirect(url_for('login'))  # Redireciona para a página de login

# Rota de pré-login, usada para redirecionamento
@app.route("/pre-login")
def pre_login():
    message = get_flashed_messages(with_categories=True)  # Obtém as mensagens flash
    return redirect(url_for('login'))  # Redireciona para o login

# Rota para visualizar dados de usuários (GET)
@app.route("/data/get", methods=["GET"])
def get_data():
    if current_user.is_authenticated:  # Verifica se o usuário está autenticado
        read = User.query.all()  # Seleciona todos os usuários do banco de dados
        return jsonify([user.to_dict() for user in read])  # Retorna os dados em formato JSON
    else:
        return "Error, you can't access this content. User is not authenticated", 404  # Retorna erro 404 se não autenticado
    
# Rota de pré-atualização
@app.route('/pre-update')
def pre_update():
    messages = get_flashed_messages(with_categories=True)  # Obtém as mensagens flash
    return redirect(url_for('update'))  # Redireciona para a página de atualização

# Rota para atualização de dados de usuário
@app.route("/update", methods=['GET', 'POST'])
@login_required  # Exige que o usuário esteja logado
def update():
    update_form = UpdateForm(request.form)  # Instancia o formulário de atualização
    user_id = current_user.get_id()  # Obtém o ID do usuário logado
    user_update = User.query.filter_by(id=user_id).first()  # Busca o usuário pelo ID

    if user_update and request.method == 'POST' and update_form.validate():  # Verifica se o usuário existe e o formulário é válido
        
        email = update_form.email.data  # Coleta os dados do formulário de atualização
        if email:
            existing_email = User.query.filter(User.email == email, User.id != user_update.id).first()
            if existing_email:
                flash("Este email já está em uso. Escolha outro.", "danger")  # Verifica se o email já está em uso
                return redirect(url_for('update'))
            user_update.email = email

        name = update_form.name.data
        if name:
            user_update.name = name

        age = update_form.age.data
        if age:
            user_update.age = age 
        
        username = update_form.username.data
        if username:
            existing_username = User.query.filter(User.username == username, User.id != user_update.id).first()
            if existing_username:
                flash("Este username já está em uso. Escolha outro.", "danger")  # Verifica se o username já está em uso
                return redirect(url_for('update'))
            
            user_update.username = username
        
        password = update_form.password.data
        if password:
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')  # Hash da nova senha
            user_update.password = hashed_password 

        user_update.verified = True  # Marca o usuário como verificado
        db.session.commit()  # Comita as alterações no banco de dados

        flash("Dados atualizados com sucesso!", "success")  # Mensagem de sucesso
        return redirect(url_for('home', user=user_update.name))  # Redireciona para a página inicial

    elif request.method == 'POST' and not update_form.validate():  
        flash("Erro de validação! Por favor, corrija os erros e tente novamente.", "danger")  # Mensagem de erro de validação

    return render_template('update.html', update_form=update_form)  # Renderiza o template de atualização

# Rota para deletar um usuário
@app.route('/delete', methods=['GET', 'POST'])  
def delete():  
    if current_user.is_authenticated:  # Verifica se o usuário está autenticado
        user_id = current_user.get_id()  
        user = User.query.filter_by(id=user_id).first()  # Busca o usuário pelo ID
        if user:
            db.session.delete(user)  # Deleta o usuário
            db.session.commit()  # Comita a exclusão
            flash('Conta deletada com sucesso!', 'success')  # Mensagem de sucesso
        else:
            flash('Usuário não encontrado.', 'danger')  # Mensagem de erro
    else:
        flash('Conta não pode ser deletada pois o usuário não está autenticado.', 'danger')  # Mensagem de erro para usuário não autenticado
        return 'error, user is not authenticated', 404

    return redirect(url_for('home'))  # Redireciona para a página inicial