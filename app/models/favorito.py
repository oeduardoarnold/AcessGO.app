from app import db
from datetime import datetime

class Favorito(db.Model):
    __tablename__ = 'favorito'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Chaves estrangeiras opcionais (um favorito aponta para um hotel OU para uma experiência/ponto turístico)
    hotel_id = db.Column(db.Integer, db.ForeignKey('hotel.id'), nullable=True)
    experiencia_id = db.Column(db.Integer, db.ForeignKey('experiencia.id'), nullable=True)
    data_adicionado = db.Column(db.DateTime, default=datetime.utcnow)

    # Relacionamentos para carregar os dados facilmente no Jinja2
    hotel = db.relationship('Hotel', backref='favoritados')
    experiencia = db.relationship('Experiencia', backref='favoritados')