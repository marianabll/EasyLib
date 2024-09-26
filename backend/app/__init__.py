from flask import Flask
from flask_pymongo import PyMongo
from app.config import Config

# Inicialização do banco de dados MongoDB
mongo = PyMongo()

def create_app():
    # Cria a instância da aplicação Flask
    app = Flask(__name__)

    # Carrega as configurações
    app.config.from_object(Config)

    # Inicializa a extensão PyMongo com a configuração da app
    mongo.init_app(app)

    # Registrando blueprints
    from app.routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
