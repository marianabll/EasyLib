# APIs para EasyLib

## Introdução

Este documento contém as APIs que foram criadas e testadas para _algumas_ das consultas MongoDB. Elas permitem realizar as quatro operações básicas (CRUD) das aplicações que manipulam dados:
- CRIAR:a disponibilidade de livros, listar livros por gênero ou autor, verificar a permissão de retirada para um determinado usuário e registrar novas retiradas/devoluções de livros. No arquivo `app/library_manager.py`, elas foram devidamente definidas dentro de funções.

## CRIAR

### create_user()
Permite criar um novo usuário usando o modelo Pydantic (a criação de um novo livro seguiria o mesmo processo).

```
@app.post("/users/")
async def create_user(user: UserModel):
    try:
        created_user = library_manager.create_user(user)
        return created_user
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

#### Verificar Disponibilidade de um Livro

```db.Books.findOne({ book_name: "1984" }, { available: 1 })```

#### Consultar Livros por Autor

```db.Books.find({ "author.name": "George Orwell" })```

#### Listar Livros Disponíveis por Gênero

```db.Books.find({ book_genre: "Dystopian", available: true })```

#### Retornar Livros Disponíveis de um Determinado Gênero usando Agregação
```
db.Books.aggregate([
  {
    $match: {
      available: true,            // Filtra apenas livros disponíveis
      book_genre: "Gênero Específico" // Substituir pelo gênero desejado
    }
  },
  {
    $project: {{
            "_id": {"$toString": "$_id"},  # Converte o _id para string
            "book_name": 1,
            "author.name": 1,
    }}
  }
])
```

## 2. Coleção `Users`

A coleção `Users` contém documentos com a seguinte estrutura:

```json
{
  "_id": { "$oid": "66f5bff7b7394dd698d8e1a7" },
  "username": "joaosilva",
  "email": "joaosilva@example.com",
  "full_name": "João Silva",
  "password_hash": "hashed_password_1",
  "date_of_birth": "1990-05-15",
  "join_date": "2023-01-10",
  "is_active": true,
  "favorite_genres": ["Fiction", "Adventure"],
  "number_of_books_issued": { "$numberInt": "1" },
  "borrowed_books": ["66f5b5b2b7394dd698d8e1a6"]
}
```

### Exemplos de consultas para a coleção `Users`

#### Verificar se um Usuário está Registrado na Biblioteca

```db.Users.findOne({ username: "joaosilva" })```

#### Consultar o Número de Livros que um Usuário Mantém em Mãos

```db.Users.findOne({ _id: ObjectId("66f37341f0b1344ec2bba9df") }, { number_of_books_issued: 1 })```

