# Consultas usando Redis

## Introdução

O Redis será incorporado como uma camada de cache ou banco de dados intermediário em funcionalidades onde a rapidez no acesso e a baixa latência fazem a diferença:

### 1. Cache para consulta de livros por gênero
Aqui, o Redis atuará como cache para armazenar consultas recentes de livros por gênero, evitando o acesso ao MongoDB toda vez que a consulta é feita para o mesmo gênero.



### 2. Armazenamento de sessões de usuários ativos
Esse recurso salva o status dos usuários logados, permitindo a verificação rápida de quem está ativo, com dados que expiram automaticamente após um certo tempo de inatividade.



#### 3. Contador de empréstimos por usuário
Essa funcionalidade registra o número de empréstimos feitos por cada usuário, útil para gerar estatísticas de uso e para otimizar contagens de empréstimos.
