import pytest
from pi3_01_2026.app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


### ----------------------
### TESTES DE ROTAS (HTML)
### ----------------------

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


### ----------------------
### TESTES DE APIs
### ----------------------

def test_api_estoque(client):
    response = client.get('/api/estoque')
    assert response.status_code == 200
    assert response.is_json


def test_api_genero(client):
    response = client.get('/api/genero')
    assert response.status_code == 200
    assert response.is_json


def test_api_lotes_sem_parametro(client):
    # Produto inexistente (ou sem lotes)
    response = client.get('/api/lotes/999')
    assert response.status_code == 200
    assert response.is_json


### ----------------------
### TESTES DE POST (INSERÇÃO)
### ----------------------

def test_inserir_genero(client):
    response = client.post('/genero/inserir', data={
        'genero': 'Arroz',
        'medida': 'kg',
        'min': '10'
    }, follow_redirects=True)

    # Deve redirecionar para estoque
    assert response.status_code == 200


def test_inserir_lote(client):
    response = client.post('/estoque/inserir', data={
        'genero': '1',  # depende de existir produto com id=1
        'entrada': '2025-01-01',
        'validade': '2025-12-31',
        'quant': '100'
    }, follow_redirects=True)

    # Mesmo sem garantir banco populado, pelo menos não pode quebrar
    assert response.status_code == 200


def test_inserir_consumo_lote_inexistente(client):
    response = client.post('/consumo/inserir', data={
        'lote_id': '999',
        'quantidade': '10',
        'data': '2025-01-01'
    })

    assert response.status_code == 404


def test_inserir_consumo_erro_estoque(client):
    """
    Esse teste pode falhar se não houver lote real.
    Idealmente você mockaria ou criaria um lote antes.
    """
    response = client.post('/consumo/inserir', data={
        'lote_id': '1',
        'quantidade': '999999',
        'data': '2025-01-01'
    })

    # Pode ser 400 (estoque insuficiente) OU 404 (lote não existe)
    assert response.status_code in [400, 404]