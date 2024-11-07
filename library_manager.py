from database import users_collection, books_collection, redis_client
from fastapi.encoders import jsonable_encoder
from bson.objectid import ObjectId
from datetime import datetime
from models import UserModel

# Criar um novo usuário
def create_user(user_data: UserModel):
    # Insere o documento no MongoDB usando a representação do modelo
    result = users_collection.insert_one(user_data.dict(exclude={"id"}))

    # Cria um dicionário com o ObjectId convertido para string
    created_user = user_data.dict()
    created_user["id"] = str(result.inserted_id)

    return created_user

# Criar um novo livro (sem endpoint)
def create_book(book_data):
    book_data["_id"] = ObjectId()
    books_collection.insert_one(book_data)
    return jsonable_encoder(book_data)  # Garantir que seja serializável

# Obter um usuário pelo username
def get_user(username):
    user = users_collection.find_one({"username": username})
    if user:
        user["_id"] = str(user["_id"])  # Converter ObjectId para string
        return jsonable_encoder(user)  # Garantir que seja serializável
    return None

# Obter um livro pelo ID
def get_book(book_id):
    book = books_collection.find_one({"_id": ObjectId(book_id)})
    if book:
        book["_id"] = str(book["_id"])
        return jsonable_encoder(book)
    return None

# Verificar a disponibilidade de um livro (usada em outras funções)
def check_book_availability(book_id):
    book = books_collection.find_one({"_id": ObjectId(book_id)}, {"transactions": 1})
    if book and "transactions" in book:
        last_transaction = book["transactions"][-1] if book["transactions"] else None
        if last_transaction and last_transaction["transaction_type"] == "borrow":
            return False  # Livro não disponível (empréstimo ativo)
    return True  # Livro disponível

# Realizar o empréstimo de um livro
def borrow_book(user_id, book_id):
    # Verifica a disponibilidade do livro
    if not check_book_availability(book_id):
        return {"status": "error", "message": "Book not available"}

    # Atualiza a coleção de livros
    books_collection.update_one(
        {"_id": ObjectId(book_id)},
        {"$push": {
            "transactions": {
                "transaction_type": "borrow",
                "transaction_date": datetime.now().strftime("%Y-%m-%d"),
                "user_id": ObjectId(user_id)
            }
        }}
    )

    # Atualiza a coleção de usuários
    users_collection.update_one(
        {"_id": ObjectId(user_id)},
        {"$push": {
            "transactions": {
                "transaction_type": "borrow",
                "transaction_date": datetime.now().strftime("%Y-%m-%d"),
                "book_id": ObjectId(book_id)
            }
        }}
    )

    # Incrementa o contador de empréstimos do usuário no Redis
    redis_client.hincrby("loan_counter", str(user_id), 1)

    return {"status": "success", "message": "Book borrowed successfully"}


# Realizar a devolução de um livro
def return_book(user_id, book_id):
    # 1. Verifica a transação mais recente para ver se o livro foi emprestado ao usuário em questão
    book = books_collection.find_one({"_id": ObjectId(book_id)})
    
    # Confere se a última transação foi um empréstimo pelo mesmo usuário
    if book and book["transactions"] and book["transactions"][-1]["transaction_type"] == "borrow" and book["transactions"][-1]["user_id"] == ObjectId(user_id):
        # 2. Adiciona a transação de devolução na coleção Books
        books_collection.update_one(
            {"_id": ObjectId(book_id)},
            {"$push": {
                "transactions": {
                    "transaction_type": "return",
                    "transaction_date": datetime.now().strftime("%Y-%m-%d"),
                    "user_id": ObjectId(user_id)
                }
            }}
        )

        # 3. Adiciona a transação de devolução na coleção Users
        users_collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$push": {
                "transactions": {
                    "transaction_type": "return",
                    "transaction_date": datetime.now().strftime("%Y-%m-%d"),
                    "book_id": ObjectId(book_id)
                }
            }}
        )
        
        return "Book returned successfully"

    return "Book not borrowed by this user"

