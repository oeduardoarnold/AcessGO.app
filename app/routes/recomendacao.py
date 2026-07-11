from flask import Blueprint, render_template
from app.models.hotel import Hotel
from app.models.experiencia import Experiencia
from app.recomendacao.engine import recomendar
from app.forms.preferencia_form import PreferenciaForm

recomendacao_bp = Blueprint("recomendacao", __name__)


@recomendacao_bp.route("/recomendacoes", methods=["GET", "POST"])
def buscar_recomendacoes():
    form = PreferenciaForm()
    hoteis_rec, exp_rec = [], []

    if form.validate_on_submit():
        preferencias = {
            "cidade_id": form.cidade_id.data or None,
            "preco_max": form.preco_max.data,
            "acessibilidade": form.acessibilidade.data,
        }
        hoteis_rec = recomendar(Hotel.query.all(), preferencias, top_n=10)
        exp_rec = recomendar(Experiencia.query.all(), preferencias, top_n=10)

    return render_template(
        "recomendacao/resultado.html",
        form=form, hoteis=hoteis_rec, experiencias=exp_rec
    )