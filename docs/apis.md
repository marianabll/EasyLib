# APIs para EasyLib

## Introdução

Este documento contém as APIs que foram criadas e testadas para _algumas_ das consultas MongoDB. Elas permitem realizar as quatro operações básicas (CRUD) das aplicações que manipulam dados:


## CRIAR

### create_user()
Permite criar um novo usuário usando o modelo Pydantic (a criação de um novo livro segue a mesma lógica).

```
@app.post("/users/")
async def create_user(user: UserModel):
    try:
        created_user = library_manager.create_user(user)
        return created_user
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

## LER
Permite obter um livro pelo ID ou um usuário por seu _username_.

### get_book()

```
@app.get("/books/{book_id}")
async def read_book(book_id: str):
    book = library_manager.get_book(book_id)
    if book:
        return book
    raise HTTPException(status_code=404, detail="Book not found")
```

### get_user()

```
@app.get("/users/{username}")
def read_user(username):
    user = library_manager.get_user(username)
    if user:
        return user
    raise HTTPException(status_code=404, detail="User not found")
```

## ATUALIZAR
Embora nenhuma API tenha sido criada para atualizar pontualmente um documento (o nome de um livro ou a data de nascimento de um usuário, por exemplo), duas operações provocarão atualizações simultâneas nas duas coleções (Users e Books): a de **empréstimo** e a de **devolução** de um livro.

### borrow_book()
Permite registrar uma nova transação de empréstimo de livro, atualizar sua disponibilidade e aumentar o número de livros emprestados com o usuário que o pegou.

```
ATUALIZAR
```

### return_book()
Permite registrar uma nova transação de devolução de livro, atualizar sua disponibilidade e diminuir o número de livros emprestados com o usuário que o pegou.

```
ATUALIZAR
```

## APAGAR

### delete_user()
Permite excluir do banco de dados um usuário identificado a partir do seu username.

```
@app.delete("/users/{username}")
async def delete_user(username: str):
    response = library_manager.delete_user(username)
    if response["message"] == "User deleted successfully":
        return response
    else:
        raise HTTPException(status_code=404, detail=response["message"])
```

## EXTRA: CONSULTA ENVOLVENDO AGREGAÇÃO
Como requisito especial do projeto, uma consulta envolvendo agregação retornará a lista de livros disponíveis de um determinado gênero.

```
@app.get("/books/available/")
async def get_available_books_by_genre(genre: str):
    books = library_manager.get_available_books_by_genre(genre)
    return books
```
