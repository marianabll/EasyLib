from flask import Blueprint, jsonify, request
from app import mongo

# Criação de um blueprint para organizar as rotas
main = Blueprint('main', __name__)

@main.route('/users', methods=['GET'])
def get_users():
    """Retorna todos os usuários."""
    users = mongo.db.Users.find()
    return jsonify([user for user in users]), 200

@main.route('/books', methods=['GET'])
def get_books():
    """Retorna todos os livros disponíveis."""
    books = mongo.db.Books.find()
    return jsonify([book for book in books]), 200

@main.route('/transactions', methods=['POST'])
def create_transaction():
    """Cria uma nova transação."""
    data = request.json
    mongo.db.Transactions.insert_one(data)
    return jsonify({'message': 'Transaction created successfully'}), 201

@main.route('/user/<string:username>', methods=['GET'])
def get_user_by_username(username):
    """Retorna um usuário pelo nome de usuário."""
    user = mongo.db.Users.find_one({'username': username})
    if user:
        return jsonify(user), 200
    return jsonify({'error': 'User not found'}), 404
