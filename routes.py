from flask import Blueprint, render_template, redirect, url_for, request, jsonify
from .models import db, Lote, Produto, Consumo
from datetime import datetime 


routes_bp = Blueprint('routes_bp', __name__) 

### Estoque ###

# Pagina inicial do Estoque
@routes_bp.route('/') 
def listar_estoque(): 
    return render_template('estoque/listar.html')

# Pagina para inserir novos lotes
@routes_bp.route('/estoque/form') 
def form_estoque():
    produtos = Produto.query.filter_by(ativo=True).all() # Dados para o select do HTML
    return render_template('estoque/form.html', produtos = produtos)

# Rota para inserir itens no banco de dados, (action do form)
@routes_bp.route('/estoque/inserir', methods = ['POST']) 
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
    
    return redirect(url_for('routes_bp.listar_estoque')) 

# API Estoque

@routes_bp.route('/api/estoque')
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
    
### Gênero ###
    
# Pagina Inicial do Gênero 
@routes_bp.route('/genero')
def listar_genero(): 
    return render_template('generos/listar.html') 

# Pagina para inserir novos gêneros 
@routes_bp.route('/genero/form') 
def form_genero(): 
    return render_template('generos/form.html') 

# Rota para o action do form, para inserir dados no banco

@routes_bp.route('/genero/inserir', methods = ['POST'])
def inserir_genero():
    genero = request.form['genero']
    medida = request.form['medida']
    minimo = request.form['min']
    
    novo_produto = Produto(nome = genero,
                           unidade_medida = medida,
                           estoque_minimo = minimo)
    
    try:
        db.session.add(novo_produto)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(e)
    
    return redirect(url_for('routes_bp.listar_estoque'))
    
# API para listar o gênero    

@routes_bp.route('/api/genero')
def api_genero():
    busca = Produto.query.all()
    dados = [{'id':i.id,
              'nome':i.nome,
              'unidade_medida':i.unidade_medida,
              'estoque_minimo':i.estoque_minimo,
              'ativo':i.ativo
              } for i in busca]
    
    return jsonify(dados)
    
    
    

    
### Consumo ###

# Pagina inicial da parte de consumo
@routes_bp.route('/consumo')
def listar_consumo(): 
    return render_template('consumo/listar.html')

# Cadastro de consumo
@routes_bp.route('/consumo/form') 
def form_consumo():
    return render_template('consumo/form.html')

# Rota para inserir consumo

@routes_bp.route('/consumo/inserir', methods=['POST'])
def inserir_consumo():
    try:
        lote_id = int(request.form['lote_id'])
        quantidade = float(request.form['quantidade'])
        data_consumo = datetime.strptime(request.form['data'], '%Y-%m-%d')

        refeicao = request.form.get('refeicao')
        numero_alunos = request.form.get('numero_alunos')
        responsavel = request.form.get('responsavel')

        lote = db.session.get(Lote, lote_id)

        if not lote:
            return {"erro": "Lote não encontrado"}, 404

        # ⚠️ valida estoque
        if lote.quantidade_atual < quantidade:
            return {"erro": "Quantidade maior que o estoque do lote"}, 400

        # Atualiza estoque
        lote.quantidade_atual -= quantidade

        # Registra consumo
        consumo = Consumo(
            lote_id=lote.id,
            quantidade=quantidade,
            data_consumo=data_consumo,
            refeicao=refeicao,
            numero_alunos=numero_alunos,
            responsavel=responsavel
        )

        db.session.add(consumo)
        db.session.commit()

        return redirect(url_for('routes_bp.listar_consumo'))

    except Exception as e:
        db.session.rollback()
        return {"erro": str(e)}, 500
    
# API lote

@routes_bp.route('/api/lotes/<int:produto_id>')
def api_lotes(produto_id):
    lotes = Lote.query\
        .filter_by(produto_id=produto_id)\
        .filter(Lote.quantidade_atual > 0)\
        .order_by(Lote.data_validade)\
        .all()

    dados = [{
        "id": l.id,
        "validade": l.data_validade.strftime('%d/%m/%Y'),
        "quantidade": float(l.quantidade_atual)
    } for l in lotes]

    return jsonify(dados)