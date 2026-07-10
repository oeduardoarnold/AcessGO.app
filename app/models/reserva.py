from app import db
from datetime import datetime


class Reserva(db.Model):
    __tablename__ = 'reserva'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Chaves estrangeiras opcionais (uma reserva aponta para um hotel OU para uma experiência)
    hotel_id = db.Column(db.Integer, db.ForeignKey('hotel.id'), nullable=True)
    experiencia_id = db.Column(db.Integer, db.ForeignKey('experiencia.id'), nullable=True)

    quantidade = db.Column(db.Integer, default=1, nullable=False)
    valor_total = db.Column(db.Float, default=0.0, nullable=False)

    # Dados do responsável pela reserva
    nome_responsavel = db.Column(db.String(120), nullable=False)
    telefone_contato = db.Column(db.String(20), nullable=False)
    # Por segurança, guardamos apenas os 3 últimos dígitos do CPF (não o número completo)
    cpf_responsavel = db.Column(db.String(14), nullable=False)

    # Dados do cartão de crédito usado no pagamento.
    # Por segurança, NUNCA armazenamos o número completo do cartão nem o CVV no banco;
    # guardamos apenas o nome impresso e os 4 últimos dígitos, apenas para exibição/conferência.
    nome_cartao = db.Column(db.String(120), nullable=True)
    numero_cartao_final = db.Column(db.String(4), nullable=True)
    validade_cartao = db.Column(db.String(5), nullable=True)  # formato MM/AA

    # Datas: hotel usa entrada/saída; experiência usa data + horário do passeio
    data_entrada = db.Column(db.Date, nullable=True)
    data_saida = db.Column(db.Date, nullable=True)
    data_passeio = db.Column(db.Date, nullable=True)
    horario_passeio = db.Column(db.String(5), nullable=True)  # formato "HH:MM"

    observacoes = db.Column(db.Text, nullable=True)

    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)

    # Relacionamentos para carregar os dados facilmente no Jinja2
    hotel = db.relationship('Hotel', backref='reservas')
    experiencia = db.relationship('Experiencia', backref='reservas')

    @property
    def tipo(self):
        return 'hotel' if self.hotel_id else 'experiencia'
