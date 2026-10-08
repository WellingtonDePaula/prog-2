from flask import render_template, flash, redirect, url_for, request,session
from flask_login import login_user, current_user, login_required, logout_user
from model import Usuario, Produto, Cliente, Vendedor, Compra, ItemVenda
from forms import LoginForm, ProdutoForm, RegistroUsuarioForm
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
            if usuario is not None:
                 login_user(usuario)
                 flash('Usuário logado com sucesso!', 'success')
                 return render_template("index.html",form=form)
            else:
                 flash('CPF ou senha inválido!', 'error')
    else:
        return render_template("index.html",form=form)
    return render_template("index.html",form=form)

@app.route('/listar_produtos', methods=['GET'])
@login_required
def listar_produtos():
    produtos = current_user.listar_produtos()
    return render_template('listar_produtos.html', produtos=produtos)

@app.route('/cadastrar_produto', methods=['GET', 'POST'])
@login_required
def cadastrar_produto():
    if current_user.papel != "Gerente":
        flash('Acesso negado. Apenas gerentes podem cadastrar produtos.', 'error')
        return redirect(url_for('index'))
    
    form = ProdutoForm()
    if form.validate_on_submit():
        novo_produto = Produto(
            marca=form.marca.data,
            nome=form.nome.data,
            descricao=form.descricao.data,
            valor_custo=form.valor_custo.data,
            valor_venda=form.valor_venda.data,
            peso=form.peso.data,
            quantidade=form.quantidade.data,
            id_gerente=current_user.id
        )
        db.session.add(novo_produto)
        db.session.commit()
        flash('Produto cadastrado com sucesso!', 'success')
        return redirect(url_for('listar_produtos'))
    
    return render_template('cadastrar_produto.html', form=form)

@app.route('/registrar_compra', methods=['GET', 'POST'])
@login_required
def registrar_compra():
    if current_user.papel == "Cliente":
        flash('Acesso negado. Apenas funcionários podem registrar compras.', 'error')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        id_cliente = request.form.get('id_cliente')
        produto_ids = request.form.getlist('produto_id[]')
        quantidades = request.form.getlist('quantidade[]')
        
        if not id_cliente or not produto_ids:
            flash('Selecione um cliente e adicione pelo menos um produto.', 'error')
            return redirect(url_for('registrar_compra'))
            
        nova_compra = Compra(id_cliente=int(id_cliente))
        db.session.add(nova_compra)
        db.session.flush()
        
        for p_id, qtd in zip(produto_ids, quantidades):
            produto = Produto.query.get(int(p_id))
            qtd_comprada = int(qtd)
            if produto and produto.quantidade >= qtd_comprada and qtd_comprada > 0:
                produto.quantidade -= qtd_comprada
                item = ItemVenda(id_produto=produto.id, id_venda=nova_compra.id, preco=produto.valor_venda, quantidade=qtd_comprada)
                db.session.add(item)
            else:
                flash(f'Erro no estoque ou quantidade do produto {produto.nome if produto else "desconhecido"}.', 'error')
                db.session.rollback()
                return redirect(url_for('registrar_compra'))
                
        db.session.commit()
        flash('Compra registrada com sucesso!', 'success')
        return redirect(url_for('listar_produtos'))
        
    clientes = Cliente.query.all()
    produtos = Produto.query.filter(Produto.quantidade > 0).all()
    return render_template('registrar_compra.html', clientes=clientes, produtos=produtos)

@app.route('/registrar_cliente', methods=['GET', 'POST'])
@login_required
def registrar_cliente():
    if current_user.papel == "Cliente":
        flash('Acesso negado. Apenas gerentes e vendedores podem cadastrar clientes.', 'error')
        return redirect(url_for('index'))
    
    form = RegistroUsuarioForm()
    if form.validate_on_submit():
        novo_cliente = Cliente(
            cpf=form.cpf.data,
            nome=form.nome.data,
            senha=form.senha.data,
            papel="Cliente",
            ativo=True
        )
        db.session.add(novo_cliente)
        db.session.commit()
        flash('Cliente registrado com sucesso!', 'success')
        return redirect(url_for('index'))
    
    return render_template('registrar_cliente.html', form=form)

@app.route('/registrar_funcionario', methods=['GET', 'POST'])
@login_required
def registrar_funcionario():
    if current_user.papel != "Gerente":
        flash('Acesso negado. Apenas gerentes podem cadastrar funcionários.', 'error')
        return redirect(url_for('index'))
    
    form = RegistroUsuarioForm()
    if form.validate_on_submit():
        novo_vendedor = Vendedor(
            cpf=form.cpf.data,
            nome=form.nome.data,
            senha=form.senha.data,
            papel="Vendedor",
            ativo=True
        )
        db.session.add(novo_vendedor)
        db.session.commit()
        flash('Vendedor registrado com sucesso!', 'success')
        return redirect(url_for('index'))
    
    return render_template('registrar_funcionario.html', form=form)

@app.route('/deslogar', methods=['POST', 'GET'])
def deslogar():
    logout_user()
    return redirect(url_for('index'))
