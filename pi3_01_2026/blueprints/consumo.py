from flask import Blueprint, render_template, redirect, url_for, request, jsonify
from pi3_01_2026.models import db, Lote, Consumo
from datetime import datetime 

consumo = Blueprint('consumo', __name__) 


    
### Consumo ###

# Pagina inicial da parte de consumo
@consumo.route('/consumo')
def listar_consumo(): 
    return render_template('consumo/listar.html')

# Cadastro de consumo
@consumo.route('/consumo/form') 
def form_consumo():
    return render_template('consumo/form.html')

# Rota para inserir consumo

@consumo.route('/consumo/inserir', methods=['POST'])
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

        return redirect(url_for('consumo.listar_consumo'))

    except Exception as e:
        db.session.rollback()
        return {"erro": str(e)}, 500
    
# API lote

@consumo.route('/api/lotes/<int:produto_id>')
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

@consumo.route('/api/consumo')
def api_consumo():
    consumos = Consumo.query.order_by(Consumo.data_consumo.desc()).all()

    dados = []
    for c in consumos:
        dados.append({
            "id": c.id,
            "produto": c.lote.produto.nome,
            "quantidade": float(c.quantidade),
            "data": c.data_consumo.strftime('%d/%m/%Y'),
            "refeicao": c.refeicao,
            "responsavel": c.responsavel
        })

    return jsonify(dados)