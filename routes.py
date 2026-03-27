from flask import Blueprint, render_template, redirect, url_for, request 
from .models import db, Lote, Produto 
from datetime import datetime 


routes_bp = Blueprint('routes_bp', __name__) 

# Estoque 

@routes_bp.route('/') 
def listar_estoque(): 
    return render_template('estoque/listar.html')

@routes_bp.route('/estoque/form') 
def form_estoque():
    produtos = Produto.query.filter_by(ativo=True).all()
    return render_template('estoque/form.html', produtos = produtos)

@routes_bp.route('/estoque/inserir', methods = ['POST']) 
def inserir_lote(): 
    genero = request.form['genero']
    entrada = datetime.strptime(request.form['entrada'], '%Y-%m-%d')
    validade = datetime.strptime(request.form['validade'], '%Y-%m-%d')
    quantidade = int(request.form['quant']) 
    novo_lote = Lote(
        produto_id = genero,
        data_recebimento = entrada,
        data_validade = validade,
        quantidade_inicial = quantidade)
    
    try: 
        db.session.add(novo_lote)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(e)
        return redirect(url_for('routes_bp.listar_estoque')) 
    
 # Gênero
    
@routes_bp.route('/genero')
def listar_genero(): 
    return render_template('generos/listar.html') 

@routes_bp.route('/genero/form') 
def form_genero(): 
    return render_template('generos/form.html') 

# Consumo

@routes_bp.route('/consumo')
def listar_consumo(): 
    return render_template('consumo/listar.html')

@routes_bp.route('/consumo/form') 
def form_consumo():
    return render_template('consumo/form.html')