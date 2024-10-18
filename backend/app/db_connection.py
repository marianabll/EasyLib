import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Carregar o conteúdo do arquivo .env
load_dotenv()

# Obter a URI do MongoDB a partir da variável de ambiente
MONGODB_URI = os.getenv("MONGODB_URI")

# Verificar se a URI foi carregada corretamente
if not MONGODB_URI:
    raise ValueError("A URI do MongoDB não foi encontrada. Verifique seu arquivo .env.")

# Conectar ao MongoDB
client = MongoClient(MONGODB_URI)

# Acessar o banco de dados
db = client['Library24']

# Acessar as coleções
users_collection = db['Users']
books_collection = db['Books']
