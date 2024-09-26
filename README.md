# EasyLib
## Gerenciamento de Biblioteca com MongoDB

## Descrição

Este projeto foi desenvolvido para a disciplina "Banco de Dados NoSQL" e tem como objetivo gerenciar uma biblioteca utilizando o MongoDB Atlas. A aplicação permite registrar retiradas e devoluções de livros, além de consultar a disponibilidade de um livro e a situação dos usuários.

## Funcionalidades

- **Registro de Usuários:** Adiciona novos usuários ao sistema.
- **Cadastro de Livros:** Permite o registro de novos livros na biblioteca.
- **Gerenciamento de Transações:** Registra retiradas e devoluções de livros.
- **Consulta de Disponibilidade:** Verifica se um livro está disponível para retirada.
- **Consulta de Usuários:** Verifica a situação atual de um usuário em relação aos livros emprestados.

## Estrutura das Coleções

### Users
- **_id:** Identificador único do usuário
- **name:** Nome do usuário
- **email:** Email do usuário
- **borrowedBooks:** Lista de livros retirados pelo usuário

### Books
- **_id:** Identificador único do livro
- **title:** Título do livro
- **author:** Autor do livro
- **available:** Indica se o livro está disponível para retirada

### Transactions
- **_id:** Identificador único da transação
- **userId:** ID do usuário que realizou a transação
- **bookId:** ID do livro retirado ou devolvido
- **date:** Data da transação
- **type:** Tipo da transação (retirada ou devolução)

## Tecnologias Utilizadas

- [MongoDB](https://www.mongodb.com/)
- [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
- Python (para o backend)
- Flask (para a construção da API)
