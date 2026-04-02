from flask import Blueprint, render_template, redirect, url_for, request, jsonify
from pi3_01_2026.models import db, Lote, Produto
from datetime import datetime 

estoque = Blueprint('estoque', __name__) 

### Estoque ###

# Pagina inicial do Estoque
@estoque.route('/') 
def listar_estoque(): 
    return render_template('estoque/listar.html')

# Pagina para inserir novos lotes
@estoque.route('/estoque/form') 
def form_estoque():
    produtos = Produto.query.filter_by(ativo=True).all() # Dados para o select do HTML
    return render_template('estoque/form.html', produtos = produtos)

# Rota para inserir itens no banco de dados, (action do form)
@estoque.route('/estoque/inserir', methods = ['POST']) 
def inserir_lote(): 
    genero = request.form['genero']
    entrada = datetime.strptime(request.form['entrada'], '%Y-%m-%d')
    validade = datetime.strptime(request.form['validade'], '%Y-%m-%d')
    quantidade = float(request.form['quant']) 
    novo_lote = Lote(
                    produto_id=genero,
                    data_recebimento=entrada,
                    data_validade=validade,
                    quantidade_inicial=quantidade,
                    quantidade_atual=quantidade
                )
    
    try: 
        db.session.add(novo_lote)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(e)
    
    return redirect(url_for('estoque.listar_estoque')) 

# API Estoque

@estoque.route('/api/estoque')
def api_estoque():
    produtos = Produto.query.filter_by(ativo=True).all()

    dados = []
    for p in produtos:
        dados.append({
            "id": p.id,
            "nome": p.nome,
            "unidade_medida": p.unidade_medida,
            "estoque_total": float(p.estoque_total())
        })

    return jsonify(dados)