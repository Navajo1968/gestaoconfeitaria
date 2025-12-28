# Sistema de Gestão de Confeitaria 🧁

Sistema completo de gestão para confeitarias, desenvolvido em Python com interface de linha de comando (CLI).

## 📋 Funcionalidades

### 1. Gerenciamento de Produtos
- Cadastrar produtos (bolos, tortas, doces, etc.)
- Listar todos os produtos
- Atualizar informações de produtos
- Excluir produtos
- Armazenar preço e tempo de preparo

### 2. Gerenciamento de Clientes
- Cadastrar clientes com informações de contato
- Manter registro de telefone, email e endereço
- Atualizar dados de clientes
- Listar todos os clientes

### 3. Gerenciamento de Pedidos
- Criar pedidos completos com múltiplos itens
- Associar pedidos a clientes
- Definir data de entrega
- Acompanhar status dos pedidos:
  - Pendente
  - Em Produção
  - Pronto
  - Entregue
  - Cancelado
- Calcular valor total automaticamente
- Adicionar observações específicas

### 4. Controle de Estoque
- Cadastrar ingredientes e materiais
- Monitorar quantidades disponíveis
- Alertas de estoque baixo
- Definir quantidades mínimas
- Suporte a diferentes unidades de medida

### 5. Relatórios
- Relatório de pedidos por status
- Resumo de vendas
- Produtos mais vendidos
- Total de receitas

## 🚀 Como Usar

### Requisitos
- Python 3.7 ou superior
- SQLite3 (já incluído no Python)

### Instalação

1. Clone o repositório:
```bash
git clone https://github.com/Navajo1968/gestaoconfeitaria.git
cd gestaoconfeitaria
```

2. (Opcional) Crie um ambiente virtual:
```bash
python3 -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

### Executar o Sistema

```bash
python3 main.py
```

### Executar os Testes

```bash
python3 test_sistema.py
```

## 📁 Estrutura do Projeto

```
gestaoconfeitaria/
├── main.py              # Aplicação principal com interface CLI
├── models.py            # Modelos de domínio (Produto, Cliente, Pedido, etc.)
├── database.py          # Camada de acesso ao banco de dados
├── test_sistema.py      # Testes unitários
├── requirements.txt     # Dependências do projeto
├── .gitignore          # Arquivos a serem ignorados pelo Git
└── README.md           # Este arquivo
```

## 🗄️ Modelo de Dados

### Produto
- ID, Nome, Descrição, Preço, Tempo de Preparo

### Cliente
- ID, Nome, Telefone, Email, Endereço

### Pedido
- ID, Cliente, Data do Pedido, Data de Entrega, Status, Observações
- Lista de Itens do Pedido

### Item de Pedido
- ID, Pedido, Produto, Quantidade, Preço Unitário, Observações

### Estoque
- ID, Nome, Unidade de Medida, Quantidade Atual, Quantidade Mínima

## 💡 Exemplos de Uso

### Criar um Produto
1. Selecione "1. Gerenciar Produtos"
2. Escolha "2. Adicionar produto"
3. Preencha: Nome, Descrição, Preço, Tempo de preparo

### Fazer um Pedido
1. Primeiro, cadastre um cliente (opção 2 do menu principal)
2. Selecione "3. Gerenciar Pedidos"
3. Escolha "2. Criar novo pedido"
4. Selecione o cliente
5. Defina a data de entrega
6. Adicione produtos ao pedido

### Verificar Estoque Baixo
1. Selecione "4. Gerenciar Estoque"
2. Escolha "4. Itens com estoque baixo"
3. O sistema mostrará todos os itens que precisam de reposição

## 🧪 Testes

O projeto inclui testes unitários para:
- Modelos de domínio
- Operações de banco de dados
- Cálculos (subtotais, totais)
- CRUD de todas as entidades

Execute: `python3 test_sistema.py`

## 🔒 Segurança

- Dados armazenados localmente em SQLite
- Sem exposição de dados sensíveis
- Validações de entrada implementadas

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para:
1. Fazer um fork do projeto
2. Criar uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abrir um Pull Request

## 📧 Contato

Para dúvidas ou sugestões, abra uma issue no GitHub.

---

Desenvolvido com ❤️ para facilitar a gestão de confeitarias
