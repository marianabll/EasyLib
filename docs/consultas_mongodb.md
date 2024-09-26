# Consultas MongoDB para EasyLib

## Introdução

Este documento contém exemplos de consultas MongoDB para as três coleções (`Books`, `Users` e `Transactions`) do projeto de gerenciamento de biblioteca. As consultas permitem verificar a disponibilidade de livros, listar livros por gênero ou autor, verificar a permissão de retirada para um determinado usuário e registrar novas retiradas/devoluções de livros.

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
  "is_book_available": false,
  "tags": ["dystopia", "politics", "surveillance"]
}
```

### Consultas para a coleção `Books`

#### Verificar Disponibilidade de um Livro

```db.Books.findOne({ book_name: "1984" }, { is_book_available: 1 })```

#### Listar Livros Disponíveis por Gênero

```db.Books.find({ book_genre: "Dystopian", is_book_available: true })```

#### Consultar Livros por Autor

```db.Books.find({ "author.name": "George Orwell" })```

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
  "number_of_books_issued": { "$numberInt": "1" }
}
```

### Consultas para a coleção `Users`

#### Verificar se um Usuário está Registrado na Biblioteca

```db.Users.findOne({ username: "joaosilva" })```

#### Consultar o Número de Livros que um Usuário Mantém em Mãos

```db.Users.findOne({ _id: ObjectId("66f37341f0b1344ec2bba9df") }, { number_of_books_issued: 1 })```


## 3. Coleção `Transactions`

A coleção `Transactions` contém documentos com a seguinte estrutura:

```json
{
  "_id": { "$oid": "66f5c071b7394dd698d8e1a8" },
  "user_id": { "$oid": "66f37341f0b1344ec2bba9df" },
  "user_name": "João Silva",
  "book_id": { "$oid": "66f37341f0b1344ec2bba9d5" },
  "book_name": "1984",
  "transaction_type": "issued",  // pode ser "issued" ou "returned"
  "transaction_date": "2023-08-15"
}
```

### Consulta para a coleção `Transactions`

#### Obter Todos os Livros Emprestados para um Usuário

```
db.Transactions.find({
    user_id: ObjectId("66f37341f0b1344ec2bba9df"),
    transaction_type: "issued"
})```
