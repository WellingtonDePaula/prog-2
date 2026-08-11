from flask import render_template, flash, url_for, redirect, request, session
from flask_login import login_user, current_user, logout_user, login_required
from model import Usuario, Produto, Cliente, Vendedor, Gerente, Compra, ItemVenda, Caixa
from forms import LoginForm, CadastrarForm, RegistrarProdutoForm, RealizarVendaForm, SelecionarClienteForm
from app import app, db


def _produtos_para_venda():
    """Produtos com estoque disponível, formatados para o SelectField do formulário de venda."""
    produtos = Produto.query.filter(Produto.quantidade > 0).all()
    return [(p.id, f'{p.nome} ({p.marca}) - R${p.valor_venda} - estoque: {p.quantidade}') for p in produtos]


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

@app.route('/listar_produtos', methods=['POST', 'GET'])
@login_required
def listar_produtos():
    produtos = Produto.query.all()
    return render_template('listar_produtos.html', produtos=produtos)

@app.route('/registrar_compra', methods=['GET'])
@login_required
def registrar_compra():
    if current_user.papel == "Cliente":
        flash("Clientes não podem registrar compras!", "error")
        return redirect(url_for("index"))

    cliente = None
    cliente_id = session.get('venda_cliente_id')
    if cliente_id:
        cliente = Cliente.query.get(cliente_id)
        if cliente is None:
            session.pop('venda_cliente_id', None)

    carrinho = session.get('venda_carrinho', [])
    itens_carrinho = []
    total = 0
    for indice, item in enumerate(carrinho):
        produto = Produto.query.get(item['produto_id'])
        if produto is None:
            continue
        subtotal = produto.valor_venda * item['quantidade']
        total += subtotal
        itens_carrinho.append({
            'indice': indice,
            'produto': produto,
            'quantidade': item['quantidade'],
            'subtotal': subtotal,
        })

    cliente_form = SelecionarClienteForm()
    venda_form = RealizarVendaForm()
    venda_form.produto.choices = _produtos_para_venda()

    return render_template(
        'registrar_compra.html',
        cliente=cliente,
        cliente_form=cliente_form,
        venda_form=venda_form,
        itens_carrinho=itens_carrinho,
        total=total,
    )


@app.route('/registrar_compra/selecionar_cliente', methods=['POST'])
@login_required
def selecionar_cliente_venda():
    if current_user.papel == "Cliente":
        flash("Clientes não podem registrar compras!", "error")
        return redirect(url_for("index"))

    form = SelecionarClienteForm()
    if form.validate_on_submit():
        cliente = Cliente.query.filter_by(cpf=form.cpf.data).one_or_none()
        if cliente is None:
            flash('Cliente não encontrado. Verifique o CPF ou cadastre o cliente antes.', 'error')
        else:
            session['venda_cliente_id'] = cliente.id
            session['venda_carrinho'] = []
            flash(f'Cliente {cliente.nome} selecionado.', 'success')
    else:
        flash('Informe um CPF válido.', 'error')

    return redirect(url_for('registrar_compra'))


@app.route('/registrar_compra/adicionar_item', methods=['POST'])
@login_required
def adicionar_item_venda():
    if current_user.papel == "Cliente":
        flash("Clientes não podem registrar compras!", "error")
        return redirect(url_for("index"))

    if 'venda_cliente_id' not in session:
        flash('Selecione um cliente antes de adicionar produtos.', 'error')
        return redirect(url_for('registrar_compra'))

    form = RealizarVendaForm()
    form.produto.choices = _produtos_para_venda()

    if form.validate_on_submit():
        produto = Produto.query.get(form.produto.data)
        carrinho = session.get('venda_carrinho', [])

        no_carrinho = sum(item['quantidade'] for item in carrinho if item['produto_id'] == produto.id)
        disponivel = produto.quantidade - no_carrinho

        if form.quantidade.data > disponivel:
            flash(f'Estoque insuficiente de {produto.nome}. Disponível: {disponivel}.', 'error')
        else:
            carrinho.append({'produto_id': produto.id, 'quantidade': form.quantidade.data})
            session['venda_carrinho'] = carrinho
            flash(f'{produto.nome} adicionado à venda.', 'success')
    else:
        flash('Não foi possível adicionar o produto. Verifique os dados.', 'error')

    return redirect(url_for('registrar_compra'))


@app.route('/registrar_compra/remover_item/<int:indice>', methods=['POST'])
@login_required
def remover_item_venda(indice):
    if current_user.papel == "Cliente":
        flash("Clientes não podem registrar compras!", "error")
        return redirect(url_for("index"))

    carrinho = session.get('venda_carrinho', [])
    if 0 <= indice < len(carrinho):
        carrinho.pop(indice)
        session['venda_carrinho'] = carrinho

    return redirect(url_for('registrar_compra'))


