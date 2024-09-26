# Consultas MongoDB para Gerenciamento de Biblioteca

## Introdução

Este documento contém exemplos de consultas MongoDB para a coleção `Books` do projeto de gerenciamento de biblioteca. As consultas permitem verificar a disponibilidade de livros, listar livros por gênero ou autor e atualizar informações relevantes.

## Estrutura da Coleção `Books`

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
  "summary": "Uma crítica à totalitarismo através da história de Winston Smith.",
  "average_rating": { "$numberDouble": "4.8" },
  "is_book_available": false,
  "tags": ["dystopia", "politics", "surveillance"]
}
```

## Consultas para a coleção `Books`

### Verificar Disponibilidade de um Livro

db.Books.findOne({ book_name: "1984" }, { is_book_available: 1 })

### Listar Livros Disponíveis por Gênero

db.Books.find({ is_book_available: true })

### Consultar Livros por Autor

db.Books.find({ "author.name": "George Orwell" })

