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
- **username:** Nome de usuário
- **email:** Email do usuário
- **full_name:** Nome completo do usuário
- **password_hash:** Senha hash do usuário
- **date_of_birth:** Data de nascimento do usuário
- **join_date:** Data de registro do usuário
- **is_active:** Status de atividade do usuário (verdadeiro ou falso)
- **favorite_genres:** Lista de gêneros favoritos do usuário
- **transactions:** Histórico de transações realizadas pelo usuário

### Books
- **_id:** Identificador único do livro
- **book_name:** Título do livro
- **author:** Informações sobre o autor
  - **name:** Nome do autor
  - **birth_date:** Data de nascimento do autor
  - **nationality:** Nacionalidade do autor
- **publisher:** Editora do livro
- **release_year:** Ano de lançamento do livro
- **book_genre:** Gênero do livro
- **pages:** Número de páginas do livro
- **isbn:** ISBN do livro
- **summary:** Resumo do livro
- **average_rating:** Avaliação média do livro
- **available:** Status de disponibilidade do livro (verdadeiro ou falso)
- **tags:** Lista de tags relacionadas ao livro
- **transactions:** Histórico de transações a que o livro foi submetido

## Tecnologias Utilizadas

- [MongoDB](https://www.mongodb.com/)
- [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
- Python (para o backend)
- FastAPI (para a construção da API)