@app.route('/registrar_compra/cancelar', methods=['POST'])
@login_required
def cancelar_venda():
    session.pop('venda_carrinho', None)
    session.pop('venda_cliente_id', None)
    flash('Venda cancelada.', 'success')
    return redirect(url_for('registrar_compra'))


@app.route('/registrar_compra/finalizar', methods=['POST'])
@login_required
def finalizar_venda():
    if current_user.papel == "Cliente":
        flash("Clientes não podem registrar compras!", "error")
        return redirect(url_for("index"))

    cliente_id = session.get('venda_cliente_id')
    carrinho = session.get('venda_carrinho', [])

    if not cliente_id:
        flash('Selecione um cliente antes de finalizar a venda.', 'error')
        return redirect(url_for('registrar_compra'))
    if not carrinho:
        flash('Adicione ao menos um produto antes de finalizar a venda.', 'error')
        return redirect(url_for('registrar_compra'))

    compra = Compra(id_cliente=cliente_id, id_vendedor=current_user.id)
    db.session.add(compra)

    for item in carrinho:
        produto = Produto.query.get(item['produto_id'])
        if produto is None or produto.quantidade < item['quantidade']:
            db.session.rollback()
            nome = produto.nome if produto else 'produto removido'
            flash(f'Estoque insuficiente para finalizar a venda ({nome}). Ajuste o carrinho.', 'error')
            return redirect(url_for('registrar_compra'))

        db.session.add(ItemVenda(
            id_produto=produto.id,
            preco=produto.valor_venda,
            quantidade=item['quantidade'],
            compra=compra,
        ))
        produto.quantidade -= item['quantidade']

    db.session.commit()

    session.pop('venda_carrinho', None)
    session.pop('venda_cliente_id', None)

    flash(f'Venda registrada com sucesso! Total: R${compra.total:.2f}', 'success')
    return redirect(url_for('registrar_compra'))

@app.route('/fechar_caixa', methods=['GET', 'POST'])
@login_required
def fechar_caixa():
    if current_user.papel == "Cliente":
        flash("Clientes não podem fechar o caixa!", "error")
        return redirect(url_for("index"))

    compras_pendentes = Compra.query.filter_by(id_caixa=None).order_by(Compra.data).all()
    total_pendente = sum((compra.total for compra in compras_pendentes), 0)

    if request.method == 'POST':
        if not compras_pendentes:
            flash('Não há vendas pendentes para fechar o caixa.', 'error')
            return redirect(url_for('fechar_caixa'))

        caixa = Caixa(id_operador=current_user.id, valor_total=total_pendente)
        db.session.add(caixa)
        for compra in compras_pendentes:
            compra.caixa = caixa
        db.session.commit()

        flash(f'Caixa fechado com sucesso! Total: R${caixa.valor_total:.2f}', 'success')
        return redirect(url_for('fechar_caixa'))

    ultimos_fechamentos = Caixa.query.order_by(Caixa.data_fechamento.desc()).limit(5).all()

    return render_template(
        'fechar_caixa.html',
        compras_pendentes=compras_pendentes,
        total_pendente=total_pendente,
        ultimos_fechamentos=ultimos_fechamentos,
    )


@app.route('/registrar_produto', methods=['POST', 'GET'])
@login_required
def registrar_produto():
    if (current_user.papel != "Gerente"):
        flash("Só o gerente pode registrar produtos!", "error")
        return redirect(url_for('index'))
    form = RegistrarProdutoForm()
    
    if (form.validate_on_submit()):
        produto = Produto.query.filter_by(marca=form.marca.data, nome=form.nome.data).first()
        if(produto is not None):
            flash('Produto já cadastrado', 'error')
            return redirect(url_for('registrar_produto'))
        produto = Produto(
            marca=form.marca.data,
            nome=form.nome.data,
            descricao=form.descricao.data,
            valor_custo=form.valor_custo.data,
            valor_venda=form.valor_venda.data,
            peso=form.peso.data,
            quantidade=form.quantidade.data,
            id_gerente=current_user.id
        )
        db.session.add(produto)
        db.session.commit()
        flash('Produto cadastrado com sucesso!', 'success')
        return redirect(url_for('registrar_produto'))
    
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

@app.route('/registrar_usuario', methods=['POST', 'GET'])
@login_required
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

@app.route('/deslogar', methods=['POST', 'GET'])
@login_required
def deslogar():
    logout_user()
    return redirect(url_for('index'))
