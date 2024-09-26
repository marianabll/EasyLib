from app import mongo
from bson.objectid import ObjectId

class UserModel:
    @staticmethod
    def get_user_by_username(username):
        """Obtém um usuário pelo nome de usuário."""
        return mongo.db.Users.find_one({"username": username})

    @staticmethod
    def create_user(user_data):
        """Cria um novo usuário."""
        mongo.db.Users.insert_one(user_data)
        return user_data

    @staticmethod
    def update_user(username, update_data):
        """Atualiza as informações de um usuário."""
        mongo.db.Users.update_one({"username": username}, {"$set": update_data})

    @staticmethod
    def delete_user(username):
        """Remove um usuário pelo nome de usuário."""
        mongo.db.Users.delete_one({"username": username})

class BookModel:
    @staticmethod
    def get_all_books():
        """Obtém todos os livros."""
        return list(mongo.db.Books.find())

    @staticmethod
    def get_book_by_id(book_id):
        """Obtém um livro pelo ID."""
        return mongo.db.Books.find_one({"_id": ObjectId(book_id)})

    @staticmethod
    def create_book(book_data):
        """Cria um novo livro."""
        mongo.db.Books.insert_one(book_data)
        return book_data

class TransactionModel:
    @staticmethod
    def create_transaction(transaction_data):
        """Cria uma nova transação."""
        mongo.db.Transactions.insert_one(transaction_data)
        return transaction_data

    @staticmethod
    def get_transactions_by_user(user_id):
        """Obtém todas as transações de um usuário específico."""
        return list(mongo.db.Transactions.find({"user_id": ObjectId(user_id)}))
