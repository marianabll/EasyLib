import os
from redis import Redis
from dotenv import load_dotenv
from pymongo import MongoClient

# Carregar o conteúdo do arquivo .env
load_dotenv()

# Obter a URI do MongoDB a partir da variável de ambiente
MONGODB_URI = os.getenv("MONGODB_URI")

# Criar a conexão com o MongoDB Atlas
client = MongoClient(MONGODB_URI)

# Configuração do Redis
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

# Instância do cliente Redis
redis_client = Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)


# Acessar o banco de dados (nome do seu banco)
db = client['Library']

# Acessar as coleções
users_collection = db['Users']
books_collection = db['Books']

