from db_connection import db, users_collection, books_collection
from bson.objectid import ObjectId
from datetime import datetime

# Função para verificar a disponibilidade de um livro
def check_book_availability(book_id):
    book = books_collection.find_one({"_id": ObjectId(book_id)}, {"transactions": 1})
    if book and "transactions" in book:
        last_transaction = book["transactions"][-1] if book["transactions"] else None
        if last_transaction and last_transaction["transaction_type"] == "borrow":
            return False  # Livro não disponível (empréstimo ativo)
    return True  # Livro disponível

# Função para realizar o empréstimo de um livro
def borrow_book(user_id, book_id):
    # Verifica se o livro está disponível
    if not check_book_availability(book_id):
        return "Livro não disponível para empréstimo."

    # Adiciona a transação de empréstimo ao livro
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

    # Adiciona a transação de empréstimo ao usuário
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

    return "Livro emprestado com sucesso!"

# Função para realizar a devolução de um livro
def return_book(user_id, book_id):
    # Adiciona a transação de devolução ao livro
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

    # Adiciona a transação de devolução ao usuário
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

    return "Livro devolvido com sucesso!"

# Função para contar o número de livros emprestados atualmente por um usuário
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

# Função para consultar os livros atualmente emprestados por um usuário
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

# Função para consultar o histórico de transações de um livro
def get_book_transaction_history(book_id):
    book = books_collection.find_one({"_id": ObjectId(book_id)}, {"transactions": 1})
    if book and "transactions" in book:
        return book["transactions"]
    return []

# Função para consultar o histórico de transações de um usuário
def get_user_transaction_history(user_id):
    user = users_collection.find_one({"_id": ObjectId(user_id)}, {"transactions": 1})
    if user and "transactions" in user:
        return user["transactions"]
    return []
