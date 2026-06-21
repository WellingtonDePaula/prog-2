from flask import render_template, redirect, url_for, flash, request
from model import Desenvolvedor, Tarefa, load_user
from forms import DeveloperForm, LoginForm, TarefaForm, TarefaPesquisarForm, TarefaAtualizarForm
from app import app, db
from flask_login import login_user, logout_user, login_required, current_user


@app.route('/')
def index():
    if(current_user.is_authenticated):
        print(current_user.nome)
    else:
        print('NADA AINDA!')
    form = LoginForm()
    """Rota principal que exibe todos os desenvolvedores e tarefas cadastradas."""
    developers = Desenvolvedor.query.order_by(Desenvolvedor.nome).all()
    tarefas = Tarefa.query.order_by(Tarefa.prazo).all()
    return render_template('index.html', developers=developers, tarefas=tarefas, form = form)

@app.route('/logar',methods=['POST',"GET"])
def logar():
    usuario_logado = False
    form = LoginForm()
    if (form.validate_on_submit()):
        dev = Desenvolvedor.query.filter_by(nome=form.nome.data, senha=form.senha.data).first()
        if(dev):
            login_user(dev)
            flash('Usuário logado com sucesso', 'success')
            return redirect(url_for('index'))
        flash('Email ou senha errados', 'error')
        
    developers = Desenvolvedor.query.order_by(Desenvolvedor.nome).all()
    tarefas = Tarefa.query.order_by(Tarefa.prazo).all()
    return render_template('index.html', developers=developers, tarefas=tarefas, form=form)

@app.route('/deslogar',methods=['POST','GET'])
@login_required
def deslogar():
    form = LoginForm()
    logout_user()
    flash('Usuário deslogado com sucesso!', 'success')
    
    return redirect(url_for('index'))
    # developers = Desenvolvedor.query.order_by(Desenvolvedor.nome).all()
    # tarefas = Tarefa.query.order_by(Tarefa.prazo).all()
    # return render_template('index.html', developers=developers, tarefas=tarefas, form=form)

@app.route('/cadastrar-desenvolvedor', methods=['GET', 'POST'])
def registrar_desenvolvedor():
    """Rota para acessar o formulário e cadastrar novos desenvolvedores."""
    form = DeveloperForm()
    # Processa o formulário se enviado com método POST e passar nas validações
    if form.validate_on_submit():
        new_dev = Desenvolvedor(nome=form.nome.data,
                                senha = form.senha.data)
        db.session.add(new_dev)
        db.session.commit()
        
        login_user(new_dev)
        flash('Desenvolvedor cadastrado com sucesso!', 'success')
        return redirect(url_for('index'))
    if form.errors:
        flash('Preencha corretamente os dados!', 'error')
    return render_template('registrar_desenvolvedor.html', form=form,usuario=current_user)

@app.route('/criar-tarefa', methods=['GET', 'POST'])
@login_required
def criar_tarefa():
    """Rota para visualizar o formulário e criar novas tarefas vinculadas aos desenvolvedores."""
    form = TarefaForm()
    # Popula o SelectField de desenvolvedor_id dinamicamente com as opções do banco de dados
    devs = Desenvolvedor.query.all()
    devs_list = []
    for d in devs:
        devs_list.append((d.id, d.nome))
    form.id_desenvolvedor.choices = devs_list

    # Verifica se os dados do formulário são válidos e processa o cadastro
    if form.validate_on_submit():
        nova_tarefa = Tarefa(
            nome=form.nome.data,
            descricao=form.descricao.data,
            prioridade=form.prioridade.data,
            prazo=form.prazo.data,
            id_desenvolvedor=form.id_desenvolvedor.data
        )
        db.session.add(nova_tarefa)
        db.session.commit()
        flash('Tarefa criada com sucesso!', 'success')
        return redirect(url_for('criar_tarefa'))
    return render_template('criar_tarefa.html', form=form,usuario=current_user)

@app.route('/pesquisar-tarefas', methods=['GET', 'POST'])
def buscar_tarefas():
    form = TarefaPesquisarForm()
    # Por padrão, mostra todas as tarefas ordenadas por data
    tarefas = Tarefa.query.order_by(Tarefa.prazo).all()

    if form.validate_on_submit():
        if form.data_busca.data:
            tarefas = Tarefa.query.filter_by(prazo=form.data_busca.data).order_by(Tarefa.prioridade).all()
        else:
            tarefas = Tarefa.query.order_by(Tarefa.prazo).all()

    return render_template('busca_tarefas.html', form=form, tarefas=tarefas)

@app.route('/editar-tarefa/<int:id_tarefa>/<string:origem>', methods=['GET', 'POST'])
@login_required
def editar_tarefa(id_tarefa, origem):
    tarefa = Tarefa.query.filter_by(id=id_tarefa,id_desenvolvedor=current_user.id).one_or_none()
    if tarefa != None:
        form = TarefaAtualizarForm(obj=tarefa)  # Pré-preenche o formulário com os dados atuais
        devs = Desenvolvedor.query.all()
        devs_list = []
        for d in devs:
            devs_list.append((d.id, d.nome))
        form.id_desenvolvedor.choices = devs_list
        print(request.url_rule)
        print(form.validate_on_submit())
        print(origem)
        if form.validate_on_submit() and origem != "buscar_tarefas" :
            # Atualiza os campos manualmente para garantir compatibilidade de tipos
            tarefa.nome = form.nome.data
            tarefa.descricao = form.descricao.data
            tarefa.prioridade = form.prioridade.data
            tarefa.prazo = form.prazo.data
            tarefa.id_desenvolvedor = form.id_desenvolvedor.data
            
            db.session.commit()
            flash('Tarefa atualizada com sucesso!', 'success')
            return redirect(url_for('buscar_tarefas'))
    else:
        flash('Você não pode editar uma tarefa que não é sua!', 'error')
        return redirect(url_for('buscar_tarefas'))
    return render_template('editar_tarefa.html', form=form, tarefa=tarefa)

@app.route('/deletar-tarefa/<int:id_tarefa>', methods=['POST'])
@login_required
def deletar_tarefa(id_tarefa):
    tarefa = Tarefa.query.filter_by(id=id_tarefa,id_desenvolvedor=current_user.id).one_or_none()
    if tarefa != None:
        db.session.delete(tarefa)
        db.session.commit()
        flash('Tarefa deletada com sucesso!', 'success')
    else:
        flash('Essa tarefa não pertence a você!', 'error')
    return redirect(url_for('buscar_tarefas'))

@app.route("/deletar_usuario<int:id_usuario>", methods=["POST"])
@login_required
def deletar_usuario(id_usuario):
    dev = Desenvolvedor.query.filter_by(id=id_usuario).one_or_none()
    
    if dev != None:
        db.session.delete(dev)
        db.session.commit()
        flash('Usuário deletado com sucesso!', 'success')
        if(dev.id == current_user.id):
            return redirect(url_for('deslogar'))
    else:
        flash('Usuário não encontrado!', 'error')
    return redirect(url_for('index'))