from app import db

class Acessibilidade(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    hotel_id = db.Column(db.Integer, db.ForeignKey('hotel.id'))

    rampa = db.Column(db.Boolean, default=False)
    elevador = db.Column(db.Boolean, default=False)
    banheiro_acessivel = db.Column(db.Boolean, default=False)
    piso_tatil = db.Column(db.Boolean, default=False)
    braille = db.Column(db.Boolean, default=False)
    sinalizacao_visual = db.Column(db.Boolean, default=False)
    sinalizacao_auditiva = db.Column(db.Boolean, default=False)
    