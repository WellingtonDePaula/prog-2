from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, FloatField
from wtforms.validators import DataRequired, Length

class CadastroForm(FlaskForm):
    nome = StringField("Nome", validators=[DataRequired(message="O nome é obrigatório"), Length(min=1, max=100, message="O nome não deve passar de 100 caracteres")])
    raca = StringField("Raça", validators=[DataRequired(message="A raça é obrigatória")])
    peso = FloatField("Peso", validators=[DataRequired(message="O peso é obrigatório")])
    sexo = StringField("Sexo", validators=(DataRequired(message="O sexo é obrigatório"), Length(min=1, max=1, message="O sexo deve ser dado em 1 caractere (F ou M)")))
    submit = SubmitField("Cadastrar")