from flask import Flask
from .models import db
from .blueprints.consumo import consumo
from .blueprints.estoque import estoque
from .blueprints.genero import genero

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

    db.init_app(app)

    with app.app_context():
        db.create_all()
  
    app.register_blueprint(consumo)
    app.register_blueprint(estoque)
    app.register_blueprint(genero)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0')
