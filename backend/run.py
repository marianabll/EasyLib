from flask import Flask
from app.routes import main as main_blueprint
from app.config import Config

def create_app():
    # Inicializa a aplicação Flask
    app = Flask(__name__)

    # Carrega as configurações
    app.config.from_object(Config)

    # Registra blueprints
    app.register_blueprint(main_blueprint)

    return app

if __name__ == "__main__":
    # Cria a aplicação
    app = create_app()
    
    # Define a porta e o modo de execução
    app.run(host='0.0.0.0', port=5000, debug=True)  # Defina debug=True apenas em desenvolvimento
