import os

class Config:
    """Classe de configuração para a aplicação."""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'default_secret_key'
    MONGO_URI = os.environ.get('MONGO_URI') or 'mongodb://localhost:27017/seu_banco_de_dados'

# SECRET_KEY: Uma chave secreta usada para proteger dados da sessão. Pode ser definida através de uma variável de ambiente ou uma chave padrão.
# MONGO_URI: A URI de conexão com o MongoDB, que pode ser configurada através de uma variável de ambiente ou um valor padrão.
