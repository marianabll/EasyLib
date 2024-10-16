# Consultas MongoDB para EasyLib

## Introdução

Este documento contém exemplos de consultas MongoDB para as duas coleções (`Books` e `Users`) do projeto de gerenciamento de biblioteca. As consultas permitem verificar a disponibilidade de livros, listar livros por gênero ou autor, verificar a permissão de retirada para um determinado usuário e registrar novas retiradas/devoluções de livros.

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
  "available": false,
  "borrowed_by": {
    "user_id": "66f5bff7b7394dd698d8e1a7",
    "borrowed_date: "2023-01-10"
  }
}
```

### Exemplos de consultas para a coleção `Books`

#### Verificar Disponibilidade de um Livro

```db.Books.findOne({ book_name: "1984" }, { is_book_available: 1 })```

#### Consultar Livros por Autor

```db.Books.find({ "author.name": "George Orwell" })```

#### Listar Livros Disponíveis por Gênero

```db.Books.find({ book_genre: "Dystopian", is_book_available: true })```

#### Retornar Livros Disponíveis de um Determinado Gênero usando Agregação
```
db.Books.aggregate([
  {
    $match: {
      available: true,            // Filtra apenas livros disponíveis
      genres: "Gênero Específico" // Substitua por um gênero desejado
    }
  },
  {
    $project: {
      title: 1,     // Inclui o título do livro
      author: 1,    // Inclui o autor do livro
      status: 1     // Inclui o status do livro
    }
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
  "borrowed_books": [{"book_id": "66f5b5b2b7394dd698d8e1a6"}]
}
```

### Exemplos de consultas para a coleção `Users`

#### Verificar se um Usuário está Registrado na Biblioteca

```db.Users.findOne({ username: "joaosilva" })```

#### Consultar o Número de Livros que um Usuário Mantém em Mãos

```db.Users.findOne({ _id: ObjectId("66f37341f0b1344ec2bba9df") }, { number_of_books_issued: 1 })```

