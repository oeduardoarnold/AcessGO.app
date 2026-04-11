from app import db

class Cidade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    estado = db.Column(db.String(2))

    hoteis = db.relationship('Hotel', backref='cidade', lazy=True)
    experiencias = db.relationship('Experiencia', backref='cidade', lazy=True)