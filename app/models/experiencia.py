from app import db

class Experiencia(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150))
    descricao = db.Column(db.Text)

    cidade_id = db.Column(db.Integer, db.ForeignKey('cidade.id'))

    categoria = db.Column(db.String(50))
    
    preco = db.Column(db.Float, nullable=True, default=0.00)
