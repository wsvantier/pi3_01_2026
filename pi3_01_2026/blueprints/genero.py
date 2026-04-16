from flask import Blueprint, render_template, redirect, url_for, request, jsonify
from pi3_01_2026.models import db, Produto

genero = Blueprint('genero', __name__) 

### Gênero ###
    
# Pagina Inicial do Gênero 
@genero.route('/genero')
def listar_genero(): 
    return render_template('generos/listar.html') 

# Pagina para inserir novos gêneros 
@genero.route('/genero/form') 
def form_genero(): 
    return render_template('generos/form.html') 

# Rota para o action do form, para inserir dados no banco

@genero.route('/genero/inserir', methods = ['POST'])
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
    
    return redirect(url_for('estoque.listar_estoque'))
    
# API para listar o gênero    

@genero.route('/api/genero')
def api_genero():
    busca = Produto.query.all()

    dados = [{
        'id': i.id,
        'nome': i.nome,
        'unidade_medida': i.unidade_medida,
        'estoque_minimo': float(i.estoque_minimo),
        'estoque_total': float(i.estoque_total()), 
        'ativo': i.ativo
    } for i in busca]

    return jsonify(dados)
    
    