from flask_wtf import FlaskForm
from wtforms import DecimalField, SelectField, SelectMultipleField, widgets
from app.models.cidade import Cidade


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class PreferenciaForm(FlaskForm):
    cidade_id = SelectField("Cidade", coerce=int, choices=[])
    preco_max = DecimalField("Preço máximo", places=2)
    acessibilidade = MultiCheckboxField(
        "Recursos de acessibilidade necessários",
        choices=[
            ("rampa", "Rampa de acesso"),
            ("elevador", "Elevador"),
            ("banheiro_acessivel", "Banheiro acessível"),
            ("piso_tatil", "Piso tátil"),
            ("braille", "Sinalização em braille"),
            ("sinalizacao_visual", "Sinalização visual"),
            ("sinalizacao_auditiva", "Sinalização auditiva"),
            ]
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cidade_id.choices = [(0, "Todas as cidades")] + [
            (c.id, c.nome) for c in Cidade.query.all()
        ]