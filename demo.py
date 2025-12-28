#!/usr/bin/env python3
"""
Demo Script - Sistema de Gestão de Confeitaria
Demonstrates the main features of the bakery management system
"""

from datetime import datetime, timedelta
from database import Database
from models import Produto, Cliente, Pedido, ItemPedido, Estoque, StatusPedido


def demo():
    """Demonstração das funcionalidades do sistema"""
    print("="*70)
    print("   DEMONSTRAÇÃO - SISTEMA DE GESTÃO DE CONFEITARIA")
    print("="*70)
    
    # Inicializa o banco de dados
    print("\n1. Inicializando banco de dados...")
    db = Database("demo_confeitaria.db")
    print("   ✓ Banco de dados criado")
    
    # Cria produtos
    print("\n2. Cadastrando produtos...")
    produtos_data = [
        ("Bolo de Chocolate", "Bolo de chocolate com cobertura", 50.00, 120),
        ("Torta de Limão", "Torta de limão siciliano", 45.00, 90),
        ("Brigadeiro Gourmet", "Brigadeiro com chocolate belga", 3.50, 15),
        ("Cupcake Red Velvet", "Cupcake com cobertura cream cheese", 8.00, 30),
        ("Brownie", "Brownie de chocolate com nozes", 6.00, 25)
    ]
    
    produtos_ids = []
    for nome, desc, preco, tempo in produtos_data:
        produto = Produto(None, nome, desc, preco, tempo)
        produto_id = db.criar_produto(produto)
        produtos_ids.append(produto_id)
        print(f"   ✓ {nome} cadastrado (ID: {produto_id})")
    
    # Cria clientes
    print("\n3. Cadastrando clientes...")
    clientes_data = [
        ("Maria Silva", "11999999999", "maria@email.com", "Rua das Flores, 123"),
        ("João Santos", "11988888888", "joao@email.com", "Av. Principal, 456"),
        ("Ana Costa", "11977777777", "ana@email.com", None)
    ]
    
    clientes_ids = []
    for nome, tel, email, end in clientes_data:
        cliente = Cliente(None, nome, tel, email, end)
        cliente_id = db.criar_cliente(cliente)
        clientes_ids.append(cliente_id)
        print(f"   ✓ {nome} cadastrado (ID: {cliente_id})")
    
    # Cria itens de estoque
    print("\n4. Cadastrando itens de estoque...")
    estoque_data = [
        ("Farinha de Trigo", "kg", 50.0, 10.0),
        ("Açúcar", "kg", 30.0, 8.0),
        ("Chocolate em Pó", "kg", 15.0, 5.0),
        ("Ovos", "dúzia", 20.0, 5.0),
        ("Manteiga", "kg", 8.0, 3.0)
    ]
    
    for nome, unidade, qtd, qtd_min in estoque_data:
        item = Estoque(None, nome, unidade, qtd, qtd_min)
        item_id = db.criar_item_estoque(item)
        print(f"   ✓ {nome}: {qtd} {unidade} (mínimo: {qtd_min} {unidade})")
    
    # Cria pedidos
    print("\n5. Criando pedidos...")
    
    # Pedido 1: Maria - 2 Bolos de Chocolate
    pedido1 = Pedido(
        None, clientes_ids[0], 
        datetime.now(), 
        datetime.now() + timedelta(days=2),
        StatusPedido.PENDENTE,
        "Entrega pela manhã, por favor"
    )
    produto1 = db.obter_produto(produtos_ids[0])
    pedido1.adicionar_item(ItemPedido(None, None, produtos_ids[0], 2, produto1.preco))
    pedido1_id = db.criar_pedido(pedido1)
    print(f"   ✓ Pedido #{pedido1_id} criado para Maria Silva")
    print(f"     - 2x Bolo de Chocolate = R$ {pedido1.valor_total:.2f}")
    
    # Pedido 2: João - Mix de doces
    pedido2 = Pedido(
        None, clientes_ids[1],
        datetime.now(),
        datetime.now() + timedelta(days=1),
        StatusPedido.EM_PRODUCAO
    )
    produto2 = db.obter_produto(produtos_ids[2])  # Brigadeiro
    produto3 = db.obter_produto(produtos_ids[3])  # Cupcake
    pedido2.adicionar_item(ItemPedido(None, None, produtos_ids[2], 50, produto2.preco, "Embalagem para presente"))
    pedido2.adicionar_item(ItemPedido(None, None, produtos_ids[3], 12, produto3.preco))
    pedido2_id = db.criar_pedido(pedido2)
    print(f"   ✓ Pedido #{pedido2_id} criado para João Santos")
    print(f"     - 50x Brigadeiro Gourmet")
    print(f"     - 12x Cupcake Red Velvet")
    print(f"     - Total: R$ {pedido2.valor_total:.2f}")
    
    # Pedido 3: Ana - Torta de Limão
    pedido3 = Pedido(
        None, clientes_ids[2],
        datetime.now(),
        datetime.now() + timedelta(hours=4),
        StatusPedido.PRONTO
    )
    produto4 = db.obter_produto(produtos_ids[1])
    pedido3.adicionar_item(ItemPedido(None, None, produtos_ids[1], 1, produto4.preco))
    pedido3_id = db.criar_pedido(pedido3)
    print(f"   ✓ Pedido #{pedido3_id} criado para Ana Costa")
    print(f"     - 1x Torta de Limão = R$ {pedido3.valor_total:.2f}")
    
    # Exibe estatísticas
    print("\n6. Estatísticas do Sistema:")
    print("   " + "-"*66)
    
    todos_produtos = db.listar_produtos()
    todos_clientes = db.listar_clientes()
    todos_pedidos = db.listar_pedidos()
    todos_estoque = db.listar_estoque()
    
    print(f"   Total de produtos cadastrados: {len(todos_produtos)}")
    print(f"   Total de clientes cadastrados: {len(todos_clientes)}")
    print(f"   Total de pedidos realizados: {len(todos_pedidos)}")
    print(f"   Total de itens no estoque: {len(todos_estoque)}")
    
    valor_total_pedidos = sum(p.valor_total for p in todos_pedidos)
    print(f"   Valor total em pedidos: R$ {valor_total_pedidos:.2f}")
    
    # Pedidos por status
    print("\n   Pedidos por status:")
    for status in StatusPedido:
        pedidos_status = [p for p in todos_pedidos if p.status == status]
        if pedidos_status:
            print(f"     - {status.value}: {len(pedidos_status)}")
    
    # Alerta de estoque
    print("\n7. Verificando estoque...")
    itens_baixos = [item for item in todos_estoque if item.precisa_reposicao]
    if itens_baixos:
        print("   ⚠️  ATENÇÃO: Itens com estoque baixo:")
        for item in itens_baixos:
            print(f"     - {item.nome}: {item.quantidade_atual} {item.unidade_medida}")
    else:
        print("   ✓ Todos os itens estão com estoque adequado")
    
    print("\n" + "="*70)
    print("   DEMONSTRAÇÃO CONCLUÍDA COM SUCESSO!")
    print("="*70)
    print("\n📝 Nota: Um arquivo 'demo_confeitaria.db' foi criado.")
    print("   Execute 'python3 main.py' e aponte para este arquivo para explorar os dados.")
    print("\n   Para usar o sistema com seus próprios dados, execute:")
    print("   $ python3 main.py")
    print("="*70)


if __name__ == "__main__":
    demo()
