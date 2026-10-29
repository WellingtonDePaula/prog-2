from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Optional, Length

class CadastroForm(FlaskForm):
    nome = StringField("Nome",
                        validators=[DataRequired(message="O nome é obrigatório."),
                        Length(min=1, max=120)],
                        render_kw={"placeholder": "Nome do item"}
                    )
    quantidade = IntegerField("Quantidade",
                               validators=[Optional(),   NumberRange(min=0, message="Valor mínimo: 0")],
                               default=0,
                               render_kw={"min": 0}
                             )
    valor = FloatField( "Valor (R$)",
                        validators=[Optional(), NumberRange(min=0.0, message="Valor mínimo: 0")],
                        default=0.0,
                        render_kw={"step": "0.01", "min": 0}
                    )
    submit = SubmitField("Cadastrar")


class BuscaForm(FlaskForm):
    busca = StringField( "Buscar item",
                        validators=[DataRequired(), Length(min=3, message="Digite ao menos 3 letras")],
                        render_kw={"autocomplete": "off", "placeholder": "Mínimo 3 letras"}
                        )


class EdicaoForm(FlaskForm):
    nome = StringField( "Nome",
                        validators=[DataRequired(), Length(min=1, max=120)]
                      )
    quantidade = IntegerField("Quantidade",
                              validators=[Optional(), NumberRange(min=0)],
                                render_kw={"min": 0}
                            )
    valor = FloatField("Valor (R$)",
                        validators=[Optional(), NumberRange(min=0.0)],
                        render_kw={"step": "0.01", "min": 0}
                      )
    submit_atualizar = SubmitField("Atualizar")
    submit_deletar = SubmitField("Deletar")
