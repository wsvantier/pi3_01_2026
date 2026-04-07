from flask_sqlalchemy import SQLAlchemy
from datetime import date

db = SQLAlchemy()


# Produto
class Produto(db.Model):
    __tablename__ = "produto"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    unidade_medida = db.Column(db.String(20), nullable=False)  # kg, litro, unidade
    estoque_minimo = db.Column(db.Float, nullable=False, default=0)
    ativo = db.Column(db.Boolean, default=True)

    lotes = db.relationship("Lote", backref="produto", lazy=True)

    def estoque_total(self):
        return sum(lote.quantidade_atual for lote in self.lotes)

    def __repr__(self):
        return f"<Produto {self.nome}>"



# Lote (controle de validade)
class Lote(db.Model):
    __tablename__ = "lote"

    id = db.Column(db.Integer, primary_key=True)
    produto_id = db.Column(db.Integer, db.ForeignKey("produto.id"), nullable=False)

    data_recebimento = db.Column(db.Date, nullable=False, default=date.today)
    data_validade = db.Column(db.Date, nullable=False)

    quantidade_inicial = db.Column(db.Float, nullable=False)
    quantidade_atual = db.Column(db.Float, nullable=False)

    numero_guia_remessa = db.Column(db.String(100))

    consumos = db.relationship("Consumo", backref="lote", lazy=True)

    def esta_vencido(self):
        return self.data_validade < date.today()

    def __repr__(self):
        return f"<Lote Produto {self.produto_id} - Validade {self.data_validade}>"



# Consumo Diário
class Consumo(db.Model):
    __tablename__ = "consumo"

    id = db.Column(db.Integer, primary_key=True)
    lote_id = db.Column(db.Integer, db.ForeignKey("lote.id"), nullable=False)

    quantidade = db.Column(db.Float, nullable=False)
    data_consumo = db.Column(db.Date, nullable=False, default=date.today)

    refeicao = db.Column(db.String(50))  # café, almoço, lanche
    numero_alunos = db.Column(db.Integer)

    responsavel = db.Column(db.String(120))

    def __repr__(self):
        return f"<Consumo {self.quantidade} do lote {self.lote_id}>"
