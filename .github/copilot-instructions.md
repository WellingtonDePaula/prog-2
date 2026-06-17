# Instruções de Commit - Programação II (Python / Flask / SQLAlchemy)

Você está gerando mensagens de commit para um repositório acadêmico. 
Analise as alterações no código Python e classifique-as conforme as regras abaixo:

## 1. Identificação do Escopo
- Se a alteração for na pasta de exercícios: use `(exercicio)`
- Se a alteração for na pasta de trabalhos: use `(trabalho)`

## 2. Mapeamento Técnico (Convenções)
Escolha o tipo de commit (`feat`, `fix`, `refactor`, `docs`) baseando-se no que foi alterado:
- **Novas Rotas / Endpoints Flask:** Use `feat` (ex: criar rota de cadastro).
- **Modelos SQLAlchemy / Tabelas:** Use `feat` ou `refactor` (ex: definir modelo Usuario).
- **Consultas (Queries / CRUD):** Use `feat` ou `fix` (ex: buscar registros com filter_by).
- **Configurações / Banco de Dados:** Use `chore` ou `feat` (ex: configurar string de conexão).

## 3. Diretrizes de Escrita
- Escreva obrigatoriamente em **Português (Brasil)**.
- Comece o título com um verbo no infinitivo (ex: Adicionar, Corrigir, Implementar, Otimizar).
- Mencione os componentes relevantes (ex: Flask, SQLAlchemy, Modelo, Rota) quando apropriado.

## 4. Estrutura da Mensagem
[tipo][(escopo)]: [Título curto - máx 50 caracteres]

[Descrição detalhada explicando o conceito de Programação II ou da stack aplicado. Ex: Uso de herança em modelos, relacionamentos implicit_fk/relationship, validação de rotas, etc.]
