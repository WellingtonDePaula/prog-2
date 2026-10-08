from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    TextAreaField,
    IntegerField,
    DecimalField,
    SelectField,
    SubmitField,
    PasswordField,
)
from wtforms.validators import DataRequired, NumberRange, EqualTo, Optional


class RegistrarProdutoForm(FlaskForm):
    marca = StringField('Marca', validators=[DataRequired(message='A marca é obrigatória.')])
    nome = StringField('Nome', validators=[DataRequired(message='O nome é obrigatório.')])
    descricao = TextAreaField('Descrição', validators=[Optional()])
    valor_custo = DecimalField(
        'Valor de custo',
        places=2,
        validators=[
            DataRequired(message='O valor de custo é obrigatório.'),
            NumberRange(min=0.01, message='O valor de custo deve ser maior que zero.'),
        ],
    )
    valor_venda = DecimalField(
        'Valor de venda',
        places=2,
        validators=[
            DataRequired(message='O valor de venda é obrigatório.'),
            NumberRange(min=0.01, message='O valor de venda deve ser maior que zero.'),
        ],
    )
    peso = DecimalField(
        'Peso',
        places=2,
        validators=[
            DataRequired(message='O peso é obrigatório.'),
            NumberRange(min=0.01, message='O peso deve ser maior que zero.'),
        ],
    )
    quantidade = IntegerField(
        'Quantidade em estoque',
        validators=[
            DataRequired(message='A quantidade é obrigatória.'),
            NumberRange(min=0, message='A quantidade não pode ser negativa.'),
        ],
    )
    submit = SubmitField('Registrar')


class SelecionarClienteForm(FlaskForm):
    cpf = StringField('CPF do cliente', validators=[DataRequired(message='Informe o CPF do cliente.')])
    submit = SubmitField('Buscar cliente')


class RealizarVendaForm(FlaskForm):
    produto = SelectField(
        'Produto',
        coerce=int,
        choices=[],
        validators=[DataRequired(message='Selecione um produto.')],
    )
    quantidade = IntegerField(
        'Quantidade',
        validators=[
            DataRequired(message='A quantidade é obrigatória.'),
            NumberRange(min=1, message='A quantidade deve ser pelo menos 1.'),
        ],
    )
    submit = SubmitField('Adicionar produto')


class LoginForm(FlaskForm):
    cpf = StringField('CPF', validators=[DataRequired(message='O CPF é obrigatório.')])
    senha = PasswordField('Senha', validators=[DataRequired(message='A senha é obrigatória.')])
    submit = SubmitField('Logar')


class CadastrarForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired(message='O nome é obrigatório.')])
    cpf = StringField('CPF', validators=[DataRequired(message='O CPF é obrigatório.')])
    senha = PasswordField('Senha', validators=[DataRequired(message='A senha é obrigatória.')])
    confirmar_senha = PasswordField(
        'Confirmar Senha',
        validators=[
            DataRequired(message='Confirmar a senha é obrigatório.'),
            EqualTo('senha', message='As senhas devem ser iguais.'),
        ],
    )
    papel = SelectField(
        'Papel',
        default='Cliente',
        choices=[('Cliente', 'Cliente'), ('Vendedor', 'Vendedor'), ('Gerente', 'Gerente')],
        coerce=str,
    )
    submit = SubmitField('Registrar')