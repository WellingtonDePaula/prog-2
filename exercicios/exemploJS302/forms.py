from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, FloatField, SelectField, DateField, SubmitField, PasswordField,RadioField
from wtforms.validators import DataRequired, NumberRange, EqualTo

class LoginForm(FlaskForm):
    cpf = StringField('CPF', validators=[DataRequired(message="O CPF é obrigatório.")])
    senha = PasswordField("Senha",validators=[DataRequired(message="A senha é obrigatória.")])
    submit = SubmitField('Logar')

class ProdutoForm(FlaskForm):
    marca = StringField('Marca', validators=[DataRequired(message="A marca é obrigatória.")])
    nome = StringField('Nome', validators=[DataRequired(message="O nome é obrigatório.")])
    descricao = TextAreaField('Descrição')
    valor_custo = FloatField('Valor de Custo', validators=[DataRequired(message="O valor de custo é obrigatório.")])
    valor_venda = FloatField('Valor de Venda', validators=[DataRequired(message="O valor de venda é obrigatório.")])
    peso = FloatField('Peso', validators=[DataRequired(message="O peso é obrigatório.")])
    quantidade = IntegerField('Quantidade', validators=[DataRequired(message="A quantidade é obrigatória.")])
    submit = SubmitField('Cadastrar Produto')

class RegistroUsuarioForm(FlaskForm):
    cpf = StringField('CPF', validators=[DataRequired(message="O CPF é obrigatório.")])
    nome = StringField('Nome', validators=[DataRequired(message="O nome é obrigatório.")])
    senha = PasswordField("Senha", validators=[DataRequired(message="A senha é obrigatória.")])
    submit = SubmitField('Registrar')
