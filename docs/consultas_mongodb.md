# Consultas MongoDB para EasyLib

## Introdução

Este documento contém _alguns_ exemplos de documentos e de consultas MongoDB para as duas coleções (`Books` e `Users`) do projeto de gerenciamento de biblioteca. As consultas permitirão verificar a disponibilidade de livros, listar livros por gênero ou autor, registrar novas retiradas/devoluções de livros etc. No arquivo `app/library_manager.py`, elas foram devidamente definidas dentro de funções.

## 1. Coleção `Books`

A coleção `Books` contém documentos com a seguinte estrutura:

```json
{
  "_id": { "$oid": "66f5b5b2b7394dd698d8e1a6" },
  "book_name": "1984",
  "author": {
    "name": "George Orwell",
    "birth_date": "1903-06-25",
    "nationality": "British"
  },
  "publisher": "Companhia das Letras",
  "release_year": { "$numberInt": "1949" },
  "book_genre": "Dystopian",
  "pages": { "$numberInt": "328" },
  "isbn": "978-8535932003",
  "summary": "Uma crítica ao totalitarismo através da história de Winston Smith.",
  "average_rating": { "$numberDouble": "4.8" },
  "tags": ["dystopia", "politics", "surveillance"],
  "transactions": []
}
```

### Exemplos de consultas para a coleção `Books`

#### Verificar Disponibilidade de um Livro

```db.Books.findOne({ book_name: "1984" }, { available: 1 })```

#### Consultar Livros por Autor

```db.Books.find({ "author.name": "George Orwell" })```

#### Listar Livros Disponíveis por Gênero sem Agregação

```db.Books.find({ book_genre: "Dystopian", available: true })```

#### Listar Livros Disponíveis por Gênero usando Agregação
```
db.Books.aggregate([
  {
    $match: {
      available: true,                     # Filtra apenas livros disponíveis
      book_genre: "Gênero Específico"      # A ser substituido pelo gênero desejado
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
  "transactions": []
}
```

### Exemplo de consultas para a coleção `Users`

#### Verificar se um Usuário está Registrado na Biblioteca

```db.Users.findOne({ username: "joaosilva" })```


