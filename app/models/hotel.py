from app import db

class Hotel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150))
    descricao = db.Column(db.Text)

    cidade_id = db.Column(db.Integer, db.ForeignKey('cidade.id'))

    endereco = db.Column(db.String(200))
    telefone = db.Column(db.String(20))
    preco = db.Column(db.Float, nullable=True, default=0.00)

    acessibilidade = db.relationship('Acessibilidade', backref='hotel', uselist=False)