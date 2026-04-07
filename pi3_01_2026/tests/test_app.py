import pytest
from datetime import datetime

from pi3_01_2026.app import create_app
from pi3_01_2026.models import db, Produto, Lote


# ----------------------
# CONFIGURAÇÃO DO APP
# ----------------------

@pytest.fixture
def app():
    app = create_app()

    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SQLALCHEMY_TRACK_MODIFICATIONS": False
    })

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


# ----------------------
# DADOS DE TESTE
# ----------------------

@pytest.fixture
def produto_teste(app):
    produto = Produto(
        nome="Arroz",
        unidade_medida="kg",
        estoque_minimo=10
    )

    db.session.add(produto)
    db.session.commit()

    return produto


@pytest.fixture
def lote_teste(app, produto_teste):
    lote = Lote(
        produto_id=produto_teste.id,
        data_recebimento=datetime(2025, 1, 1),
        data_validade=datetime(2025, 12, 31),
        quantidade_inicial=100,
        quantidade_atual=100
    )

    db.session.add(lote)
    db.session.commit()

    return lote


# ----------------------
# TESTES DE ROTAS (HTML)
# ----------------------

def test_estoque_status_code(client):
    response = client.get('/')
    assert response.status_code == 200


def test_genero_status_code(client):
    response = client.get('/genero')
    assert response.status_code == 200


def test_consumo_status_code(client):
    response = client.get('/consumo')
    assert response.status_code == 200


def test_form_estoque_status_code(client):
    response = client.get('/estoque/form')
    assert response.status_code == 200


def test_form_genero_status_code(client):
    response = client.get('/genero/form')
    assert response.status_code == 200


def test_form_consumo_status_code(client):
    response = client.get('/consumo/form')
    assert response.status_code == 200


# ----------------------
# TESTES DE APIs
# ----------------------

def test_api_estoque_vazio(client):
    response = client.get('/api/estoque')
    assert response.status_code == 200
    assert response.is_json
    assert response.get_json() == []


def test_api_estoque_com_dados(client, produto_teste):
    response = client.get('/api/estoque')
    data = response.get_json()

    assert response.status_code == 200
    assert isinstance(data, list)
    assert data[0]['nome'] == "Arroz"


def test_api_genero(client, produto_teste):
    response = client.get('/api/genero')
    data = response.get_json()

    assert response.status_code == 200
    assert isinstance(data, list)
    assert data[0]['nome'] == "Arroz"


def test_api_lotes(client, lote_teste):
    response = client.get(f'/api/lotes/{lote_teste.produto_id}')
    data = response.get_json()

    assert response.status_code == 200
    assert isinstance(data, list)
    assert data[0]['quantidade'] == 100.0


# ----------------------
# TESTES DE INSERÇÃO
# ----------------------

def test_inserir_genero(client):
    response = client.post('/genero/inserir', data={
        'genero': 'Feijão',
        'medida': 'kg',
        'min': '5'
    }, follow_redirects=True)

    assert response.status_code == 200


def test_inserir_lote(client, produto_teste):
    response = client.post('/estoque/inserir', data={
        'genero': str(produto_teste.id),
        'entrada': '2025-01-01',
        'validade': '2025-12-31',
        'quant': '50'
    }, follow_redirects=True)

    assert response.status_code == 200


# ----------------------
# TESTES DE CONSUMO
# ----------------------

def test_consumo_sucesso(client, lote_teste):
    response = client.post('/consumo/inserir', data={
        'lote_id': lote_teste.id,
        'quantidade': '10',
        'data': '2025-01-01'
    }, follow_redirects=True)

    assert response.status_code == 200

    # Verifica se o estoque foi atualizado
    lote_atualizado = db.session.get(Lote, lote_teste.id)
    assert lote_atualizado.quantidade_atual == 90


def test_consumo_estoque_insuficiente(client, lote_teste):
    response = client.post('/consumo/inserir', data={
        'lote_id': lote_teste.id,
        'quantidade': '200',
        'data': '2025-01-01'
    })

    assert response.status_code == 400


def test_consumo_lote_inexistente(client):
    response = client.post('/consumo/inserir', data={
        'lote_id': '999',
        'quantidade': '10',
        'data': '2025-01-01'
    })

    assert response.status_code == 404