# Consultar o histórico de transações de um usuário (sem endpoint)
def get_user_transaction_history(user_id):
    user = users_collection.find_one({"_id": ObjectId(user_id)}, {"transactions": 1})
    if user and "transactions" in user:
        return jsonable_encoder(user["transactions"])  # Garantir que seja serializável
    return []

# Contar o número de livros emprestados atualmente por um usuário (sem endpoint)
def count_books_issued(user_id):
    user = users_collection.find_one({"_id": ObjectId(user_id)}, {"transactions": 1})
    if user and "transactions" in user:
        borrow_count = 0
        for transaction in user["transactions"]:
            if transaction["transaction_type"] == "borrow":
                borrow_count += 1
            elif transaction["transaction_type"] == "return":
                borrow_count -= 1
        return borrow_count
    return 0

# Consultar os livros atualmente emprestados por um usuário (sem endpoint)
def get_currently_borrowed_books(user_id):
    user = users_collection.find_one({"_id": ObjectId(user_id)}, {"transactions": 1})
    if user and "transactions" in user:
        borrowed_books = []
        for transaction in user["transactions"]:
            if transaction["transaction_type"] == "borrow":
                borrowed_books.append(transaction["book_id"])
            elif transaction["transaction_type"] == "return" and transaction["book_id"] in borrowed_books:
                borrowed_books.remove(transaction["book_id"])
        return borrowed_books
    return []

# Consultar o histórico de transações de um livro
def get_book_transaction_history(book_id):
    book = books_collection.find_one({"_id": ObjectId(book_id)}, {"transactions": 1})
    if book and "transactions" in book:
        return jsonable_encoder(book["transactions"])  # Garantir que seja serializável
    return []

# Excluir um usuário a partir do seu username
def delete_user(username):
    result = users_collection.delete_one({"username": username})
    if result.deleted_count == 1:
        return {"message": "User deleted successfully"}
    else:
        return {"message": "User not found"}


# Contar o total de transações por cada usuário usando agregação
def get_transaction_count_per_user():
    pipeline = [
        {"$unwind": "$transactions"},
        {"$group": {
            "_id": "$_id",
            "username": {"$first": "$username"},
            "transaction_count": {"$sum": 1}
        }}
    ]
    result = users_collection.aggregate(pipeline)
    formatted_result = [
        {
            "id": str(record["_id"]),
            "username": record["username"],
            "transaction_count": record["transaction_count"]
        }
        for record in result
    ]
    return jsonable_encoder(formatted_result)

# Obter livros disponíveis por gênero usando agregação
def get_available_books_by_genre(genre):

    pipeline = [
        {"$match": {"book_genre": genre}},
        {"$project": {
            "_id": {"$toString": "$_id"},  # Converte o _id para string
            "book_name": 1,
            "author": 1,
            "book_genre": 1,
            "transactions": 1  # Inclui as transações para verificação
        }}
    ]
    result = books_collection.aggregate(pipeline)

    available_books = []
    for book in result:
        if check_book_availability(book["_id"]):  # Verifica a disponibilidade
            available_books.append({
                "_id": str(book["_id"]),  # Converte ObjectId para string
                "book_name": book["book_name"],
                "author_name": book["author"]["name"]
            })

    return jsonable_encoder(available_books) # Garantir que seja serializável

# Contar quantas vezes cada livro foi emprestado usando agregação (sem endpoint)
def get_most_borrowed_books():
    pipeline = [
        {"$unwind": "$transactions"},
        {"$match": {
            "transactions.transaction_type": "borrow"
        }},
        {"$group": {
            "_id": "$_id",
            "book_name": {"$first": "$book_name"},
            "borrow_count": {"$sum": 1}
        }},
        {"$sort": {"borrow_count": -1}}
    ]
    result = books_collection.aggregate(pipeline)
    return jsonable_encoder(list(result))  # Garantir que seja serializável