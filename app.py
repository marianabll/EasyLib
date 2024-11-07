from fastapi import FastAPI, HTTPException
from models import UserModel, BookModel, TransactionModel
from database import redis_client, books_collection
import library_manager

# Testar a conexão
try:
    redis_client.ping()
    print("Conectado ao Redis com sucesso!")
except Exception as e:
    print(f"Erro ao conectar ao Redis: {e}")

app = FastAPI()

# 1. Criar um novo usuário
@app.post("/users/")
async def create_user(user: UserModel):
    try:
        created_user = library_manager.create_user(user)
        return created_user
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 2. Obter um usuário pelo username
@app.get("/users/{username}")
def read_user(username):
    user = library_manager.get_user(username)
    if user:
        return user
    raise HTTPException(status_code=404, detail="User not found")

# 3. Obter um livro pelo ID
@app.get("/books/{book_id}")
async def read_book(book_id: str):
    book = library_manager.get_book(book_id)
    if book:
        return book
    raise HTTPException(status_code=404, detail="Book not found")

# 4. Emprestar um livro (com Redis)


# 5. Devolver um livro
@app.post("/books/return/")
async def return_book(user_id: str, book_id: str):
    result = library_manager.return_book(user_id, book_id)
    if result == "Book not borrowed by this user":
        raise HTTPException(status_code=400, detail="Book not borrowed by this user")
    return {"message": "Book returned successfully"}

# 6. Obter o histórico de transações de um livro
@app.get("/books/{book_id}/transactions")
async def get_book_transaction_history(book_id: str):
    transactions = library_manager.get_book_transaction_history(book_id)
    return transactions

# 7. Excluir um usuário a partir do seu username
@app.delete("/users/{username}")
async def delete_user(username: str):
    response = library_manager.delete_user(username)
    if response["message"] == "User deleted successfully":
        return response
    else:
        raise HTTPException(status_code=404, detail=response["message"])

# 8. Obter livros disponíveis de um determinado gênero usando agregação
@app.get("/books/available/")
async def get_available_books_by_genre(genre: str):
    books = library_manager.get_available_books_by_genre(genre)
    return books

# 9. Contar o total de transações por usuário usando agregação
@app.get("/users/transaction_count/")
async def get_transaction_count():
    try:
        transaction_counts = library_manager.get_transaction_count_per_user()
        return {"transaction_counts": transaction_counts}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 10. Cache para consulta de livros por gênero (Redis)
@app.get("/books/genre/")
async def get_books_by_genre(genre: str):
    cache_key = f"books_genre_{genre}"
    cached_books = redis_client.get(cache_key)

    if cached_books:
        return {"source": "cache", "books": eval(cached_books)}

    # Caso não exista em cache, consulta o MongoDB
    books = list(books_collection.find({"book_genre": genre, "available": True}, {"_id": 1, "book_name": 1, "author.name": 1}))
    
    if not books:
        raise HTTPException(status_code=404, detail="No books found for this genre")

    # Armazena no cache e retorna
    redis_client.setex(cache_key, 300, str(books))  # Expiração de 5 minutos
    return {"source": "database", "books": books}

# 11. Contador de empréstimos por usuário (Redis)
from fastapi import HTTPException

@app.post("/borrow-book/{user_id}/{book_id}")
async def borrow_book(user_id: str, book_id: str):
    result = library_manager.borrow_book(user_id, book_id)

    if result["status"] == "error":
        raise HTTPException(status_code=404, detail=result["message"])

    # Obtém a contagem de empréstimos atualizada do Redis
    loan_count = redis_client.hget("loan_counter", user_id)
    
    return {"message": result["message"], "loan_count": int(loan_count) if loan_count else 0}


@app.get("/user-loan-count/{user_id}")
async def get_user_loan_count(user_id: str):
    loan_count = redis_client.hget("loan_counter", user_id)
    
    if loan_count is None:
        return {"message": "No loans found for this user", "loan_count": 0}
    
    return {"user_id": user_id, "loan_count": int(loan_count)}




# Iniciar o servidor FastAPI
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
