from flask import render_template, flash, url_for, redirect
from flask_login import login_user, current_user, logout_user, login_required
from model import Usuario, Produto, Cliente, Vendedor, Gerente
from forms import LoginForm, CadastrarForm, RegistrarProdutoForm
from app import app, db

@app.route('/')
def index():
    form = LoginForm()
    return render_template("index.html",form=form)


@app.route('/logar', methods=['POST', 'GET'])
def logar(): 
    form = LoginForm()
    if not current_user.is_authenticated:
        if form.validate_on_submit():
            usuario = Usuario.query.filter_by(cpf=form.cpf.data).one_or_none()
            if usuario is not None and usuario.verificar_senha(form.senha.data):
                 login_user(usuario)
                 flash('Usuário logado com sucesso!', 'success')
                 return render_template("index.html",form=form)
            else:
                 flash('CPF ou senha inválido!', 'error')
    else:
        return render_template("index.html",form=form)
    return render_template("index.html",form=form)

@login_required
@app.route('/listar_produtos', methods=['POST', 'GET'])
def listar_produtos():
    produtos = Produto.query.all()
    return render_template('listar_produtos.html', produtos=produtos)

@login_required
@app.route('/registrar_compra', methods=['POST', 'GET'])
def registrar_compra():
    if (current_user.papel == "Cliente"):
        flash("Clientes não podem registrar compras!", "error")
        return redirect(url_for("index"))
    
    return render_template('registrar_compra.html')

@login_required
@app.route('/registrar_produto', methods=['POST', 'GET'])
def registrar_produto():
    if (current_user.papel != "Gerente"):
        flash("Só o gerente pode registrar produtos!", "error")
        return redirect(url_for('index'))
    form = RegistrarProdutoForm()
    
    if (form.validate_on_submit()):
        pass
    
    return render_template("registrar_produto.html", form=form)

@app.route('/registrar_cliente', methods=['POST', 'GET'])
def registrar_cliente():
    form = CadastrarForm()
    
    form.papel.data = "Cliente"
    
    if (form.validate_on_submit()):
        atual = Usuario.query.filter_by(cpf=form.cpf.data).first()
        if (atual != None):
            flash("Cpf já cadastrado!", "error")
            return redirect(url_for('index'))
        
        cliente = Cliente(nome=form.nome.data, cpf=form.cpf.data, senha=form.senha.data, ativo = True)
        
        db.session.add(cliente)
        db.session.commit()
        flash("Cliente cadastrado com sucesso", "success")
        return redirect(url_for('index'))
        
    return render_template('registrar_cliente.html', form=form)

@login_required
@app.route('/registrar_usuario', methods=['POST', 'GET'])
def registrar_usuario():
    form = CadastrarForm()
    
    if (form.validate_on_submit()):
        atual = Usuario.query.filter_by(cpf=form.cpf.data).first()
        if (atual != None):
            flash("Cpf já cadastrado!", "error")
            return redirect(url_for('index'))
        
        usuario = None
        if (form.papel.data == "Cliente"):
            usuario = Cliente(nome=form.nome.data, cpf=form.cpf.data, senha=form.senha.data, ativo = True)
        elif (form.papel.data == "Vendedor"):
            usuario = Vendedor(nome=form.nome.data, cpf=form.cpf.data, senha=form.senha.data, ativo = True)
        elif (form.papel.data == "Gerente"):
            usuario = Gerente(nome=form.nome.data, cpf=form.cpf.data, senha=form.senha.data, ativo = True)
        
        db.session.add(usuario)
        db.session.commit()
        flash(f"{form.papel.data} cadastrado com sucesso", "success")
        return redirect(url_for('index'))
        
    return render_template('registrar_usuario.html', form=form)

@login_required
@app.route('/deslogar', methods=['POST', 'GET'])
def deslogar():
    logout_user()
    return redirect(url_for('index'))