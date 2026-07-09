from app import db
from datetime import datetime

class Carrinho(db.Model):
    __tablename__ = 'carrinho'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Chaves estrangeiras opcionais (um item do carrinho aponta para um hotel OU para uma experiência/ponto turístico)
    hotel_id = db.Column(db.Integer, db.ForeignKey('hotel.id'), nullable=True)
    experiencia_id = db.Column(db.Integer, db.ForeignKey('experiencia.id'), nullable=True)

    # Quantidade do item (ex: diárias, ingressos)
    quantidade = db.Column(db.Integer, default=1, nullable=False)
    data_adicionado = db.Column(db.DateTime, default=datetime.utcnow)

    # Relacionamentos para carregar os dados facilmente no Jinja2
    hotel = db.relationship('Hotel', backref='no_carrinho')
    experiencia = db.relationship('Experiencia', backref='no_carrinho')

    @property
    def subtotal(self):
        """Calcula o subtotal do item (preço unitário x quantidade)."""
        if self.hotel:
            return self.hotel.preco * self.quantidade
        if self.experiencia:
            return self.experiencia.preco * self.quantidade
        return 0
