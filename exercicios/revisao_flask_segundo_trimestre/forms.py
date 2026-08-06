from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, SelectField, DateField, SubmitField, PasswordField,RadioField
from wtforms.validators import DataRequired, NumberRange, EqualTo

class LoginForm(FlaskForm):
    cpf = StringField('CPF', validators=[DataRequired(message="O CPF é obrigatório.")])
    senha = PasswordField("Senha",validators=[DataRequired(message="A senha é obrigatória.")])
    submit = SubmitField('Logar')

class CadastrarForm(FlaskForm):
    # id = db.Column(db.Integer,  primary_key=True)
    # cpf = db.Column(db.String(25), nullable=False, unique=True)
    # nome = db.Column(db.String(25), nullable=False)
    # __senha = db.Column(db.String(256), nullable=False)
    # papel = db.Column(db.String(50),nullable=False)
    # ativo = db.Column(db.Boolean,nullable=False)
    nome = StringField('Nome', validators=[DataRequired(message="O nome é obrigatório.")])
    cpf = StringField('CPF', validators=[DataRequired(message="O CPF é obrigatório.")])
    senha = PasswordField('Senha', validators=[DataRequired(message="A senha é obrigatória.")])
    confirmar_senha = PasswordField('Confirmar Senha', validators=[EqualTo('senha'), DataRequired(message="Confirmar a senha é obrigatório.")])
    papel = SelectField('Papel', default='Cliente', choices=[('Cliente', 'Cliente'), ('Vendedor', 'Vendedor'), ('Gerente', 'Gerente')], coerce=str)
    submit = SubmitField('Registrar')